import pandas as pd

def data_frame_to_diccionario(df):
    dict = df.to_dict(orient='dict')
    return dict