def obtener_datos_de_columna_(dataframe , nombre_columna, unicos) -> list:
    """
    Esta función extrae los datos de una columna específica de un DataFrame,
    los ordena y los devuelve en forma de lista. Opcionalmente, puede devolver
    solo valores únicos.
    
    Parámetros:
    - df (pandas.DataFrame): El DataFrame del cual se extraerán los datos.
    - nombre_columna (str): El nombre de la columna cuyos datos se desean obtener.
    - unicos (bool): Si es True, la función devolverá solo valores únicos.
    
    Retorna:
    - list: Una lista con los datos de la columna especificada, ordenados. Si
    unicos es True, los datos también serán únicos.
    """
    
    if nombre_columna in dataframe.columns:
        if unicos:
            # Elimina duplicados convirtiendo a set y luego a lista para ordenar
            return sorted(set(dataframe[nombre_columna].tolist()))
        else:
            # Simplemente ordena los valores de la columna
            return sorted(dataframe[nombre_columna].tolist())
    else:
        # Maneja el caso en que la columna no exista en el DataFrame
        print(f"La columna '{nombre_columna}' no existe en el DataFrame.")
        return []