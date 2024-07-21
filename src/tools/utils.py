import os
from PIL import Image
import csv
import pandas       as pd
import csv
import json
import numpy
import sys


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

print('BASE_DIR ' , BASE_DIR)

def create_folder_treeV2(folder_name):
    #sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/my_models_'))
    from src.tools.generatorV2 import generate_concrete_classesV2
    # Directorio de salida para las clases concretas
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_models_')
    generate_concrete_classesV2(output_dir , folder_name)
    return


def create_folder_tree(folder_name):
    #sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/my_models_'))
    from src.tools.generator import generate_concrete_classes
    # Directorio de salida para las clases concretas
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_models_')
    generate_concrete_classes(output_dir , folder_name)    
    return

def imprime(algo):
    print(algo)

def save_dataframe_to_csv(dataframe, filepath):
    try:
        dict = {
            'sep' : ';' ,
            'encoding' : 'UTF-8' , 
            'lineterminator' : '\n'
        }
        dataframe = quitar_retorno_de_columnas(dataframe)
        dataframe.to_csv(
            f'{filepath}',
            sep = dict.get('sep') , encoding = dict.get('encoding') , lineterminator=dict.get('lineterminator'),            
            #quoting=csv.QUOTE_ALL,
            index=False,
            header=True
        )        
    except:
        print('..check nombre de archivo o espacio en disco..!' , f'{filepath}.csv')
    else:
        
        print('..archivo ', filepath ,' grabado..!')
    return

def save_json(diccionario, filepath):
    """
    Función para grabar un diccionario en un archivo JSON.

    :param diccionario: Diccionario a grabar.
    :param nombre_archivo: Nombre del archivo de destino.
    """
    try:
        # Abriendo el archivo en modo escritura.
        with open(filepath, 'w', encoding='utf-8') as archivo:
            # Serializando el diccionario y escribiéndolo en el archivo.
            json.dump(diccionario, archivo, indent=4, ensure_ascii=False, default=default_converter)
        print(f"Archivo '{filepath}' grabado con éxito.")
    except TypeError as e:
        # Manejo de errores si hay algún problema durante la serialización.
        print(f"Error al grabar el archivo: {e}")
    except Exception as e:
        # Manejo de cualquier otro error.
        print(f"Ocurrió un error: {e}")
    
def quitar_retorno_de_columnas(dataframe):
    # Quitar '\r' de los nombres de las columnas
    dataframe.columns = [c.replace('\r', '') for c in dataframe.columns]
    return dataframe

def ensure_dir(directory):
    # Obtiene la ruta absoluta del directorio a crear
    abs_directory = os.path.abspath(directory)
    print(f"Intentando asegurar el directorio: {abs_directory}")

    # Normaliza ambas rutas a minúsculas para evitar problemas de comparación
    normalized_abs_directory = abs_directory.lower()
    normalized_base_dir = BASE_DIR.lower()

    # Verifica que el directorio esté dentro de BASE_DIR
    if not normalized_abs_directory.startswith(normalized_base_dir):
        raise ValueError(f"El directorio {abs_directory} no está dentro de la carpeta base permitida {BASE_DIR}.")

    # Si no existe, crea el directorio
    if not os.path.exists(abs_directory):
        os.makedirs(abs_directory)
        print(f"Directorio creado: {abs_directory}")
    else:
        print(f"El directorio ya existe: {abs_directory}")

def save_image(image, filepath):
    # Asegura que el directorio del archivo exista
    ensure_dir(os.path.dirname(filepath))
    # Guarda la imagen
    image.save(filepath)


#############################################################################

df = pd.DataFrame()

def selectRows(df , columna , rowsList):    
    try:
        selected_rows = df[df[columna].isin(rowsList)]
    except:
        print('..check lista de filas a seleccionar..!')
    else:
        print('..OK filas seleccionadas !')
    return selected_rows

def selectColumns(df , columnsList):    
    try:
        df = df[columnsList]
    except:
        print('..check lista de columnas a seleccionar..!')
    else:
        print('..OK columnas seleccionadas !')
    return df

