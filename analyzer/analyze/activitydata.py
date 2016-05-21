from data import Data
import matplotlib.pyplot as plt


class ActivityData(Data):

    name = "activity"

    def getAnalyzed(self):
        data = self.extractData()
        for sensor, values in data:
            plt.plot(values)
            plt.title(sensor)
        plt.show()

    def extractData(self):
        data = [el[0] for sensor in ["accelerometer", "steps"] for el in self.data[sensor]]
        return data