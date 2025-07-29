
"""
DataQualityChecker: A simple Python package for data profiling,
missing value detection, outlier identification, and imputation suggestions.
"""

from .core import DataProfiler
from .report import generate_report
from .visualizer import visualize_missing_data, visualize_outliers

__all__ = [
    'DataProfiler',
    'generate_report',
    'visualize_missing_data',
    'visualize_outliers',
]

__version__ = '0.1.0'
