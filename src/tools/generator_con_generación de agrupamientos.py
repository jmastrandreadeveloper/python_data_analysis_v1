import os
import importlib.util
import pandas as pd
import inspect
from abc import ABC

# Ruta de la carpeta abstract_model
base_path = os.path.dirname(os.path.abspath(__file__))
abstract_model_path = os.path.join(base_path, 'src/abstract_model')

# Función para cargar un módulo dinámicamente
def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Función para generar nombres de métodos y claves
def generate_method_name(columns, agg_dict):
    column_part = "_".join(columns)
    agg_part = "_".join([f"{col}_{func}" for col, func in agg_dict.items()])
    return f"df_{column_part}_{agg_part}"

# Función para generar clases concretas
def generate_concrete_classes(output_dir, concrete_models, group_params_list=None):
    concrete_classes_path = os.path.join(output_dir, concrete_models)
    
    # Verificar si la carpeta ya existe
    if os.path.exists(concrete_classes_path):
        print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
        return
    
    os.makedirs(concrete_classes_path, exist_ok=True)

    # Inicializar la lista para __all__
    all_classes = []

    # Crear el archivo __init__.py dentro de concrete_models
    init_file = os.path.join(concrete_classes_path, '__init__.py')
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write("# Archivo __init__.py para el paquete concrete_models\n")
        f.write("\n")

        # Leer todas las clases abstractas
        abstract_classes = {}
        for filename in os.listdir(abstract_model_path):
            if filename.endswith('.py'):
                module = load_module(os.path.join(abstract_model_path, filename))
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
                        abstract_classes[name] = obj

        # Generar clases concretas y escribir importaciones en __init__.py
        for name, abstract_class in abstract_classes.items():
            concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
            f.write(f"from .{concrete_class_name} import {concrete_class_name}\n")
            all_classes.append(concrete_class_name)

            module_name = abstract_class.__module__.replace('src.', '')
            imports = f"from src.abstract_model.{module_name} import {name}\nimport pandas as pd\n\n"
            class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, dataframe: pd.DataFrame):\n        super().__init__(dataframe)\n\n"

            # Generar métodos abstractos vacíos o específicos para agrupamiento
            methods = ""
            for method_name, method in abstract_class.__dict__.items():
                if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
                    if method_name == "group_data" and group_params_list is not None and name == "AbstractGroup":
                        methods += "    def group_data(self):\n"
                        methods += "        self.grouped_data = {}\n"
                        for columns, agg_dict in group_params_list:
                            method_name_suffix = generate_method_name(columns, agg_dict)
                            group_code = (
                                f"        def {method_name_suffix}():\n"
                                f"            if all(col in self.dataframe.columns for col in {columns}):\n"
                                f"                self.grouped_data['{method_name_suffix}'] = self.dataframe.groupby({columns}).agg({agg_dict})\n"
                                f"            else:\n"
                                f"                raise ValueError('Las columnas especificadas no existen en el dataframe')\n"
                                f"        {method_name_suffix}()\n"
                            )
                            methods += group_code
                        methods += "\n"
                    else:
                        methods += f"    def {method_name}(self):\n        pass\n\n"

            # Guardar la clase concreta en un archivo
            file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
            with open(file_path, 'w', encoding='utf-8') as class_file:
                class_file.write(imports + class_definition + methods)

        # Escribir la variable __all__ en el archivo __init__.py
        f.write("\n__all__ = [\n")
        for cls in all_classes:
            f.write(f"    '{cls}',\n")
        f.write("]\n")

    print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# # Llamar a la función si el script se ejecuta directamente
# if __name__ == "__main__":
#     my_models_path = os.path.join(base_path, 'my_models')
#     group_params_list = [
#         (['Escuela_ID', 'CURSO_NORMALIZADO'], {'Alumno_ID': 'count'}),
#         (['Profesor_ID'], {'Nota': 'mean'})
#     ]
#     generate_concrete_classes(my_models_path, 'concrete_models', group_params_list)





"""
import os
import importlib.util
import pandas as pd
import inspect
from abc import ABC

# Ruta de la carpeta abstract_model
base_path = os.path.dirname(os.path.abspath(__file__))
abstract_model_path = os.path.join(base_path, 'src/abstract_model')

# Función para cargar un módulo dinámicamente
def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Función para generar clases concretas
def generate_concrete_classes(output_dir, concrete_models):
    concrete_classes_path = os.path.join(output_dir, concrete_models)
    
    # Verificar si la carpeta ya existe
    if os.path.exists(concrete_classes_path):
        print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
        return
    
    os.makedirs(concrete_classes_path, exist_ok=True)

    # Inicializar la lista para __all__
    all_classes = []

    # Crear el archivo __init__.py dentro de concrete_models
    init_file = os.path.join(concrete_classes_path, '__init__.py')
    with open(init_file, 'w') as f:
        f.write("# Archivo __init__.py para el paquete concrete_models\n")
        f.write("\n")

        # Leer todas las clases abstractas
        abstract_classes = {}
        for filename in os.listdir(abstract_model_path):
            if filename.endswith('.py'):
                module = load_module(os.path.join(abstract_model_path, filename))
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
                        abstract_classes[name] = obj

        # Generar clases concretas y escribir importaciones en __init__.py
        for name, abstract_class in abstract_classes.items():
            concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
            f.write(f"from .{concrete_class_name} import {concrete_class_name}\n")
            all_classes.append(concrete_class_name)

            module_name = abstract_class.__module__.replace('src.', '')
            imports = f"from src.abstract_model.{module_name} import {name}\nimport pandas as pd\n\n"
            class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, dataframe: pd.DataFrame):\n        super().__init__(dataframe)\n\n"

            # Generar métodos abstractos vacíos
            methods = ""
            for method_name, method in abstract_class.__dict__.items():
                if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
                    methods += f"    def {method_name}(self):\n        pass\n\n"

            # Guardar la clase concreta en un archivo
            file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
            with open(file_path, 'w') as class_file:
                class_file.write(imports + class_definition + methods)

        # Escribir la variable __all__ en el archivo __init__.py
        f.write("\n__all__ = [\n")
        for cls in all_classes:
            f.write(f"    '{cls}',\n")
        f.write("]\n")

    print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# Llamar a la función si el script se ejecuta directamente
if __name__ == "__main__":
    my_models_path = os.path.join(base_path, 'my_models')
    generate_concrete_classes(my_models_path, 'concrete_models')

"""




