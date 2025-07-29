import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_missing_heatmap(df):
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title("Missing Values Heatmap")
    plt.show()

def plot_distributions(df):
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribution of {col}")
        plt.show()
