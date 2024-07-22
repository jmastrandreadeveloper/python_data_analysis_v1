import pandas as pd

def get_alumnos_sin_DESEMPEÑO(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[dataframe['DESEMPEÑO'] == '-']