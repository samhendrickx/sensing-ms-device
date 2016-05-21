from os import listdir, stat
from time import sleep
from analyze.csvreader import CSVReader
from analyze.analyzer import Analyzer


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


if __name__ == "__main__":
    directory = "../device/data/analyze/"
    csvReader = CSVReader(directory)
    analyzer = Analyzer()
    while True:
        if filesAvailable(directory):
            sleep(2)
            csvReader.read()
            analyzer.parseSensorData(csvReader.sensorData)
            csvReader.clear()
        sleep(2)



