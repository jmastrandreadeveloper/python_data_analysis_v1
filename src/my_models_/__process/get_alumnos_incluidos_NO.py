import pandas as pd

def get_alumnos_incluidos_NO(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[dataframe['Incluido'] == 'No']