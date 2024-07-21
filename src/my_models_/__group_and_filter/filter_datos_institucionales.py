import pandas as pd

def filtrar_datos_institucionales( unaEscuela: int, dFrame: pd.DataFrame ) -> dict:
    # Inicializa un diccionario vacío para los datos institucionales.
    diccionario_datos_institucionales = {}

    # Filtra el DataFrame para obtener los datos de la escuela especificada.
    df_filtrado = dFrame[dFrame['Escuela_ID'] == unaEscuela]

    # Verifica si se encontraron datos para la escuela especificada.
    if not df_filtrado.empty:
        # Extrae la primera fila de datos como una Serie (asumiendo que hay una única entrada para cada ID de escuela).
        datos_escuela = df_filtrado.iloc[0]

        # Lista de columnas cuyos datos se incluirán en el diccionario.
        columnas_datos = ['Nivel', 'Nivel_Unificado' , 'Gestión', 'Supervisión', 'Departamento', 'Localidad', 'zona', 'AMBITO', 'Regional']

        # Rellena el diccionario con los datos de las columnas especificadas.
        for columna in columnas_datos:
            # Asegura que la columna existe para evitar errores.
            if columna in df_filtrado.columns:
                diccionario_datos_institucionales[columna] = datos_escuela[columna]
            else:
                print(f"La columna '{columna}' no existe en el DataFrame.")

    else:
        print(f"No se encontraron datos para la escuela con ID '{unaEscuela}'.")

    return diccionario_datos_institucionales