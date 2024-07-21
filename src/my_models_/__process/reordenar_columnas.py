import pandas as pd

def reordenar_columnas_(dataframe , listaDeColumnas) -> pd.DataFrame:
    return dataframe[listaDeColumnas]