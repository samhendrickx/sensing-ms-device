from csvreader import CSVReader
from collections import defaultdict


class Analyzer(object):

    csvReader = None

    def __init__(self, directory):
        self.csvReader = CSVReader(directory)

    def analyze(self):
        self.csvReader.read()
        analyzed = defaultdict()
        for data in self.csvReader.getData():
            analyzed[data.name] = data.getAnalyzed()
        self.csvReader.clear()
        return analyzed
