from urllib import urlopen
from dateutil import parser
from classification.classifier import Classifier
import json
import datetime
from time import sleep
from sys import stdout
import urllib2


def getData(url):
    response = urlopen(url)
    response = response.read()
    data = json.loads(response)
    return data


def groupData(mobileData, sensorData):
    groups = list()
    for mobileEntry in mobileData:
        date = mobileEntry["datetime"]
        date = parser.parse(date)
        minDelta = None
        bestMatch = None
        for sensorEntry in sensorData:
            date2 = sensorEntry["datetime"]
            date2 = parser.parse(date2)
            date2 -= datetime.timedelta(hours=2)
            delta = abs(date - date2)
            if minDelta is None:
                minDelta = delta
                bestMatch = sensorEntry
            else:
                if delta < minDelta:
                    minDelta = delta
                    bestMatch = sensorEntry
        groups.append((mobileEntry["vasScore"], bestMatch))
    return groups


def extractFeatures(groups, featureNames):
    features = list()
    labels = list()
    for group in groups:
        labels.append(group[0])
        featuresList = list()
        for key, value in group[1].iteritems():
            if key in featuresNames:
                if value is None:
                    value = 0
                if isinstance(value, dict):
                    for key2, value2 in value.iteritems():
                        featuresList.append(value2)
                else:
                    featuresList.append(value)
        features.append(featuresList)
    return features, labels


def getLatestSensorData(url):
    data = getData(url)
    latestDate = None
    latestEntry = None
    for entry in data:
        date = entry["datetime"]
        date = parser.parse(date)
        if latestDate is None:
            latestDate = date
            latestEntry = entry
        else:
            if date > latestDate:
                latestDate = date
                latestEntry = entry
    return latestEntry


def postPrediction(prediction):
    req = urllib2.Request(
        'http://sensing-ms-api.mybluemix.net/api/Patients/0/VasScores?'
        'access_token=QCOI7AjXi7Is90f9hK0BQsOQuKxoU2ISnBa9HLt6Bmsg0nvQbOqPAbELCzTsl2ww'
    )
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(prediction))
    html = response.read()
    html = json.loads(html)
    print "Success!\n"
    print "Result:"
    for key, value in html.iteritems():
        if isinstance(value, dict):
            print str(key) + ":"
            for key2, value2 in value.iteritems():
                print "     " + str(key2) + ": " + str(value2)
        else:
            print str(key) + ": " + str(value)

if __name__ == "__main__":
    mobileUrl = "http://sensing-ms-api.mybluemix.net/api/Patients/0/" \
                "mobileData?access_token=QCOI7AjXi7Is90f9hK0BQsOQuKxoU2ISnBa9HLt6Bmsg0nvQbOqPAbELCzTsl2ww"
    sensorUrl = "http://sensing-ms-api.mybluemix.net/api/Patients/0/" \
                "sensorData?access_token=QCOI7AjXi7Is90f9hK0BQsOQuKxoU2ISnBa9HLt6Bmsg0nvQbOqPAbELCzTsl2ww"
    featuresNames = ["heartrate", "temperature", "steps", "activity"]
    allFeaturesNames = [
        "heartrate_std", "heartrate_max", "heartrate_avg", "heartrate_min",
        "temperature_std", "temperature_max", "temperature_avg", "temperature_min",
        "steps", "activity_score", "activity_minutes"

    ]
    mobileData = getData(mobileUrl)
    sensorData = getData(sensorUrl)
    groups = groupData(mobileData, sensorData)
    features, labels = extractFeatures(groups, featuresNames)
    clf = Classifier()
    clf.train(features, labels)
    rules = clf.getDangerousRules(allFeaturesNames)
    print rules
    maxSeconds = 1
    seconds = maxSeconds
    previousSensorData = None
    while True:
        if seconds > 0:
            print "\nWaiting for "+str(seconds)+" seconds."
            sleep(1)
            seconds -= 1
        else:
            print "\nStarting again..."
            latestSensorData = getLatestSensorData(sensorUrl)
            if previousSensorData is None or latestSensorData["datetime"] != previousSensorData["datetime"]:
                previousSensorData = latestSensorData
                features, _ = extractFeatures([("?", latestSensorData)], featuresNames)
                features = features[0]
                score = clf.predict(features)
                score = score[0]
                prediction = {"score": score, "datetime": latestSensorData["datetime"]}
                postPrediction(prediction)
                seconds = maxSeconds
            else:
                print "No new data..."
