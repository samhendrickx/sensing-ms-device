from csvreader import CSVReader
from collections import defaultdict
import datetime as dt

class Analyzer(object):

    csvReader = None

    def __init__(self, directory):
        self.csvReader = CSVReader(directory)

    def analyze(self):
        self.csvReader.read()
        analyzed = defaultdict()

        for data in self.csvReader.getData():
            analyzed[data.name] = data.getAnalyzed()
        i = dt.datetime.now()
        analyzed["datetime"] = i.isoformat()
        self.csvReader.clear()
        return analyzed
