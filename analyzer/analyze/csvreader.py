import csv
from os import listdir, remove
from collections import defaultdict


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
                dataList = [row for row in reader if row != []]
                self.sensorData[sensor] = dataList

    def clear(self):
        '''self.sensorData = None
        fileNames = listdir(self.directory)
        for fileName in fileNames:
            path = str(self.directory) + str(fileName)
            remove(path)'''
        pass
