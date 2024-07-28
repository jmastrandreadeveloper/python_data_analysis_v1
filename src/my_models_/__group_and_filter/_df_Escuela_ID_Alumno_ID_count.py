import pandas as pd

def agrupar_df_Escuela_ID_Alumno_ID_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['Escuela_ID', 'Alumno_ID']
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    if not missing_columns:
        result = dataframe.groupby(['Escuela_ID']).agg({'Alumno_ID': 'count'})
        result.rename(columns={'Alumno_ID': 'Matrícula_por_Escuela_ID',}, inplace=True)
        return result.reset_index()
    else:
        raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {missing_columns}')
    
    
def filtrar_df_Escuela_ID_Alumno_ID_count(Escuela_ID : int, dataframe: pd.DataFrame) -> int:# Filtrar el DataFrame por Escuela_ID
    dFrame_filtrado = dataframe[dataframe['Escuela_ID'] == Escuela_ID]
    
    # Devolver el primer valor de Alumno_ID como entero
    if not dFrame_filtrado.empty:
        return int(dFrame_filtrado['Matrícula_por_Escuela_ID'].values[0])
    else:
        return 0  # o algún valor por defecto que prefieras, si no hay coincidencias
