import pandas as pd

def agrupar_df_Escuela_ID_CURSO_NORMALIZADO_list(dataframe: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['Escuela_ID', 'CURSO_NORMALIZADO']
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    
    if not missing_columns:
        result = dataframe.groupby('Escuela_ID')['CURSO_NORMALIZADO'].agg(lambda x: sorted(set(x)))
        result = result.reset_index()  # Resetea el índice para convertir 'Escuela_ID' en una columna
        result.rename(columns={'CURSO_NORMALIZADO': 'Lista_de_cursos_por_Escuela_ID'}, inplace=True)
        return result
    else:
        raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {missing_columns}')    

def filtrar_df_Escuela_ID_CURSO_NORMALIZADO_list(Escuela_ID, dFrame):
    # Filtrar el DataFrame por Escuela_ID
    dFrame_filtrado = dFrame[dFrame['Escuela_ID'] == Escuela_ID]
    
    # Devolver una lista ordenada y sin duplicados de CURSO_NORMALIZADO
    if not dFrame_filtrado.empty:
        # Aplanar la lista de cursos normalizados
        cursos = dFrame_filtrado['Lista_de_cursos_por_Escuela_ID'].explode().tolist()
        # Eliminar duplicados y ordenar la lista
        cursos = sorted(set(cursos))
        return cursos
    else:
        return None  # o algún valor por defecto que prefieras, si no hay coincidencias