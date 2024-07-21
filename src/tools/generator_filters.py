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

# Función para generar una nueva clase con métodos de filtrado
def generate_filter_class(filter_methods, main_dir, filter_dir, class_name):
    # Obtener el nombre de la carpeta principal automáticamente
    main_folder_name = os.path.basename(main_dir.rstrip('/\\'))
    # Crear la ruta completa para la carpeta de filtros
    concrete_models_path = os.path.join(main_dir, 'src', 'my_models_', filter_dir)
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
        class_content += "    def __init__(self, dataframe_dict):\n"
        class_content += "        self.dataframe_dict = dataframe_dict\n\n"

    # Agregar métodos de filtrado
    for method_name, df_name in filter_methods.items():
        if method_name not in metodos_existentes:
            method_content = generate_filter_method_content(method_name, df_name)
            class_content += method_content

    with open(class_file, 'w', encoding='utf-8') as f:
        f.write(class_content)

    print(f"Clase {class_name} generada exitosamente en {class_file}")

# Función para generar el contenido del método de filtrado
def generate_filter_method_content(method_name, df_name):
    method_content = f"    def {method_name}(self, value):\n"
    method_content += f"        df = self.dataframe_dict['{df_name}']\n"
    method_content += f"        # Aquí puedes añadir la lógica de filtrado\n"
    method_content += f"        \n"
    return method_content

# Ejemplo de uso
filter_methods = {
    'matricula_por_escuela': 'nominal_df_Escuela_ID_Alumno_ID_count',
    'desempeno_por_curso': 'nominal_df_Escuela_ID_Desempeno'
}

# main_dir = 'e:/GitHub/python_data_analysis'
# filter_dir = 'nombre_carpeta_filtros'
# class_name = 'Filtro'

# generate_filter_class(filter_methods, main_dir, filter_dir, class_name)