def insert_data_into_dict(list_dict, key_master, key_path, target_id, new_key, data):
    """
    Este código corrige el problema asegurando que todos los niveles especificados en key_path 
    se creen como diccionarios si no existen. Cuando llegamos al lugar donde queremos insertar 
    new_key y data, ya estamos en el nivel correcto, por lo que simplemente asignamos data a new_key en el current_level.
    key_path debe ser una lista de las claves que llevan al lugar donde quieres insertar el nuevo dato, 
    incluso si el camino es de un solo nivel, key_path debe ser una lista con un solo elemento.
    Inserta un dato dentro de una lista de diccionarios de forma más flexible, permitiendo especificar
    un camino hacia el subnivel deseado.
    
    :param list_dict: Lista con los diccionarios.
    :param key_master: La clave principal en la que queremos buscar.
    :param key_path: Lista de claves que definen el camino hacia el subnivel donde insertar el nuevo dato.
    :param target_id: Es el id que debe coincidir con el valor de key_master para realizar la inserción.
    :param new_key: Es la nueva clave que se va a insertar en el nivel especificado por key_path.
    :param data: Los datos que se van a insertar bajo la clave new_key.
    """
    for item in list_dict:
        if item.get(key_master) == target_id:
            current_level = item
            # Navegar a través del camino especificado por key_path, creando diccionarios si es necesario
            for key in key_path:  # Ahora incluimos todo key_path para navegar correctamente
                if key not in current_level:
                    current_level[key] = {}  # Inicializar como diccionario si la clave no existe
                current_level = current_level[key]
            
            # Asegurarse de que el último paso se maneje correctamente
            # Insertar el nuevo dato directamente sin tratar de acceder primero, ya que estamos en el nivel correcto
            current_level[new_key] = data
            break
    return list_dict

def obtener_data_de_la_lista(list_dict, key_master, target_id, key_path):
    """
    Recupera un dato de cualquier nivel de profundidad dentro de la estructura del diccionario en una lista de diccionarios,
    incluyendo el target_id en el resultado.
    
    :param list_dict: Lista de diccionarios.
    :param key_master: La clave principal en la que queremos buscar.
    :param target_id: Es el id que debe coincidir con el valor de key_master para seleccionar el diccionario.
    :param key_path: Lista de claves que definen el camino hacia el dato deseado.
    :return: Un diccionario que incluye el valor encontrado en el camino especificado bajo la clave 'data',
             y el 'target_id' bajo la clave 'id', o False si no se encuentra.
    """
    for item in list_dict:
        if item.get(key_master) == target_id:
            data = get_data_from_path(item, key_path)
            if data is not False:  # Asegura que el dato fue encontrado antes de incluir el id.
                return {'id': target_id, 'data': data}
    return False

def get_data_from_path(data, key_path):
    """
    Función recursiva para navegar a través de un camino de claves dentro de una estructura anidada.
    
    :param data: El diccionario o subdiccionario actual.
    :param key_path: Lista de claves restantes para navegar.
    :return: El valor encontrado o False si alguna clave no existe.
    """
    if not key_path:  # Si key_path está vacío, hemos llegado al valor deseado
        return data
    key = key_path[0]  # Tomar la primera clave del camino
    if key in data:
        return get_data_from_path(data[key], key_path[1:])  # Recursivamente navegar al siguiente nivel
    else:
        return False  # Si la clave no existe en el nivel actual, retornar False

def default_converter(o):
    if isinstance(o, numpy.int64): return int(o)  
    raise TypeError

# Tu diccionario anidado aquí...
def imprimirDiccionario(diccionario_anidado):
    print(json.dumps(diccionario_anidado, indent=4, ensure_ascii=False, default=default_converter))
    return

def default_converter_2(o):
    """Función de conversión por defecto para tipos no serializables por defecto con JSON."""
    # Aquí puedes añadir lógica personalizada para convertir tipos no serializables.
    # Por ejemplo, si tienes objetos de tipo datetime, podrías convertirlos a string.
    # if isinstance(o, datetime.datetime):
    #     return o.__str__()
    raise TypeError(f'El objeto de tipo {o.__class__.__name__} no es serializable por JSON')

