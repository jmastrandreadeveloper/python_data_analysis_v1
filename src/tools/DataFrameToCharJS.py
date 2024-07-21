import pandas       as pd

df = pd.DataFrame()

def get_valor_label(df,label,nombreColumna):
    # devuelve un valor de un dataframe de un indice especificado
    # por label y de una columna determinada por nombreColumna
    # df.loc[indice, columna]
    return df.at[label , nombreColumna]

def convertir_dataFrame_a_Bar_ChartJS(df):
    # Supongamos que 'df' ya tiene los índices correctos y las columnas representan los grados ("2°", "3°", etc.)
    columnas = list(df.columns)  # Esto obtendrá los grados como labels    
    # Preparar la estructura del resultado
    resultado = {
        "datos_barra": [
            {
                "labels": columnas,
                "datasets": []
            }
        ]
    }
    # Ahora, imaginemos que los índices son las categorías como "Crítico", "Básico", etc.
    indices = list(df.index)    
    # Rellenar los datasets
    for indice in indices:
        dataset = {
            "label": indice,
            "data": []
        }
        for columna in columnas:
            # Suponiendo que puedes acceder directamente al valor deseado con df.loc[indice, columna]
            valor = df.loc[indice, columna]
            #valor = get_valor_label(df,indice,columna)
            dataset["data"].append(valor)
        resultado["datos_barra"][0]["datasets"].append(dataset)
    
    return resultado



def convertir_dataFrame_a_Pie_ChartJS(
        df,
        nombreColumna,
        label):
    ##############################################################################################
    # para convertir un dataframe a formato de Pie de ChartJS necesito:
    # 1-el dataframe debe tener un índice y una sola columna específica de donde sacar los datos
    # 2-tener los labels, por convención ellos estarán en el índice del dataframe
    # 3-un nombre para el Pie,
    # 4-una manera de poder extraer los valores para cada label
    ##############################################################################################
    # extraigo los indices que serán los labels
    labels = []
    data_top = df.head()
    labels = list(data_top.index)
    pieChartDataDict = {}    
    pieChartDataDict = {
        'datos_pie': {
            'labels': labels
        },
        'datasets': [
            {   
                'label' : label,             
                'data': [
                    df.loc[label, nombreColumna] for label in labels
                ]
            }
        ]
    }
    return pieChartDataDict