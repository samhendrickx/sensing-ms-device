from data import Data
from numpy import mean, max, min, std
from random import randint


class HeartrateData(Data):

    name = "heartrate"

    def getAnalyzed(self):
        data = self.extractData()
        if len(data) > 0:
            return {
                "avg": mean(data),
                "max": max(data),
                "min": min(data),
                "std": std(data)
            }

    def extractData(self):
        if len(self.data["heartrate"]) == 0:
            return [randint(60, 70) for i in range(0, 10)]
        return [el[0] for el in self.data["heartrate"]]
