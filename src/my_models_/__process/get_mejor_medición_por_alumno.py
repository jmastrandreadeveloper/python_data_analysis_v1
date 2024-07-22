import pandas as pd

def get_mejor_medición_por_alumno(dataframe: pd.DataFrame) -> pd.DataFrame:        
    def convert_to_int_or_str(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return '-'
    #############################################################################################################    
    df_new = dataframe.sort_values('Cantidad_de_palabras', ascending=False).drop_duplicates(['Alumno_ID']).sort_index()

    for col in ['Cantidad_de_palabras', 'Prosodia']:
        df_new[col] = pd.to_numeric(df_new[col], errors='coerce').fillna('-').apply(convert_to_int_or_str)

    df_filtered = df_new[df_new['Cantidad_de_palabras'].apply(lambda x: isinstance(x, int) and x < 300 or x == '-')]
    df_mejores_mediciones = df_filtered.sort_values(by='Cantidad_de_palabras', ascending=False).drop_duplicates(subset=['Alumno_ID'])

    return df_mejores_mediciones