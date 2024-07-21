import pandas as pd

def quitar_columnas_(dataframe , listaDeColumnasAQuitar, dejarFilasUnicas) -> pd.DataFrame:
    # Quitar las columnas especificadas
    dataframe = dataframe.drop(columns=listaDeColumnasAQuitar)        
    # Dejar filas únicas si se especifica
    if dejarFilasUnicas:
        dataframe = dataframe.drop_duplicates()
    return dataframe