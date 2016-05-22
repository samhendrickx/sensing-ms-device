from data import Data
from numpy import mean


class StressData(Data):

    name = "stress"

    def getAnalyzed(self):
        data = self.extractData()
        if len(data) > 1:
            heartrate = mean(data)
            minHeartrate = 60
            maxHeartrate = 120
            heartrate = minHeartrate if heartrate < minHeartrate else heartrate
            heartrate = maxHeartrate if heartrate > maxHeartrate else heartrate
            heartrate -= minHeartrate
            heartrate /= maxHeartrate - minHeartrate
            heartrate *= 10
            return heartrate
        return 5

    def extractData(self):
        return [el[0] for el in self.data["heartrate"]]