"""
import os
import importlib.util
import pandas as pd
import inspect
from abc import ABC

# Ruta de la carpeta abstract_model
base_path = os.path.dirname(os.path.abspath(__file__))
abstract_model_path = os.path.join(base_path, 'src/abstract_model')

# Función para cargar un módulo dinámicamente
def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Función para generar clases concretas
def generate_concrete_classes(output_dir , concrete_models):
    concrete_classes_path = os.path.join(output_dir, concrete_models)
    os.makedirs(concrete_classes_path, exist_ok=True)

    # Leer todas las clases abstractas
    abstract_classes = {}
    for filename in os.listdir(abstract_model_path):
        if filename.endswith('.py'):
            module = load_module(os.path.join(abstract_model_path, filename))
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
                    abstract_classes[name] = obj

    # Generar clases concretas
    for name, abstract_class in abstract_classes.items():
        concrete_class_name = f"Concrete{name}"
        module_name = abstract_class.__module__
        imports = f"from {module_name} import {name}\nimport pandas as pd\n\n"
        class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, dataframe: pd.DataFrame):\n        super().__init__(dataframe)\n\n"

        # Generar métodos abstractos vacíos
        methods = ""
        for method_name, method in abstract_class.__dict__.items():
            if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
                methods += f"    def {method_name}(self):\n        pass\n\n"

        # Guardar la clase concreta en un archivo
        file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
        with open(file_path, 'w') as f:
            f.write(imports + class_definition + methods)

    print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# Llamar a la función si el script se ejecuta directamente
if __name__ == "__main__":
    my_models_path = os.path.join(base_path, 'my_models')
    generate_concrete_classes(my_models_path)
"""
    

"""
Uso de generate_concrete_classes desde Otro Archivo
En otro archivo de tu proyecto, puedes importar y usar la función de la siguiente manera, especificando el directorio de salida:

import os
import sys

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'srrc'))

from generator import generate_concrete_classes

# Directorio de salida para las clases concretas
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_models')

# Generar clases concretas
generate_concrete_classes(output_dir)


"""


"""
src/
├── abstract_model/
│   ├── abstract_class1.py
│   ├── abstract_class2.py
│   └── ...
├── my_models/
│   └── concrete_models/
│       └── (archivos generados)
├── generator.py
└── (otros archivos)
"""
"""
import os
import importlib.util
import pandas as pd
import inspect
from abc import ABC

# Ruta de las carpetas
base_path = os.path.dirname(os.path.abspath(__file__))
abstract_model_path = os.path.join(base_path, 'abstract_model')
my_models_path = os.path.join(base_path, 'my_models')
concrete_classes_path = os.path.join(my_models_path, 'concrete_models')

# Crear la carpeta concreta si no existe
os.makedirs(concrete_classes_path, exist_ok=True)

# Función para cargar un módulo dinámicamente
def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Función para generar clases concretas
def generate_concrete_classes():
    # Leer todas las clases abstractas
    abstract_classes = {}
    for filename in os.listdir(abstract_model_path):
        if filename.endswith('.py'):
            module = load_module(os.path.join(abstract_model_path, filename))
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
                    abstract_classes[name] = obj

    # Generar clases concretas
    for name, abstract_class in abstract_classes.items():
        class_name = f"Concrete{name}"
        imports = f"from {abstract_class.__module__} import {name}\nimport pandas as pd\n\n"
        class_definition = f"class {class_name}({name}):\n    def __init__(self, dataframe: pd.DataFrame):\n        super().__init__(dataframe)\n\n"

        # Generar métodos abstractos vacíos
        methods = ""
        for method_name, method in abstract_class.__dict__.items():
            if inspect.isfunction(method) and method.__isabstractmethod__:
                methods += f"    def {method_name}(self):\n        pass\n\n"

        # Guardar la clase concreta en un archivo
        with open(os.path.join(concrete_classes_path, f"{class_name}.py"), 'w') as f:
            f.write(imports + class_definition + methods)

    print("Clases concretas generadas exitosamente.")

# Llamar a la función si el script se ejecuta directamente
if __name__ == "__main__":
    generate_concrete_classes()
"""
