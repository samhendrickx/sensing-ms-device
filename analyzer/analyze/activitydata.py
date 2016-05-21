from data import Data
import matplotlib.pyplot as plt
from numpy import mean
from accelerometerdata import AccelerometerData


class ActivityData(Data):

    name = "activity"
    minutes = 5

    def getAnalyzed(self):
        data = self.extractData()
        #plt.figure()
        #plt.plot(values)
        valuesList = self.divideData(data, self.minutes)
        scores = list()
        for values in valuesList:
            acc = AccelerometerData(values)
            score = acc.getScore()
            scores.append(score)
        score = mean(scores)
        minActive = len([el for el in scores if el > 5])
        # plt.show()
        return {
            "score": score,
            "minActive": minActive
        }

    def extractData(self):
        return [el[0] for el in self.data["accelerometer"]]

    def divideData(self, data, k):
        l = len(data)
        n = int(round(l/k))
        result = [data[i:i+n] for i in xrange(0, l, n)]
        return result