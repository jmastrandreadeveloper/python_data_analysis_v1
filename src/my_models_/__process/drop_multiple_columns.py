import pandas as pd

def drop_multiple_columns_(dataframe: pd.DataFrame , columnas: list, valores_a_eliminar) -> pd.DataFrame:
    # Crear una máscara booleana que indica las filas a conservar
    mascara = pd.Series([True] * len(dataframe))
    for columna in columnas:
        if columna in dataframe.columns:
            mascara &= ~dataframe[columna].isin(valores_a_eliminar)
    return dataframe[mascara]