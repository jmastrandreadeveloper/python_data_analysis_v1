import pandas as pd

def calcular_desempeño(dataframe,listaDeColumnas, dF_dataFrameIzquierdo, dF_dataFrameDerecha, ColumnaY, ColumnaX, col_titulo):    
    # Esta función calcula los porcentajes de desempeños de acuerdo a las columnas que se les pasa por parámetros.
    # La idea es que se puedan determinar por escuela, por curso, por división, etc., manteniendo la referencia de Alumno_ID
    # y renombrando las columnas de acuerdo a los parámetros suministrados.    
    # Realizando la fusión de los dataframes.
    dF_desempeño = pd.DataFrame()
    dF_desempeño = pd.merge(dF_dataFrameIzquierdo, dF_dataFrameDerecha, how="left", on=listaDeColumnas)    
    # Renombrando las columnas 'Alumno_ID_x' y 'Alumno_ID_y' según los parámetros suministrados, asumiendo que ambas columnas contienen los mismos valores.
    # Esto implica que se puede mantener solo una de estas columnas para evitar duplicados.
    dF_desempeño.rename(columns={'Alumno_ID_x': ColumnaX, 'Alumno_ID_y': ColumnaY}, inplace=True)
    # Calculando el porcentaje de desempeño.
    dF_desempeño[col_titulo] = dF_desempeño[ColumnaY] / dF_desempeño[ColumnaX] * 100    
    # Opcional: Si se desea eliminar una de las columnas de Alumno_ID para evitar redundancia, puedes descomentar la siguiente línea:
    # dF_desempeño.drop(columns=[ColumnaY], inplace=True)
    return dF_desempeño