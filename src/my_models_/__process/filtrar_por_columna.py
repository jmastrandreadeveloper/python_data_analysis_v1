import pandas as pd

def filtrar_por_columna_(dataframe,columna,condición) -> pd.DataFrame:
    return dataframe[dataframe[columna] == condición]