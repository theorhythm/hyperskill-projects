# write your code here
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

f1 = [2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87]
f2 = [65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3]
f3 = [15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2]
y = [24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0]
X = np.array([f1, f2, f3]).T


class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = 0
        self.intercept = 0
        self.res = {}

    def fit(self, X, y):
        # write your code here
        if self.fit_intercept:
            # X = np.array(X).reshape(-1, 1)
            self.X = np.hstack((np.ones((X.shape[0], 1)), X))
            self.y = np.array(y).reshape(-1, 1)
            beta = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.y
            self.intercept = beta[0]
            self.coefficient = beta[1:].flatten()
        else:
            # X = np.array(X).reshape(-1, 1)
            self.X = X
            self.y = np.array(y).reshape(-1, 1)
            beta = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.y
            self.intercept = 0
            self.coefficient = beta.flatten()
        self.res = {'Intercept': float(self.intercept), 'Coefficient': self.coefficient}

    def predict(self, X):
        # write your code here
        if self.fit_intercept:
            X = np.hstack((np.ones((X.shape[0], 1)), X))
            return X @ np.hstack((self.intercept, self.coefficient)).flatten()
        else:
            return X @ self.coefficient

    def r2_score(self, y, yhat):
        # write your code here
        r2_score = 1 - np.sum((y - yhat) ** 2) / np.sum((y - np.mean(y)) ** 2)
        self.res['R2'] = r2_score
        return r2_score

    def rmse(self, y, yhat):
        # write your code here
        rmse = np.sqrt(np.sum((y - yhat) ** 2) / len(y))
        self.res['RMSE'] = rmse
        return rmse


regCustom = CustomLinearRegression(fit_intercept=True)
regCustom.fit(X, y)
cus_y_pred = regCustom.predict(X)
regCustom.r2_score(y, cus_y_pred)
regCustom.rmse(y, cus_y_pred)

reg = LinearRegression(fit_intercept=True).fit(X, y)
y_pred = reg.predict(X)
diff = {}
diff['Intercept'] = reg.intercept_ - regCustom.res['Intercept']
diff['Coefficient'] = reg.coef_ - regCustom.res['Coefficient']
diff['R2'] = r2_score(y, y_pred) - regCustom.res['R2']
diff['RMSE'] = np.sqrt(mean_squared_error(y, y_pred)) - regCustom.res['RMSE']
print(diff)