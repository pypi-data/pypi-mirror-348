def suggest_imputation(df):
    suggestions = {}
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['int64', 'float64']:
                suggestions[col] = 'mean or median'
            else:
                suggestions[col] = 'mode (most frequent)'
    return suggestions
