from data import Data
import matplotlib.pyplot as plt


class ActivityData(Data):

    name = "activity"

    def getAnalyzed(self):
        data = self.extractData()
        for sensor, values in data.items():
            if sensor == "accelerometer":
                print sensor
                print values
                plt.plot(values)
                plt.title(sensor)
        plt.show()

    def extractData(self):
        data = dict()
        data["accelerometer"] = [el[0] for el in self.data["accelerometer"]]
        data["steps"] = [el[0] for el in self.data["steps"]]
        return data