from data import Data


class StepsData(Data):

    name = "steps"

    def getAnalyzed(self):
        if len(self.data) > 0:
            first = self.data[0]
            last = self.data[-1]
            return last-first