def grabar_diccionario_en_json(diccionario, nombre_archivo):
    """
    Función para grabar un diccionario en un archivo JSON.

    :param diccionario: Diccionario a grabar.
    :param nombre_archivo: Nombre del archivo de destino.
    """
    try:
        # Abriendo el archivo en modo escritura.
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            # Serializando el diccionario y escribiéndolo en el archivo.
            json.dump(diccionario, archivo, indent=4, ensure_ascii=False, default=default_converter)
        print(f"Archivo '{nombre_archivo}' grabado con éxito.")
    except TypeError as e:
        # Manejo de errores si hay algún problema durante la serialización.
        print(f"Error al grabar el archivo: {e}")
    except Exception as e:
        # Manejo de cualquier otro error.
        print(f"Ocurrió un error: {e}")

def obtener_valor(dic, clave):
    """
    Esta función es cuando hemos obtenido el diccionario completo de una escuela en particular y queremos sacar 
    cada uno de los valores mediante su clave
    Busca recursivamente un valor para una clave en un diccionario, incluso dentro de subdiccionarios.
    
    :param dic: El diccionario en el que buscar.
    :param clave: La clave del valor que se busca.
    :return: El valor asociado a la clave, o None si no se encuentra la clave.
    """
    if clave in dic:
        return dic[clave]
    for valor in dic.values():
        if isinstance(valor, dict):
            resultado = obtener_valor(valor, clave)
            if resultado is not None:
                return resultado
    return None

def eliminar_columna(dFrame , listaColumnasAEliminar):
    dFrame = dFrame.drop(columns=listaColumnasAEliminar)
    return dFrame

def getVal(dic, ruta_clave):
    """
    Busca un valor en un diccionario siguiendo una ruta especificada por una cadena de claves separadas por '/'.

    :param dic: El diccionario en el que buscar.
    :param ruta_clave: La ruta de la clave en formato de cadena, separada por '/'.
    :return: El valor asociado a la ruta de la clave, o None si no se encuentra.
    """
    claves = ruta_clave.split('/')
    valor_actual = dic
    try:
        for clave in claves:
            valor_actual = valor_actual[clave]
        return valor_actual
    except KeyError:
        return None


###########################################################################
# FUNCIONES PARA EL TRATAMIENTO DE ESTRUCTURAS DE OBJETOS DESTINADA A LOS #
# AGRUPAMIENTO PARA ER VISUALIZADOS EN LA LIBRERIA ChartJS................#
###########################################################################

def preparar_Datos_Visualizacion_Por_Curso(objeto_fuente, categorias, colores_background):
    """
    Este código define una función preparar_Datos_Visualizacion_Por_Curso que toma 
    tres argumentos: objeto_fuente, categorias, y colores_background. 
    La función está diseñada para preparar datos en un formato específico que se utilizará para la visualización, 
    probablemente en gráficos de barras. Aquí tienes un comentario detallado del código:
    """
    # Extrae los grados (o cursos) del objeto fuente, que es un diccionario,
    # y los usa como las etiquetas para el eje X del gráfico de barras.
    grados = list(objeto_fuente.keys())
    
    # Prepara el diccionario 'datosBarra', que incluye dos claves principales:
    # 'labels', que contiene las etiquetas para el eje X del gráfico (los grados),
    # y 'datasets', que es una lista de diccionarios, cada uno representando una categoría.
    datosBarra = {
        "labels": grados,
        "datasets": [
            # Para cada categoría, crea un diccionario que incluye la etiqueta de la categoría ('label'),
            # los datos asociados a esa categoría para cada grado ('data'), y el color de fondo
            # para esa categoría en el gráfico ('backgroundColor').
            {
                "label": categoria,
                "data": [
                    # Extrae el valor de 'Desempeño' para cada grado y categoría desde el objeto fuente.
                    objeto_fuente[grado][categoria]["Desempeño"] for grado in grados
                ],
                "backgroundColor": colores_background[categoria],  # Asigna el color de fondo.
            } for categoria in categorias  # Esto se repite para cada categoría especificada.
        ]
    }

    # La función retorna un diccionario que contiene una clave 'datosBarra',
    # que a su vez contiene una lista con un único elemento: el diccionario 'datosBarra' preparado.
    return {"datosBarra": [datosBarra]}


