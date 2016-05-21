import csv
from os import listdir, remove
from collections import defaultdict
from heartratedata import HeartrateData
from activitydata import ActivityData
from temperaturedata import TemperatureData
from stepsdata import StepsData
from stressdata import StressData


class CSVReader(object):

    directory = None
    sensorData = None

    def __init__(self, directory):
        self.directory = directory

    def read(self):
        self.sensorData = defaultdict(list)
        fileNames = listdir(self.directory)
        for fileName in fileNames:
            sensor = fileName[:-4]
            path = str(self.directory) + str(fileName)
            with open(path, "rb") as csvFile:
                reader = csv.reader(csvFile, delimiter=",")
                dataList = [map(lambda x: eval(x), row) for row in reader if row != []]
                self.sensorData[sensor] = dataList

    def clear(self):
        self.sensorData = None
        fileNames = listdir(self.directory)
        for fileName in fileNames:
            path = str(self.directory) + str(fileName)
            remove(path)

    def getData(self):
        heartrateData = HeartrateData(self.sensorData)
        activityData = ActivityData(self.sensorData)
        temperatureData = TemperatureData(self.sensorData)
        stepsData = StepsData(self.sensorData)
        stressData = StressData(self.sensorData)
        return [heartrateData, activityData, temperatureData, stepsData, stressData]