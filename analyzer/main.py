from os import listdir, stat
from time import sleep
from analyze.analyzer import Analyzer
import json
import urllib2


def filesAvailable(directory):
    fileNames = listdir(directory)
    if ".DS_Store" in fileNames:
        fileNames.remove(".DS_Store")
    if len(fileNames) > 0:
        for fileName in fileNames:
            path = str(directory)+str(fileName)
            if stat(path).st_size > 0:
                return True
        return False
    return False


def postData(analyzedDict):
    req = urllib2.Request(
        'http://sensing-ms-api.mybluemix.net/api/Patients/0/SensorData?'
        'access_token=QCOI7AjXi7Is90f9hK0BQsOQuKxoU2ISnBa9HLt6Bmsg0nvQbOqPAbELCzTsl2ww'
    )
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(analyzedDict))
    html = response.read()
    html = json.loads(html)
    print "Success!\n"
    print "Result:"
    for key, value in html.iteritems():
        if isinstance(value, dict):
            print str(key)+":"
            for key2, value2 in value.iteritems():
                print "     "+str(key2)+": "+str(value2)
        else:
            print str(key)+": "+str(value)


if __name__ == "__main__":
    directory = "../device/data/analyze/"
    analyzer = Analyzer(directory)
    while True:
        if filesAvailable(directory):
            print "\nNew files are available.\nWaiting for all data..."
            sleep(2)
            print "Data received.\nStart analyzing..."
            analyzedDict = analyzer.analyze()
            print "Data analyzed.\nStart posting..."
            postData(analyzedDict)
        sleep(5)