def preparar_Datos_Visualizacion_Por_Curso_Division(objeto_fuente, categorias, colores_background):
    """
    Este código define una función preparar_Datos_Visualizacion_Por_Curso_Division que 
    tiene como objetivo preparar datos para su visualización, agrupados por curso y subdivididos por categorías y divisiones. 
    La función toma tres argumentos: objeto_fuente, que es el diccionario 
    de datos fuente; categorias, una lista de categorías a considerar en la visualización; 
    y colores_background, un diccionario que asigna un color a cada categoría para su visualización. 
    A continuación, se explica el código en detalle:
    """    
    # Inicializa un diccionario vacío para almacenar los datos organizados para la visualización.
    objeto_salida = {}

    # Itera sobre cada curso y sus datos asociados en el objeto fuente.
    for curso, datos_curso in objeto_fuente.items():
        # Prepara la estructura básica para los datos de visualización de cada curso,
        # incluyendo etiquetas (divisiones) y conjuntos de datos por categoría.
        datos_barra_curso = {
            "labels": [],  # Lista vacía para almacenar las divisiones.
            "datasets": []  # Lista vacía para almacenar los datos de cada categoría.
        }

        # Itera sobre cada categoría especificada.
        for categoria in categorias:
            # Prepara un diccionario para almacenar los datos de la categoría actual,
            # incluyendo la etiqueta de la categoría, los datos (inicialmente vacíos),
            # y el color de fondo asignado a la categoría.
            dataset_categoria = {
                "label": categoria,
                "data": [],
                "backgroundColor": colores_background[categoria]
            }

            # Itera sobre cada división y sus datos asociados dentro de la categoría actual,
            # para el curso actual. Si la categoría no existe, se utiliza un diccionario vacío.
            for division, datos_division in datos_curso.get(categoria, {}).items():
                # Si la división no está ya en las etiquetas, se añade a la lista de etiquetas.
                if division not in datos_barra_curso["labels"]:
                    datos_barra_curso["labels"].append(division)

                # Añade el dato de desempeño de la división actual a la lista de datos de la categoría.
                dataset_categoria["data"].append(datos_division["Desempeño"])

            # Añade el conjunto de datos de la categoría actual a la lista de conjuntos de datos del curso.
            datos_barra_curso["datasets"].append(dataset_categoria)

        # Asigna los datos de visualización preparados al curso correspondiente en el objeto de salida.
        objeto_salida[curso] = {"datosBarra": [datos_barra_curso]}

    # Retorna el objeto de salida con los datos organizados para su visualización.
    return objeto_salida

def obtener_objeto_anidado(diccionario, ruta_claves):
    """
    Obtiene un objeto anidado de un diccionario dada una ruta de claves.
    
    Parámetros:
    - diccionario: el diccionario del cual obtener el objeto.
    - ruta_claves: una lista de claves que representa la ruta hacia el objeto anidado.
    
    Retorna:
    - El objeto anidado al final de la ruta de claves, o None si alguna clave no existe.
    """
    objeto_actual = diccionario
    for clave in ruta_claves:
        if clave in objeto_actual:
            objeto_actual = objeto_actual[clave]
        else:
            return None  # Retorna None si alguna clave de la ruta no existe
    return objeto_actual

def convertir_dataFrame_a_Diccionario(df):
    dataDict = {}
    return dataDict


def copiar_columna_dataframe_a_otro_dataframe(dFrame , columnaACopiar , nombreDeLaColumnaAsignada):
    new_data_frame = pd.DataFrame(dFrame[columnaACopiar].copy()).rename(columns={columnaACopiar: nombreDeLaColumnaAsignada})
    return new_data_frame


