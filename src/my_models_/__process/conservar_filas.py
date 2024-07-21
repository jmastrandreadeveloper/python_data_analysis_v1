import pandas as pd

def conservar_filas_(dataframe: pd.DataFrame , columna: str, valores_a_conservar: list) -> pd.DataFrame:
    # Verificar que la columna especificada exista en el DataFrame
    if columna not in dataframe.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")
    
    # Verificar que la lista de valores a conservar no esté vacía
    if not valores_a_conservar:
        raise ValueError("La lista de valores a conservar no puede estar vacía.")
    
    # Crear una máscara booleana que indica las filas a conservar
    mascara = dataframe[columna].isin(valores_a_conservar)
    
    # Verificar que hay filas que cumplen con la condición
    if not mascara.any():
        raise ValueError("Ninguna fila cumple con los valores especificados para conservar.")
    
    return dataframe[mascara]