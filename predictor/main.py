from urllib import urlopen
from dateutil import parser
from classification.classifier import Classifier
import json
import datetime


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


def extractFeatures(groups):
    features = list()
    labels = list()
    featuresNames = ["heartrate", "temperature", "steps", "activity"]
    for group in groups:
        labels.append(group[0])
        featuresList = list()
        for key, value in group[1].iteritems():
            if key in featuresNames:
                if isinstance(value, dict):
                    for value2 in value.values():
                        featuresList.append(value2)
                else:
                    featuresList.append(value)
        features.append(featuresList)
    return features, labels

if __name__ == "__main__":
    mobileUrl = "http://sensing-ms-api.mybluemix.net/api/Patients/0/" \
                "mobileData?access_token=QCOI7AjXi7Is90f9hK0BQsOQuKxoU2ISnBa9HLt6Bmsg0nvQbOqPAbELCzTsl2ww"
    sensorUrl = "http://sensing-ms-api.mybluemix.net/api/Patients/0/" \
                "sensorData?access_token=QCOI7AjXi7Is90f9hK0BQsOQuKxoU2ISnBa9HLt6Bmsg0nvQbOqPAbELCzTsl2ww"
    mobileData = getData(mobileUrl)
    sensorData = getData(sensorUrl)
    groups = groupData(mobileData, sensorData)
    features, labels = extractFeatures(groups)
    clf = Classifier()
    clf.train(features, labels)
    pass