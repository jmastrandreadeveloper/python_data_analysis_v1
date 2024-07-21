import pandas as pd

def df_Nivel_Unificado_CURSO_NORMALIZADO_Alumno_ID_count(self):
    required_columns = ['Nivel_Unificado', 'CURSO_NORMALIZADO', 'Alumno_ID']
    missing_columns = [col for col in required_columns if col not in self.processed_dataframe.columns]
    if not missing_columns:
        result = self.processed_dataframe.groupby(['Nivel_Unificado', 'CURSO_NORMALIZADO']).agg({'Alumno_ID': 'count'})
        return result.reset_index()
    else:
        raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {missing_columns}')