def join_dfs_on_index(dfs, how='inner'):
    """
    Une una lista de DataFrames basándose en sus índices.
    Parámetros:
    - dfs: Lista de DataFrames a unir.
    - how: Cómo unir los DataFrames. Puede ser 'left', 'right', 'outer', 'inner'. 
           Por defecto es 'inner'.
    Retorna:
    - Un DataFrame resultante de unir todos los DataFrames de la lista.

    # Unir los DataFrames
        df_unido = join_dfs_on_index(dfs, how='outer')
    """
    # Verificar que la lista no esté vacía
    if not dfs:
        return pd.DataFrame()  # Retorna un DataFrame vacío si la lista está vacía
    # Inicializar el DataFrame resultado con el primer elemento de la lista
    result_df = dfs[0]
    # Iterar sobre los DataFrames restantes y unirlos uno por uno
    for df in dfs[1:]:
        result_df = result_df.join(df, how=how)
    return result_df

def join_dfs_on_column(dfs, column, how='inner'):
    """
    Une una lista de DataFrames basándose en una columna específica.
    Parámetros:
    - dfs: Lista de DataFrames a unir.
    - column: Nombre de la columna sobre la cual unir los DataFrames.
    - how: Cómo unir los DataFrames. Puede ser 'left', 'right', 'outer', 'inner'.
           Por defecto es 'inner'.
    Retorna:
    - Un DataFrame resultante de unir todos los DataFrames de la lista basándose en la columna especificada.

    # Unir los DataFrames
        df_unido = join_dfs_on_column(dfs, column='Key', how='outer')
    """
    # Verificar que la lista no esté vacía y que la columna exista en todos los DataFrames
    if not dfs or not all(column in df.columns for df in dfs):
        raise ValueError("La lista de DataFrames está vacía o la columna especificada no está en todos los DataFrames")
    # Inicializar el DataFrame resultado con el primer elemento de la lista
    result_df = dfs[0]
    # Iterar sobre los DataFrames restantes y unirlos uno por uno
    for df in dfs[1:]:
        result_df = pd.merge(result_df, df, on=column, how=how)
    return result_df




































































































# import json

# def cargar_json(ruta_archivo):
#     """
#     Carga el contenido de un archivo JSON en un diccionario de Python.

#     Parámetros:
#     - ruta_archivo: la ruta hacia el archivo JSON que se desea cargar.

#     Retorna:
#     - Un diccionario con el contenido del archivo JSON.
#     """
#     try:
#         with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
#             # La siguiente línea convierte el contenido del archivo JSON en un diccionario de Python
#             datos = json.load(archivo)
#             return datos  # Este es un diccionario de Python
#     except FileNotFoundError:
#         print(f"No se encontró el archivo en la ruta especificada: {ruta_archivo}")
#     except json.JSONDecodeError:
#         print(f"Error al decodificar el archivo JSON: {ruta_archivo}")
#     except Exception as e:
#         print(f"Ocurrió un error inesperado: {e}")


# def obtener_objeto_anidado(diccionario, ruta_claves):
#     """
#     Obtiene un objeto anidado de un diccionario dada una ruta de claves.
    
#     Parámetros:
#     - diccionario: el diccionario del cual obtener el objeto.
#     - ruta_claves: una lista de claves que representa la ruta hacia el objeto anidado.
    
#     Retorna:
#     - El objeto anidado al final de la ruta de claves, o None si alguna clave no existe.
#     """
#     objeto_actual = diccionario
#     for clave in ruta_claves:
#         if clave in objeto_actual:
#             objeto_actual = objeto_actual[clave]
#         else:
#             return None  # Retorna None si alguna clave de la ruta no existe
#     return objeto_actual

# def transformar_claves_en_labels(diccionario, ruta_claves):
#     """
#     Dada una ruta de claves, encuentra el objeto especificado y transforma el segundo nivel de claves
#     en una nueva clave llamada "labels", cuyos valores son listas de esas claves.

#     Parámetros:
#     - diccionario: el diccionario que contiene el objeto a transformar.
#     - ruta_claves: una lista de claves que representa la ruta hacia el objeto específico.
    
#     Retorna:
#     - Un nuevo diccionario con la transformación aplicada, o None si la ruta no conduce a un objeto válido.
#     """

