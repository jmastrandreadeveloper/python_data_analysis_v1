import pandas as pd

def drop_rows_(dataframe, column, valores_a_eliminar) -> pd.DataFrame:
    return dataframe.loc[~dataframe[column].isin(valores_a_eliminar)]