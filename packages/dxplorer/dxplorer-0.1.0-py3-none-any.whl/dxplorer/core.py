import pandas as pd

class DataProfiler:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def get_shape(self):
        return self.df.shape

    def get_missing_summary(self):
        missing = self.df.isnull().sum()
        percent = self.df.isnull().mean() * 100
        return pd.DataFrame({
            'Missing Values': missing,
            'Percentage': percent
        })

    def get_data_types(self):
        return self.df.dtypes

    def get_summary_stats(self):
        return self.df.describe(include='all')

    def get_duplicates_count(self):
        return self.df.duplicated().sum()

    def get_unique_values(self):
        return {col: self.df[col].nunique() for col in self.df.columns}

    def generate_basic_report(self):
        return {
            "Shape": self.get_shape(),
            "Missing Summary": self.get_missing_summary(),
            "Data Types": self.get_data_types(),
            "Summary Stats": self.get_summary_stats(),
            "Duplicate Rows": self.get_duplicates_count(),
            "Unique Values per Column": self.get_unique_values()
        }

# ✅ Imputation suggestion utility function
def suggest_imputation(df):
    suggestions = {}
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['int64', 'float64']:
                suggestions[col] = 'mean or median'
            else:
                suggestions[col] = 'mode (most frequent)'
    return suggestions

