import pandas       as pd

def convertir_dataFrame_a_Tabla_De_Datos(df):    
    df.reset_index(inplace = True)
    #df = df.reindex(columns=list(df.columns))
    dict_listado = df.to_dict(orient='records')
    return dict_listado