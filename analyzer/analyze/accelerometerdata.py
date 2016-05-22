#import matplotlib.pyplot as plt
from numpy import mean

class AccelerometerData(object):

    data = None
    base = None
    thresholds = None

    def __init__(self, data):
        self.base = mean(data)
        self.thresholds = {
            "low": 1000,
            "medium": 3000,
            "high": 5000
        }
        self.data = map(lambda x: abs(x-self.base), data)

    def getScore(self):
        #plt.figure()
        #plt.plot(self.data)
        bottomCount = len([el for el in self.data if el <= self.thresholds["low"]])
        lowCount = len([el for el in self.data if self.thresholds["low"] < el <= self.thresholds["medium"]])
        mediumCount = len([el for el in self.data if self.thresholds["medium"] < el <= self.thresholds["high"]])
        highCount = len([el for el in self.data if self.thresholds["high"] < el])
        bottomRatio = (float(bottomCount) / len(self.data))
        lowRatio = (float(lowCount) / len(self.data))
        mediumRatio = (float(mediumCount) / len(self.data))
        highRatio = (float(highCount) / len(self.data))
        ratio = bottomRatio + lowRatio + mediumRatio + highRatio
        bottomRatio *= 3
        lowRatio *= 5
        mediumRatio *= 7
        highRatio *= 10
        ratio = lowRatio + mediumRatio + highRatio
        #plt.title(ratio)
        #plt.show()
        return ratio
