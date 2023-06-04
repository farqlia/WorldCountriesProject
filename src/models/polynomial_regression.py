import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class PolyRegression:

    def __init__(self, degree):
        self.degree = degree 
        self.poly_pipeline = make_pipeline(
            SimpleImputer(missing_values=np.nan, strategy='mean'),
            PolynomialFeatures(degree=degree, include_bias=False),
            StandardScaler())
        self.poly_reg = None   

    def fit(self, X, y):
        self.poly_reg = LinearRegression()
        X_transformed = self.poly_pipeline.fit_transform(X)
        self.poly_reg.fit(X_transformed, y)
        self.coef_ = self.poly_reg.coef_
        self.intercept_ = self.poly_reg.intercept_
        
    def predict(self, X):
        X_transformed = self.poly_pipeline.transform(X)
        return self.poly_reg.predict(X_transformed)
    
    def score(self, X, y):
        X_transformed = self.poly_pipeline.transform(X)
        return self.poly_reg.score(X_transformed, y)