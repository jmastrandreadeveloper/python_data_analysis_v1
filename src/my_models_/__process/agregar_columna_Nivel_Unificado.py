import pandas as pd

def agregar_columna_Nivel_Unificado_(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Crear la columna 'Nivel_Unificado' directamente sin usar .insert(), por simplicidad y claridad.        
    dataframe.loc[:, 'Nivel_Unificado'] = dataframe['Nivel'].replace({
        'Secundario Orientado': 'Secundario', 
        'Secundario Técnico': 'Secundario'
    })
    return dataframe