#     objeto_especifico = obtener_objeto_anidado(diccionario, ruta_claves[:-1])
#     if objeto_especifico is None or ruta_claves[-1] not in objeto_especifico:
#         print("La ruta de claves no conduce a un objeto válido.")
#         return None
    
#     clave_principal = ruta_claves[-1]
#     objeto_a_transformar = objeto_especifico[clave_principal]
#     nuevo_objeto = {}
    
#     for clave_secundaria, valor in objeto_a_transformar.items():
#         nuevo_objeto[clave_secundaria] = {
#             "labels": list(valor.keys()),
#             **valor  # Esto mantiene los datos originales intactos junto a la nueva clave "labels"
#         }
    
#     # Esta línea reemplaza el objeto original con el transformado en el diccionario principal
#     objeto_especifico[clave_principal] = nuevo_objeto
#     return nuevo_objeto



# def navigate_json(data, key_path):
#     for key in key_path:
#         if isinstance(data, dict) and key in data:
#             data = data[key]
#         else:
#             print(f"No se encontró la clave '{key}' en el camino especificado.")
#             return None
#     return data

# def parse_json(json_file, transformation_rules):
#     data = cargar_json(json_file)
    
#     datos_barra = []
#     for rule_key, rule_values in transformation_rules.items():
#         for rule_value in rule_values:
#             if ".keys" in rule_value:
#                 # Preparar la ruta de claves
#                 key_path_str = rule_value.replace(".keys", "")
#                 key_path = key_path_str.split(".")
                
#                 # Navegar según la ruta de claves
#                 target = navigate_json(data, key_path)
                
#                 # Procesar el objetivo si se encuentra y es un diccionario
#                 if target is not None and isinstance(target, dict):
#                     new_entry = {rule_key: list(target.keys())}
#                     datos_barra.append(new_entry)
#                 else:
#                     print(f"No se pudo encontrar un objeto en la ruta '{key_path_str}' o el objeto no es un diccionario.")
    
#     return {"datosBarra": datos_barra}



# def get_nested_value(d, path):
#     """
#     Obtiene un valor de un diccionario usando una ruta de acceso especificada con puntos.
#     Si la ruta termina con '.keys', devuelve las claves del último diccionario accesible.
#     """
#     keys = path.split(".")
#     for key in keys:
#         if key == "keys":
#             return list(d.keys())  # Devolver las claves si el último elemento de la ruta es 'keys'
#         if key in d:
#             d = d[key]
#         else:
#             return None  # Devolver None si alguna clave no se encuentra
#     return d

# def transform_data(source_json, schema):
#     def get_nested_value(data, path):
#         try:
#             for key in path.split('.'):
#                 if key == 'keys':  # Si 'keys' es el último, devolvemos las claves del diccionario actual
#                     return list(data.keys())
#                 data = data[key]  # Accedemos al siguiente nivel
#             return data
#         except KeyError:
#             return None  # Retorna None si la clave no se encuentra

#     transformed_data = {}
    
#     for key, value in schema.items():
#         if key == "datosBarra":
#             transformed_data[key] = []
#             for item in value:
#                 new_item = {}
#                 for item_key, item_value in item.items():
#                     if isinstance(item_value, list):
#                         # Para 'labels' y 'data', necesitamos manejar listas de rutas
#                         new_item[item_key] = [get_nested_value(source_json, v) for v in item_value]
#                     else:
#                         # Para otros casos, simplemente seguimos el esquema
#                         new_item[item_key] = get_nested_value(source_json, item_value)
#                 transformed_data[key].append(new_item)
#     return transformed_data

# def transform_data_with_labels(source_data, transformation_schema):
#     """Transforma los datos de acuerdo a un esquema de transformación e incluye la lógica para manejar las claves del primer nivel."""
#     result = {"datosBarra": []}
    
