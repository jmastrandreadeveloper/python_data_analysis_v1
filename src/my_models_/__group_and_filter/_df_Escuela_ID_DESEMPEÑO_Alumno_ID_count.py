import pandas as pd

def agrupar_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count(dataframe: pd.DataFrame):
    required_columns = ['Escuela_ID', 'DESEMPEÑO', 'Alumno_ID']
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    if not missing_columns:
        result = dataframe.groupby(['Escuela_ID', 'DESEMPEÑO']).agg({'Alumno_ID': 'count'})
        return result.reset_index()
    else:
        raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {missing_columns}')
    
def filtrar_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count(unaEscuela , dFrame):
    desempeño_por_escuela_df = pd.DataFrame()
    total_alumnos_por_escuela_df = pd.DataFrame()
    # Filtrado del DataFrame para obtener los datos correspondientes a la escuela dada.
    df = dFrame[dFrame['Escuela_ID'] == unaEscuela]
    # Asumiendo que la estructura de desempeno_df ya es adecuada para el análisis, con las columnas necesarias.
    # Establecer 'DESEMPEÑO' como índice para trabajar con él más fácilmente.
    df.set_index('DESEMPEÑO', inplace=True)
    # Asegurarse de que todos los niveles de desempeño están representados, incluso si no hay datos para algunos.
    df = df.reindex(['Crítico', 'Básico', 'Medio', 'Avanzado'])
    # Rellenar los valores faltantes en las columnas relevantes para asegurar que todos los niveles de desempeño tienen un valor.
    # AL HACER ESTO NO NECESITO FILTRAR DADO QUE CREO UN NUEVO DATAFRAME CON LA COLUMNA DE INTERÉS
    desempeño_por_escuela_df['Desempeño_por_Escuela'] = df['Desempeño_por_Escuela'].fillna(0)
    total_alumnos_por_escuela_df['Total_Alumnos_por_Tipo_de_Desempeño'] = df['Total_Alumnos_por_Tipo_de_Desempeño'].fillna(0)    
    # # Devolución de dos dataframe con el desempeño y el total de alumnos
    return desempeño_por_escuela_df , total_alumnos_por_escuela_df