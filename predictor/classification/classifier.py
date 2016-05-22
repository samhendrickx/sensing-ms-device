from sklearn.tree import DecisionTreeClassifier
from numpy import matrix


class Classifier(object):

    clf = None

    def __init__(self):
        self.clf = DecisionTreeClassifier()

    def train(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)

    def getRules(self, feature_names):
        left = self.clf.tree_.children_left
        right = self.clf.tree_.children_right
        threshold = self.clf.tree_.threshold
        features = [feature_names[i] for i in self.clf.tree_.feature]
        value = self.clf.tree_.value

        def getTabs(tabs):
            result = ""
            for i in range(0, tabs):
                result += "     "
            return result

        def recurse(left, right, threshold, features, node, previousS="", tab=0):
            if (threshold[node] != -2):
                previousS += getTabs(tab)
                previousS += "if ( " + features[node] + " <= " + str(threshold[node]) + " ) {\n"
                if left[node] != -1:
                    previousS = recurse(left, right, threshold, features, left[node], previousS, tab+1)
                previousS += getTabs(tab)
                previousS += "} else {\n"
                if right[node] != -1:
                    previousS = recurse(left, right, threshold, features, right[node], previousS, tab+1)
                previousS += getTabs(tab)
                previousS += "}\n"
            else:
                previousS += getTabs(tab)
                previousS += "return " + str(value[node]) +"\n"
            return previousS

        return recurse(left, right, threshold, features, 0)

    def getDangerousRules(self, featureNames):
        value = self.clf.tree_.value
        dangerousNodes = self.getDangerousNodes()
        rules = list()
        features = [featureNames[i] for i in self.clf.tree_.feature]
        threshold = self.clf.tree_.threshold
        left = list(self.clf.tree_.children_left)
        right = list(self.clf.tree_.children_right)
        for node in dangerousNodes:
            print value[node]
            path = self.getPathToNode(node)
            path.reverse()
            node = 0
            rule = list()
            for direction in path:
                if direction == "left":
                    rule.append(str(features[node])+" <= "+str(threshold[node]))
                    node = left[node]
                elif direction == "right":
                    rule.append(str(features[node]) + " > " + str(threshold[node]))
                    node = right[node]
            rules.append(rule)
        return rules

    def getPathToNode(self, node):
        if node == 0:
            return []
        left = list(self.clf.tree_.children_left)
        right = list(self.clf.tree_.children_right)
        if node in left:
            index = left.index(node)
            return ["left"]+self.getPathToNode(index)
        else:
            index = right.index(node)
            return ["right"]+self.getPathToNode(index)

    def getDangerousNodes(self):
        dangerous = list()
        leaves = self.getLeaves()
        value = self.clf.tree_.value
        for leaf in leaves:
            result = value[leaf]
            result = result[0]
            maxValue = 0
            maxIndex = 0
            for index2, el in enumerate(result):
                if el > maxValue:
                    maxValue = el
                    maxIndex = index2
            if maxIndex < 2:
                dangerous.append(leaf)
        return dangerous

    def getLeaves(self):
        left = list(self.clf.tree_.children_left)
        right = list(self.clf.tree_.children_right)
        l = max(len(left), len(right))
        leaves = list()
        for i in range(0, l):
            leftNode = left[i] if i < len(left) else -1
            rightNode = right[i] if i < len(right) else -1
            if leftNode == -1 and rightNode == -1:
                leaves.append(i)
        return leaves