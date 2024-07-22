import pandas as pd

def get_alumnos_incluidos_SI(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[dataframe['Incluido'] == 'Si']