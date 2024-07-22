import pandas as pd

def clean_dataframe(dataframe: pd.DataFrame, int_columns: list, float_columns: list) -> pd.DataFrame:
    for col in int_columns:
        dataframe[col] = dataframe[col].astype(int).round(0).fillna(0)
    for col in float_columns:
        dataframe[col] = dataframe[col].round(2).fillna(0)
        
    return dataframe