#     for item in transformation_schema["datosBarra"]:
#         new_item = {}
#         for key, paths in item.items():
#             if key == "labels":
#                 # Se asume que paths contiene una sola entrada que termina en ".keys"
#                 base_path = paths[0].rstrip(".keys")
#                 # Obtener directamente las claves del primer nivel del objeto deseado
#                 labels = list(get_nested_value(source_data, base_path).keys()) if get_nested_value(source_data, base_path) else []
#                 new_item[key] = labels
#             elif key == "datasets":
#                 new_item[key] = []
#                 for dataset in paths:
#                     new_dataset = {}
#                     for dataset_key, dataset_path in dataset.items():
#                         if dataset_key in ["label", "backgroundColor"]:
#                             new_dataset[dataset_key] = dataset_path
#                         elif dataset_key == "data":
#                             data_values = []
#                             for data_path in dataset_path:
#                                 value = get_nested_value(source_data, data_path)
#                                 if value is not None:
#                                     # Aquí se debería ajustar cómo se extraen los valores según la estructura específica de los datos
#                                     data_values.append(value)
#                             new_dataset[dataset_key] = data_values
#                     new_item[key].append(new_dataset)
#         result["datosBarra"].append(new_item)
    
#     return result



# def read_and_transform_data(json_file_path, schema):
#     with open(json_file_path, 'r', encoding='utf-8') as file:
#         source_json = json.load(file)

#     def get_data_from_path(data, path):
#         keys_requested = ".keys" in path
#         if keys_requested:
#             path = path.replace(".keys", "")  # Removemos el sufijo .keys para obtener el path correcto

#         for part in path.split('.'):
#             if part in data:
#                 data = data[part]
#             else:
#                 return None  # Si no se encuentra el path completo, retornar None
        
#         if keys_requested:
#             return list(data.keys())  # Retornamos las claves si se solicitó .keys
#         else:
#             return data

#     def process_schema(schema, source_json):
#         result = {"datosBarra": []}
#         for item in schema["datosBarra"]:
#             entry = {"labels": [], "datasets": []}
#             for key, value in item.items():
#                 if key == "labels":
#                     # Asumimos que solo hay un path en labels
#                     path = value[0]  # Tomamos el primer y único elemento
#                     labels_data = get_data_from_path(source_json, path)
#                     if labels_data is not None:
#                         entry["labels"] = labels_data
#                 elif key == "datasets":
#                     datasets = []
#                     for dataset in value:
#                         dataset_entry = {}
#                         if 'label' in dataset:
#                             label_data = get_data_from_path(source_json, dataset['label'])
#                             dataset_entry['label'] = label_data if label_data else dataset['label']
#                         if 'data' in dataset:
#                             data_paths = dataset['data']
#                             data_values = [get_data_from_path(source_json, path) for path in data_paths]
#                             dataset_entry['data'] = data_values
#                         if 'backgroundColor' in dataset:
#                             dataset_entry['backgroundColor'] = dataset['backgroundColor']
#                         datasets.append(dataset_entry)
#                     entry['datasets'] = datasets
#             result["datosBarra"].append(entry)
#         return result

#     # Llamada a la función process_schema para procesar el esquema con el JSON de entrada
#     return process_schema(schema, source_json)


# def find_nested_data(source_json, keys_path):
#     """
#     Busca de manera recursiva el objeto especificado por un camino de claves
#     en el JSON anidado. keys_path debe ser una lista de claves.
#     """
#     current_data = source_json
#     for key in keys_path:
#         if isinstance(current_data, dict) and key in current_data:
#             current_data = current_data[key]
#         else:
#             return None
#     return current_data

# def transform_data(json_data, keys_path):
#     """
#     Transforma los datos según el esquema deseado, teniendo en cuenta un camino de claves.
#     """
#     print('---- ' , json_data)
#     target_data = find_nested_data(json_data, keys_path)
    
#     if target_data is None:
#         return {"error": f"{'.'.join(keys_path)} no encontrado."}
    
#     # Aquí procedes con la transformación de los datos encontrados.
#     # Por ejemplo, generar 'labels' basado en las claves del primer nivel de 'target_data'.
#     labels = list(target_data.keys())
    
#     # Aquí continúas con la transformación según necesites.
#     # Este es solo un ejemplo basado en tu solicitud anterior.
#     result = {
#         "datosBarra": [
#             {
#                 "labels": labels,
#                 # Añade aquí la transformación para 'datasets' u otros datos necesarios.
#             }
#         ]
#     }
    
#     return result

