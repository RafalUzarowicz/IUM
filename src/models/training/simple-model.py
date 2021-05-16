from sklearn.tree import DecisionTreeRegressor


class SimpleModel:
    def __init__(self):
        self.model = DecisionTreeRegressor()
        pass

    def train(self, x_train, y_train):
        pass

    def predict(self, x_test):
        pass

    def score(self, x_test, y_test):
        pass

    def __preprocess__(self):
        pass

