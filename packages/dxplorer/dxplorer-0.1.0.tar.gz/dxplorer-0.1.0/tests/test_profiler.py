import pandas as pd
from dqxplorer.profiler import DataProfiler

def test_missing_check():
    df = pd.DataFrame({'A': [1, None, 3], 'B': [4, 5, None]})
    profiler = DataProfiler(df)
    assert profiler.check_missing().sum() == 2
