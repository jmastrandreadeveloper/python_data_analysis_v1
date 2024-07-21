import pandas as pd

def agrupar_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['Escuela_ID', 'CURSO_NORMALIZADO', 'División', 'Alumno_ID']
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    if not missing_columns:
        result = dataframe.groupby(['Escuela_ID', 'CURSO_NORMALIZADO', 'División']).agg({'Alumno_ID': 'count'})
        result = result.reset_index()
        result.rename(columns={'Alumno_ID': 'Matrícula', 'CURSO_NORMALIZADO': 'Curso'}, inplace=True)
        return result
    else:
        raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {missing_columns}')
    
def filtrar_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count(Escuela_ID: int ,dFrame: pd.DataFrame,  lista_de_cursos: list) -> dict:
    dict_matricula_por_curso_division = {}
    
    # Aseguramos que 'Escuela_ID' sea accesible como columna, reseteando el índice si es necesario
    if 'Escuela_ID' not in dFrame.columns:
        dFrame = dFrame.reset_index()
    
    for CURSO_NORMALIZADO in lista_de_cursos:
        # Filtramos por 'Escuela_ID' específica y un Curso específico
        dFrame_filtrado = dFrame[
            (dFrame['Escuela_ID'] == Escuela_ID) &
            (dFrame['Curso'] == CURSO_NORMALIZADO)
        ]
        
        # Cambiamos nombres de columnas        
        df_matricula_por_curso_division = dFrame_filtrado[['Curso', 'División', 'Matrícula']].reset_index(drop=True)
        df_matricula_por_curso_division.set_index('Curso', inplace=True)

        # convertir el dataframe de cada curso en una lista para que sea una tabla
        df_matricula_por_curso_division.reset_index(inplace = True)        
        dict_listado = df_matricula_por_curso_division.to_dict(orient='records')

        dict_matricula_por_curso_division[CURSO_NORMALIZADO] = dict_listado
    
    return dict_matricula_por_curso_division