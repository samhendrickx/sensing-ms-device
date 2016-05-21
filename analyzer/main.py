from os import listdir, stat
from time import sleep
from analyze.csvreader import CSVReader
from analyze.analyzer import Analyzer
from collections import defaultdict


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
    analyzer = Analyzer(directory)
    while True:
        if filesAvailable(directory):
            #sleep(2)
            analyzedDict = analyzer.analyze()
        sleep(2)



