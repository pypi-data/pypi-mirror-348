import pandas as pd

def generate_report(df):
    report = []
    report.append("# Data Quality Report\n")
    report.append(f"**Total Rows:** {len(df)}\n")
    report.append(f"**Total Columns:** {len(df.columns)}\n\n")

    report.append("## Missing Values\n")
    missing = df.isnull().sum()
    percent = df.isnull().mean() * 100
    report.append(missing.to_frame("Missing Values").assign(Percentage=percent).to_markdown())

    report.append("\n\n## Data Types\n")
    report.append(df.dtypes.to_frame("Type").to_markdown())

    report.append("\n\n## Basic Stats (Numerical)\n")
    report.append(df.describe().to_markdown())

    return "\n".join(report)
