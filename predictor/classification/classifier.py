from sklearn.tree import DecisionTreeClassifier


class Classifier(object):

    clf = None

    def __init__(self):
        self.clf = DecisionTreeClassifier()

    def train(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)