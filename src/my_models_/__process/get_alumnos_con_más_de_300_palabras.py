import pandas as pd

def get_alumnos_con_más_de_300_palabras(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Hacer una copia del DataFrame original para evitar SettingWithCopyWarning
    dataframe = dataframe.copy()
    # Convertir los valores de 'Cantidad_de_palabras' a números, reemplazando los no numéricos con NaN
    dataframe['Cantidad_de_palabras'] = pd.to_numeric(dataframe['Cantidad_de_palabras'], errors='coerce')
    
    # Crear DataFrames separados para valores menores y mayores o iguales a 300
    return dataframe[dataframe['Cantidad_de_palabras'] >= 300].copy()