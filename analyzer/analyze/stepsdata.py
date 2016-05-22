from data import Data


class StepsData(Data):

    name = "steps"

    def getAnalyzed(self):
        data = self.extractData()
        if len(data) > 1:
            first = data[0]
            last = data[-1]
            return last-first
        return 0

    def extractData(self):
        return [el[0] for el in self.data["steps"]]
