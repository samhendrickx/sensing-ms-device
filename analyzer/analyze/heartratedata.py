from data import Data
from numpy import mean, max, min, std


class HeartrateData(Data):

    name = "heartrate"

    def getAnalyzed(self):
        if len(self.data) > 0:
            return {
                "avg": mean(self.data),
                "max": max(self.data),
                "min": min(self.data),
                "std": std(self.data)
            }
