import pandas as pd

def get_alumnos_con_DESEMPEÑO(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[dataframe['DESEMPEÑO'] != '-']