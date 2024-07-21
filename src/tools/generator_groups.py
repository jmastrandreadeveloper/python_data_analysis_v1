import os
import pandas as pd
import re

# Función para leer el contenido de un archivo existente
def leer_archivo(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# Función para extraer los métodos existentes de la clase
def extraer_metodos_existentes(contenido_clase):
    if contenido_clase:
        metodos = re.findall(r"def (\w+)\(self.*\):", contenido_clase)
        return set(metodos)
    return set()

# Función para actualizar el archivo __init__.py
def actualizar_init_py(concrete_models_path, class_name):
    init_file = os.path.join(concrete_models_path, '__init__.py')
    contenido_init = leer_archivo(init_file)

    import_statement = f"from .{class_name} import {class_name}"

    # Inicializar o actualizar el contenido de __init__.py
    if contenido_init:
        # Asegurarse de que la declaración de importación esté al principio
        if import_statement not in contenido_init:
            contenido_init = f"{import_statement}\n" + contenido_init
    else:
        contenido_init = f"{import_statement}\n"

    # Manejar la variable __all__
    all_pattern = re.compile(r"__all__\s*=\s*\[(.*?)\]", re.DOTALL)
    match = all_pattern.search(contenido_init)
    if match:
        all_content = match.group(1)
        all_items = re.findall(r"'(.*?)'", all_content)
        if class_name not in all_items:
            all_items.append(class_name)
            new_all_content = ', '.join(f"'{item}'" for item in all_items)
            contenido_init = all_pattern.sub(f"__all__ = [{new_all_content}]", contenido_init)
    else:
        contenido_init += f"\n__all__ = ['{class_name}']\n"

    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(contenido_init)

    print(f"Archivo __init__.py actualizado exitosamente en {init_file}")

# Función para generar una nueva clase con métodos de agrupamiento
def generate_group_aggregation_class(group_params_list, output_dir, class_name):
    concrete_models_path = output_dir
    os.makedirs(concrete_models_path, exist_ok=True)

    class_file = os.path.join(concrete_models_path, f'{class_name}.py')
    contenido_existente = leer_archivo(class_file)
    metodos_existentes = extraer_metodos_existentes(contenido_existente)

    class_content = ""
    if contenido_existente:
        class_content += contenido_existente
        if not class_content.endswith("\n"):
            class_content += "\n"
    else:
        class_content += "import pandas as pd\n\n"
        class_content += f"class {class_name}:\n"
        class_content += "    def __init__(self, dataframe: pd.DataFrame):\n"
        class_content += "        self.dataframe = dataframe\n\n"

    for columns, agg_dict, options in group_params_list:
        method_name = generate_method_name(columns, agg_dict)
        if method_name not in metodos_existentes:
            method_content = generate_group_method_content(columns, agg_dict, options)
            class_content += method_content

    with open(class_file, 'w', encoding='utf-8') as f:
        f.write(class_content)

    print(f"Clase {class_name} generada exitosamente en {class_file}")

    # Actualizar el archivo __init__.py
    actualizar_init_py(concrete_models_path, class_name)

# Función para generar nombres de método basados en columnas y funciones de agregación
def generate_method_name(columns, agg_dict):
    column_str = "_".join(columns)
    agg_str = "_".join([f"{col}_{func}" for col, func in agg_dict.items()])
    return f"df_{column_str}_{agg_str}"

# Función para generar el contenido del método de agrupamiento
def generate_group_method_content(columns, agg_dict, options):
    method_name = generate_method_name(columns, agg_dict)
    
    method_content = f"    def {method_name}(self):\n"
    method_content += f"        required_columns = {columns + list(agg_dict.keys())}\n"
    method_content += f"        missing_columns = [col for col in required_columns if col not in self.dataframe.columns]\n"
    method_content += f"        if not missing_columns:\n"
    method_content += f"            result = self.dataframe.groupby({columns}).agg({agg_dict})\n"
    
    if 'reset_index' in options and options['reset_index']:
        method_content += f"            return result.reset_index()\n"
    else:
        method_content += f"            return result\n"
    
    method_content += f"        else:\n"
    method_content += f"            raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {{missing_columns}}')\n\n"

    return method_content


"""
import os
import pandas as pd
import re

# Función para leer el contenido de un archivo existente
def leer_archivo(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# Función para extraer los métodos existentes de la clase
def extraer_metodos_existentes(contenido_clase):
    if contenido_clase:
        metodos = re.findall(r"def (\w+)\(self.*\):", contenido_clase)
        return set(metodos)
    return set()

# Función para actualizar el archivo __init__.py
def actualizar_init_py(concrete_models_path):
    init_file = os.path.join(concrete_models_path, '__init__.py')
    contenido_init = leer_archivo(init_file)

    import_statement = "from .GroupAggregation import GroupAggregation"

    # Inicializar o actualizar el contenido de __init__.py
    if contenido_init:
        # Asegurarse de que la declaración de importación esté al principio
        if import_statement not in contenido_init:
            contenido_init = f"{import_statement}\n" + contenido_init
    else:
        contenido_init = f"{import_statement}\n"

    # Manejar la variable __all__
    all_pattern = re.compile(r"__all__\s*=\s*\[(.*?)\]", re.DOTALL)
    match = all_pattern.search(contenido_init)
    if match:
        all_content = match.group(1)
        all_items = re.findall(r"'(.*?)'", all_content)
        if 'GroupAggregation' not in all_items:
            all_items.append('GroupAggregation')
            new_all_content = ', '.join(f"'{item}'" for item in all_items)
            contenido_init = all_pattern.sub(f"__all__ = [{new_all_content}]", contenido_init)
    else:
        contenido_init += "\n__all__ = ['GroupAggregation']\n"

    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(contenido_init)

    print(f"Archivo __init__.py actualizado exitosamente en {init_file}")

# Función para generar una nueva clase GroupAggregation con métodos de agrupamiento
def generate_group_aggregation_class(group_params_list, output_dir):
    concrete_models_path = output_dir
    os.makedirs(concrete_models_path, exist_ok=True)

    group_aggregation_file = os.path.join(concrete_models_path, 'GroupAggregation.py')
    contenido_existente = leer_archivo(group_aggregation_file)
    metodos_existentes = extraer_metodos_existentes(contenido_existente)

    class_content = ""
    if contenido_existente:
        class_content += contenido_existente
        if not class_content.endswith("\n"):
            class_content += "\n"
    else:
        class_content += "import pandas as pd\n\n"
        class_content += "class GroupAggregation:\n"
        class_content += "    def __init__(self, dataframe: pd.DataFrame):\n"
        class_content += "        self.dataframe = dataframe\n\n"

    for columns, agg_dict, options in group_params_list:
        method_name = generate_method_name(columns, agg_dict)
        if method_name not in metodos_existentes:
            method_content = generate_group_method_content(columns, agg_dict, options)
            class_content += method_content

    with open(group_aggregation_file, 'w', encoding='utf-8') as f:
        f.write(class_content)

    print(f"Clase GroupAggregation generada exitosamente en {group_aggregation_file}")

    # Actualizar el archivo __init__.py
    actualizar_init_py(concrete_models_path)

# Función para generar nombres de método basados en columnas y funciones de agregación
def generate_method_name(columns, agg_dict):
    column_str = "_".join(columns)
    agg_str = "_".join([f"{col}_{func}" for col, func in agg_dict.items()])
    return f"df_{column_str}_{agg_str}"

# Función para generar el contenido del método de agrupamiento
def generate_group_method_content(columns, agg_dict, options):
    method_name = generate_method_name(columns, agg_dict)
    
    method_content = f"    def {method_name}(self):\n"
    method_content += f"        required_columns = {columns + list(agg_dict.keys())}\n"
    method_content += f"        missing_columns = [col for col in required_columns if col not in self.dataframe.columns]\n"
    method_content += f"        if not missing_columns:\n"
    method_content += f"            result = self.dataframe.groupby({columns}).agg({agg_dict})\n"
    
    if 'reset_index' in options and options['reset_index']:
        method_content += f"            return result.reset_index()\n"
    else:
        method_content += f"            return result\n"
    
    method_content += f"        else:\n"
    method_content += f"            raise ValueError(f'Las columnas especificadas no existen en el dataframe. Columnas faltantes: {{missing_columns}}')\n\n"

    return method_content
""""""
"""
"""
import os
import pandas as pd
import re

# Función para leer el contenido de un archivo existente
def leer_archivo(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# Función para extraer los métodos existentes de la clase
def extraer_metodos_existentes(contenido_clase):
    if contenido_clase:
        metodos = re.findall(r"def (\w+)\(self.*\):", contenido_clase)
        return set(metodos)
    return set()

# Función para actualizar el archivo __init__.py
def actualizar_init_py(concrete_models_path):
    init_file = os.path.join(concrete_models_path, '__init__.py')
    contenido_init = leer_archivo(init_file)

    import_statement = "from .GroupData import GroupData"

    # Inicializar o actualizar el contenido de __init__.py
    if contenido_init:
        # Asegurarse de que la declaración de importación esté al principio
        if import_statement not in contenido_init:
            contenido_init = f"{import_statement}\n" + contenido_init
    else:
        contenido_init = f"{import_statement}\n"

    # Manejar la variable __all__
    all_pattern = re.compile(r"__all__\s*=\s*\[(.*?)\]", re.DOTALL)
    match = all_pattern.search(contenido_init)
    if match:
        all_content = match.group(1)
        all_items = re.findall(r"'(.*?)'", all_content)
        if 'GroupData' not in all_items:
            all_items.append('GroupData')
            new_all_content = ', '.join(f"'{item}'" for item in all_items)
            contenido_init = all_pattern.sub(f"__all__ = [{new_all_content}]", contenido_init)
    else:
        contenido_init += "\n__all__ = ['GroupData']\n"

    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(contenido_init)

    print(f"Archivo __init__.py actualizado exitosamente en {init_file}")

# Función para generar una nueva clase GroupData con métodos de agrupamiento
def generate_group_data_class(group_params_list, output_dir):
    concrete_models_path = output_dir
    os.makedirs(concrete_models_path, exist_ok=True)

    group_data_file = os.path.join(concrete_models_path, 'GroupData.py')
    contenido_existente = leer_archivo(group_data_file)
    metodos_existentes = extraer_metodos_existentes(contenido_existente)

    class_content = ""
    if contenido_existente:
        class_content += contenido_existente
        if not class_content.endswith("\n"):
            class_content += "\n"
    else:
        class_content += "import pandas as pd\n\n"
        class_content += "class GroupData:\n"
        class_content += "    def __init__(self, dataframe: pd.DataFrame):\n"
        class_content += "        self.dataframe = dataframe\n\n"

    for columns, agg_dict, options in group_params_list:
        method_name = generate_method_name(columns, agg_dict)
        if method_name not in metodos_existentes:
            method_content = generate_group_method_content(columns, agg_dict, options)
            class_content += method_content

    with open(group_data_file, 'w', encoding='utf-8') as f:
        f.write(class_content)

    print(f"Clase GroupData generada exitosamente en {group_data_file}")

    # Actualizar el archivo __init__.py
    actualizar_init_py(concrete_models_path)

# Función para generar nombres de método basados en columnas y funciones de agregación
def generate_method_name(columns, agg_dict):
    column_str = "_".join(columns)
    agg_str = "_".join([f"{col}_{func}" for col, func in agg_dict.items()])
    return f"df_{column_str}_{agg_str}"

# Función para generar el contenido del método de agrupamiento
def generate_group_method_content(columns, agg_dict, options):
    method_name = generate_method_name(columns, agg_dict)
    
    method_content = f"    def {method_name}(self):\n"
    method_content += f"        if all(col in self.dataframe.columns for col in {columns}):\n"
    method_content += f"            result = self.dataframe.groupby({columns}).agg({agg_dict})\n"
    
    if 'reset_index' in options and options['reset_index']:
        method_content += f"            return result.reset_index()\n"
    else:
        method_content += f"            return result\n"
    
    method_content += f"        else:\n"
    method_content += f"            raise ValueError('Las columnas especificadas no existen en el dataframe')\n\n"

    return method_content
"""
# # Ejemplo de uso
# group_params_list = [
#     (['columna1'], {'columna3': 'mean'}, {'reset_index': True}),
#     (['columna2'], {'columna3': 'sum'}, {'reset_index': False})
# ]

# output_dir = 'my_models'

# generate_group_data_class(group_params_list, output_dir)

"""
import os
import pandas as pd

# Función para generar una nueva clase GroupData con métodos de agrupamiento
def generate_group_data_class(group_params_list, output_dir):
    # Ruta de la carpeta donde están las clases concretas
    # base_path = os.path.dirname(os.path.abspath(__file__))
    # print(base_path)
    # concrete_models_path = os.path.join(base_path, output_dir)
    # print('concreto : ' , concrete_models_path)
    
    concrete_models_path = output_dir # os.path.join(output_dir)
    os.makedirs(concrete_models_path, exist_ok=True)

    class_content = ""
    
    class_content += "import pandas as pd\n\n"
    
    # Generar la clase GroupData dinámicamente
    class_content += "class GroupData:\n"
    class_content += "    def __init__(self, dataframe: pd.DataFrame):\n"
    class_content += "        self.dataframe = dataframe\n\n"
    
    # Generar métodos de agrupamiento
    for columns, agg_dict, options in group_params_list:
        method_name = generate_method_name(columns, agg_dict)
        method_content = generate_group_method_content(columns, agg_dict, options)
        class_content += method_content

    # Guardar la clase GroupData en un archivo .py
    group_data_file = os.path.join(concrete_models_path, 'GroupData.py')
    with open(group_data_file, 'w', encoding='utf-8') as f:  # Especificar la codificación UTF-8
        f.write(class_content)

    print(f"Clase GroupData generada exitosamente en {group_data_file}")

# Función para generar nombres de método basados en columnas y funciones de agregación
def generate_method_name(columns, agg_dict):
    column_str = "_".join(columns)
    agg_str = "_".join([f"{col}_{func}" for col, func in agg_dict.items()])
    return f"df_{column_str}_{agg_str}"

# Función para generar el contenido del método de agrupamiento
def generate_group_method_content(columns, agg_dict, options):
    method_name = generate_method_name(columns, agg_dict)
    
    method_content = f"    def {method_name}(self):\n"
    method_content += f"        if all(col in self.dataframe.columns for col in {columns}):\n"
    method_content += f"            result = self.dataframe.groupby({columns}).agg({agg_dict})\n"
    
    # Verificar si se debe hacer reset_index
    if 'reset_index' in options and options['reset_index']:
        method_content += f"            return result.reset_index()\n"
    else:
        method_content += f"            return result\n"
    
    method_content += f"        else:\n"
    method_content += f"            raise ValueError('Las columnas especificadas no existen en el dataframe')\n\n"

    return method_content
"""



# # Llamar a la función si el script se ejecuta directamente
# if __name__ == "__main__":
#     my_models_path = os.path.join(base_path, 'my_models/concrete_models')
#     group_params_list = [
#         (['Escuela_ID', 'CURSO_NORMALIZADO'], {'Alumno_ID': 'count'}),
#         (['Profesor_ID'], {'Nota': 'mean'})
#     ]
#     add_group_methods_to_class(my_models_path, 'Group', group_params_list)
