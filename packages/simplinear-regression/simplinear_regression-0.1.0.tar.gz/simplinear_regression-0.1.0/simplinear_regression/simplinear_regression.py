class simplinear_regression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def _check_X_format(self, X):
        if len(X) > 0 and not isinstance(X[0], list):
            X = [[x] for x in X]
        return X

    def mean(self, values):
        return sum(values) / len(values)

    def variance(self, values, mean_val):
        total = 0
        for x in values:
            total += (x - mean_val) ** 2
        return total

    def covariance(self, x, mean_x, y, mean_y):
        total = 0
        for i in range(len(x)):
            total += (x[i] - mean_x) * (y[i] - mean_y)
        return total

    def fit(self, X, y):
        X = self._check_X_format(X)
        flat_X = [item[0] for item in X]

        mean_x = self.mean(flat_X)
        mean_y = self.mean(y)

        cov = self.covariance(flat_X, mean_x, y, mean_y)
        var = self.variance(flat_X, mean_x)

        self.slope = cov / var
        self.intercept = mean_y - self.slope * mean_x

    def predict(self, X):
        X = self._check_X_format(X)
        flat_X = [item[0] for item in X]

        predictions = []
        for x in flat_X:
            y = self.intercept + self.slope * x
            predictions.append(y)

        return predictions