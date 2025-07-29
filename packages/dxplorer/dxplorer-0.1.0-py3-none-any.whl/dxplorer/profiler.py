import pandas as pd

class DataProfiler:
    def __init__(self, df):
        self.df = df

    def check_missing(self):
        return self.df.isnull().sum().sort_values(ascending=False)

    def check_duplicates(self):
        return self.df[self.df.duplicated()]

    def check_types(self):
        return self.df.dtypes

    def check_variance(self, threshold=0.01):
        return self.df.var()[self.df.var() < threshold]

    def check_skewness(self, threshold=1):
        return self.df.skew()[abs(self.df.skew()) > threshold]
