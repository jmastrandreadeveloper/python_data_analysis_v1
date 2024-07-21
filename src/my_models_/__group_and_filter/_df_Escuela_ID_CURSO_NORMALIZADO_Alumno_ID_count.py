import pandas as pd

def agrupar_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count(dataframe) -> pd.DataFrame:
    required_columns = ['Escuela_ID', 'CURSO_NORMALIZADO', 'Alumno_ID']
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    if not missing_columns:
        result = dataframe.groupby(['Escuela_ID', 'CURSO_NORMALIZADO']).agg({'Alumno_ID': 'count'})
        result = result.reset_index()
        result.rename(columns={'Alumno_ID': 'Matrícula', 'CURSO_NORMALIZADO': 'Curso'}, inplace=True)
        return result
    else:
        raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {missing_columns}')

def filtrar_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count(Escuela_ID : int , dFrame: pd.DataFrame) -> pd.DataFrame:     
    # Reset index para poder filtrar por 'Escuela_ID'
    agrupado_reset = dFrame.reset_index()
    # Filtramos por una 'Escuela_ID' específica
    dFrame_filtrado = agrupado_reset[agrupado_reset['Escuela_ID'] == Escuela_ID]
    # filtramos las columnas que necesitamos
    dFrame_filtrado = dFrame_filtrado.filter(['Curso', 'Matrícula'])
    dFrame_filtrado.set_index('Curso', inplace=True)
    
    # convertir el dataframe para que sea una tabla
    dFrame_filtrado.reset_index(inplace = True)        
    dict_listado = dFrame_filtrado.to_dict(orient='records')    
    
    return dict_listado