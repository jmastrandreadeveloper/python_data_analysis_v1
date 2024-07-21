import os
import importlib.util
import inspect
from abc import ABC

# Ruta de la carpeta abstract_model
base_path = os.path.dirname(os.path.abspath(__file__))
abstract_model_path = os.path.join(base_path, 'src/_src_abstract_model_')

# Función para cargar un módulo dinámicamente
def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Función para leer el contenido de un archivo existente
def leer_archivo(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# Función para copiar clases abstractas y eliminar el prefijo "Src" de los nombres de las clases y archivos
def copiar_clases_abstractas(origen, destino):
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    for filename in os.listdir(origen):
        if filename.endswith('.py'):
            with open(os.path.join(origen, filename), 'r', encoding='utf-8') as f_src:
                content = f_src.read()
                # Quitar el prefijo "Src" de los nombres de las clases
                content = content.replace("class Src", "class ")
            
            # Quitar el prefijo "Src" del nombre del archivo
            new_filename = filename.replace('Src', '', 1)
            with open(os.path.join(destino, new_filename), 'w', encoding='utf-8') as f_dest:
                f_dest.write(content)

# Función para generar clases concretas
def generate_concrete_classesV2(output_dir, concrete_models):
    concrete_classes_path = os.path.join(output_dir, concrete_models)
    common_abstract_path = os.path.join(output_dir, '_abstract_model_')
    # recortar la el nombre tools para que no lo tenga en cuenta
    # quito el 'tools/' del path 
    print('concrete_classes_path ' , concrete_classes_path)
    concrete_classes_path = concrete_classes_path.replace('tools/','')
    
    # Verificar si la carpeta ya existe
    if os.path.exists(concrete_classes_path):
        print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
        return
    
    os.makedirs(concrete_classes_path, exist_ok=True)

    # Copiar las clases abstractas a la nueva ubicación si no se ha hecho antes
    if not os.path.exists(common_abstract_path):
        copiar_clases_abstractas(abstract_model_path, common_abstract_path)

    # Inicializar la lista para __all__
    all_classes = []

    # Crear el archivo __init__.py dentro de concrete_models
    init_file = os.path.join(concrete_classes_path, '__init__.py')
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write("# Archivo __init__.py para el paquete concrete_models\n")
        f.write("\n")

        # Leer todas las clases abstractas
        abstract_classes = {}
        for filename in os.listdir(common_abstract_path):
            if filename.endswith('.py'):
                module = load_module(os.path.join(common_abstract_path, filename))
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
                        abstract_classes[name] = obj

        # Generar clases concretas y escribir importaciones en __init__.py
        for name, abstract_class in abstract_classes.items():
            concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
            module_name = f"src.my_models_._abstract_model_"
            imports = f"from {module_name}.{name} import {name}\nimport pandas as pd\n\n"
            
            # Obtener el constructor de la clase abstracta
            constructor = abstract_class.__init__
            constructor_signature = inspect.signature(constructor)
            constructor_params = constructor_signature.parameters

            # Generar la definición del constructor para la clase concreta
            constructor_args = []
            super_args = []
            for param_name, param in constructor_params.items():
                if param_name == 'self':
                    continue
                param_str = str(param).replace('pandas.core.frame.DataFrame', 'pd.DataFrame')
                constructor_args.append(param_str)
                super_args.append(param_name)

            constructor_args_str = ', '.join(constructor_args)
            super_args_str = ', '.join(super_args)
            class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, {constructor_args_str}):\n        super().__init__({super_args_str})\n\n"

            # Generar métodos abstractos vacíos
            methods = ""
            for method_name, method in abstract_class.__dict__.items():
                if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
                    methods += f"    def {method_name}(self, *args, **kwargs):\n        pass\n\n"

            # Guardar la clase concreta en un archivo
            file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
            with open(file_path, 'w', encoding='utf-8') as class_file:
                class_file.write(imports + class_definition + methods)
            
            # Escribir importación en __init__.py
            f.write(f"from .{concrete_class_name} import {concrete_class_name}\n")
            all_classes.append(concrete_class_name)

        # Generar la clase Main y añadirla a __init__.py
        generate_main_class(concrete_classes_path, f)
        all_classes.append("Main")

        # Escribir la variable __all__ en el archivo __init__.py
        f.write("\n__all__ = [\n")
        for cls in all_classes:
            f.write(f"    '{cls}',\n")
        f.write("]\n")

    print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

def generate_main_class(concrete_classes_path, init_file_handle):
    main_class_file = os.path.join(concrete_classes_path, 'Main.py')
    main_class_content = """
import pandas as pd
from src.my_models_._abstract_model_.AbstractMain import AbstractMain
from .GroupAggregation import GroupAggregation
from .Preprocessor import Preprocessor
from .Transform import Transform

class Main(AbstractMain):

    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)
        self.group_agg = GroupAggregation(dataframe)
        self.preprocessor = Preprocessor(dataframe)
        self.transform = Transform(dataframe)

    def run_all(self):
        # Implementar una secuencia de operaciones que utilicen los métodos de las instancias
        pass
"""
    with open(main_class_file, 'w', encoding='utf-8') as f:
        f.write(main_class_content)
    
    init_file_handle.write("from .Main import Main\n")
    print(f"Clase Main generada exitosamente en {main_class_file}")

# Función para mostrar la cabecera del constructor de la clase abstracta
def show_constructor_signature(abstract_class):
    constructor = abstract_class.__init__
    constructor_signature = inspect.signature(constructor)
    return str(constructor_signature)

######################## mal
# import os
# import importlib.util
# import inspect
# from abc import ABC

# # Ruta de la carpeta abstract_model
# base_path = os.path.dirname(os.path.abspath(__file__))
# abstract_model_path = os.path.join(base_path, 'src/_src_abstract_model_')

# # Función para cargar un módulo dinámicamente
# def load_module(module_path):
#     module_name = os.path.splitext(os.path.basename(module_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, module_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# # Función para leer el contenido de un archivo existente
# def leer_archivo(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     return None

# # Función para copiar clases abstractas y eliminar el prefijo "Src" de los nombres de las clases y archivos
# def copiar_clases_abstractas(origen, destino):
#     if not os.path.exists(destino):
#         os.makedirs(destino)
    
#     for filename in os.listdir(origen):
#         if filename.endswith('.py'):
#             with open(os.path.join(origen, filename), 'r', encoding='utf-8') as f_src:
#                 content = f_src.read()
#                 # Quitar el prefijo "Src" de los nombres de las clases
#                 content = content.replace("class Src", "class ")
            
#             # Quitar el prefijo "Src" del nombre del archivo
#             new_filename = filename.replace('Src', '', 1)
#             with open(os.path.join(destino, new_filename), 'w', encoding='utf-8') as f_dest:
#                 f_dest.write(content)

# # Función para generar clases concretas
# def generate_concrete_classesV2(output_dir, concrete_models):
#     concrete_classes_path = os.path.join(output_dir, concrete_models)
#     common_abstract_path = os.path.join(output_dir, '_abstract_model_')
    
#     # Verificar si la carpeta ya existe
#     if os.path.exists(concrete_classes_path):
#         print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
#         return
    
#     os.makedirs(concrete_classes_path, exist_ok=True)

#     # Copiar las clases abstractas a la nueva ubicación si no se ha hecho antes
#     if not os.path.exists(common_abstract_path):
#         copiar_clases_abstractas(abstract_model_path, common_abstract_path)

#     # Inicializar la lista para __all__
#     all_classes = []

#     # Crear el archivo __init__.py dentro de concrete_models
#     init_file = os.path.join(concrete_classes_path, '__init__.py')
#     with open(init_file, 'w', encoding='utf-8') as f:
#         f.write("# Archivo __init__.py para el paquete concrete_models\n")
#         f.write("\n")

#         # Leer todas las clases abstractas
#         abstract_classes = {}
#         for filename in os.listdir(common_abstract_path):
#             if filename.endswith('.py'):
#                 module = load_module(os.path.join(common_abstract_path, filename))
#                 for name, obj in module.__dict__.items():
#                     if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
#                         abstract_classes[name] = obj

#         # Generar clases concretas y escribir importaciones en __init__.py
#         for name, abstract_class in abstract_classes.items():
#             concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
#             module_name = abstract_class.__module__.replace('src._src_abstract_model_', 'src.my_models_._abstract_model_')
#             imports = f"from {module_name} import {name}\nimport pandas as pd\n\n"
#             f.write(imports)
#             all_classes.append(concrete_class_name)

#             # Obtener el constructor de la clase abstracta
#             constructor = abstract_class.__init__
#             constructor_signature = inspect.signature(constructor)
#             constructor_params = constructor_signature.parameters

#             # Generar la definición del constructor para la clase concreta
#             constructor_args = []
#             super_args = []
#             for param_name, param in constructor_params.items():
#                 if param_name == 'self':
#                     continue
#                 param_str = str(param).replace('pandas.core.frame.DataFrame', 'pd.DataFrame')
#                 constructor_args.append(param_str)
#                 super_args.append(param_name)

#             constructor_args_str = ', '.join(constructor_args)
#             super_args_str = ', '.join(super_args)
#             class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, {constructor_args_str}):\n        super().__init__({super_args_str})\n\n"

#             # Generar métodos abstractos vacíos
#             methods = ""
#             for method_name, method in abstract_class.__dict__.items():
#                 if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
#                     methods += f"    def {method_name}(self, *args, **kwargs):\n        pass\n\n"

#             # Guardar la clase concreta en un archivo
#             file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
#             with open(file_path, 'w', encoding='utf-8') as class_file:
#                 class_file.write(imports + class_definition + methods)

#         # Generar la clase Main y añadirla a __init__.py
#         generate_main_class(concrete_classes_path, f)
#         all_classes.append("Main")

#         # Escribir la variable __all__ en el archivo __init__.py
#         f.write("\n__all__ = [\n")
#         for cls in all_classes:
#             f.write(f"    '{cls}',\n")
#         f.write("]\n")

#     print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# def generate_main_class(concrete_classes_path, init_file_handle):
#     main_class_file = os.path.join(concrete_classes_path, 'Main.py')
#     main_class_content = """
# import pandas as pd
# from src.my_models_._abstract_model_.AbstractMain import AbstractMain
# from .GroupAggregation import GroupAggregation
# from .Preprocessor import Preprocessor
# from .Transform import Transform

# class Main(AbstractMain):

#     def __init__(self, dataframe: pd.DataFrame):
#         super().__init__(dataframe)
#         self.group_agg = GroupAggregation(dataframe)
#         self.preprocessor = Preprocessor(dataframe)
#         self.transform = Transform(dataframe)

#     def run_all(self):
#         # Implementar una secuencia de operaciones que utilicen los métodos de las instancias
#         pass
# """
#     with open(main_class_file, 'w', encoding='utf-8') as f:
#         f.write(main_class_content)
    
#     init_file_handle.write("from .Main import Main\n")
#     print(f"Clase Main generada exitosamente en {main_class_file}")

# # Función para mostrar la cabecera del constructor de la clase abstracta
# def show_constructor_signature(abstract_class):
#     constructor = abstract_class.__init__
#     constructor_signature = inspect.signature(constructor)
#     return str(constructor_signature)



##########################################
# import os
# import importlib.util
# import inspect
# from abc import ABC

# # Ruta de la carpeta abstract_model
# base_path = os.path.dirname(os.path.abspath(__file__))
# abstract_model_path = os.path.join(base_path, 'src/_src_abstract_model_')

# # Función para cargar un módulo dinámicamente
# def load_module(module_path):
#     module_name = os.path.splitext(os.path.basename(module_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, module_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# # Función para leer el contenido de un archivo existente
# def leer_archivo(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     return None

# # Función para copiar clases abstractas y eliminar el prefijo "Src" de los nombres de las clases y archivos
# def copiar_clases_abstractas(origen, destino):
#     if not os.path.exists(destino):
#         os.makedirs(destino)
    
#     for filename in os.listdir(origen):
#         if filename.endswith('.py'):
#             with open(os.path.join(origen, filename), 'r', encoding='utf-8') as f_src:
#                 content = f_src.read()
#                 # Quitar el prefijo "Src" de los nombres de las clases
#                 content = content.replace("class Src", "class ")
            
#             # Quitar el prefijo "Src" del nombre del archivo
#             new_filename = filename.replace('Src', '', 1)
#             with open(os.path.join(destino, new_filename), 'w', encoding='utf-8') as f_dest:
#                 f_dest.write(content)

# # Función para generar clases concretas
# def generate_concrete_classesV2(output_dir, concrete_models):
#     concrete_classes_path = os.path.join(output_dir, concrete_models)
#     common_abstract_path = os.path.join(output_dir, '_abstract_model_')
    
#     # Verificar si la carpeta ya existe
#     if os.path.exists(concrete_classes_path):
#         print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
#         return
    
#     os.makedirs(concrete_classes_path, exist_ok=True)

#     # Copiar las clases abstractas a la nueva ubicación si no se ha hecho antes
#     if not os.path.exists(common_abstract_path):
#         copiar_clases_abstractas(abstract_model_path, common_abstract_path)

#     # Inicializar la lista para __all__
#     all_classes = []

#     # Crear el archivo __init__.py dentro de concrete_models
#     init_file = os.path.join(concrete_classes_path, '__init__.py')
#     with open(init_file, 'w', encoding='utf-8') as f:
#         f.write("# Archivo __init__.py para el paquete concrete_models\n")
#         f.write("\n")

#         # Leer todas las clases abstractas
#         abstract_classes = {}
#         for filename in os.listdir(common_abstract_path):
#             if filename.endswith('.py'):
#                 module = load_module(os.path.join(common_abstract_path, filename))
#                 for name, obj in module.__dict__.items():
#                     if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
#                         abstract_classes[name] = obj

#         # Generar clases concretas y escribir importaciones en __init__.py
#         for name, abstract_class in abstract_classes.items():
#             concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
#             f.write(f"from src.my_models_._abstract_model_ import {name}\n")
#             all_classes.append(concrete_class_name)

#             # Obtener el constructor de la clase abstracta
#             constructor = abstract_class.__init__
#             constructor_signature = inspect.signature(constructor)
#             constructor_params = constructor_signature.parameters

#             # Generar la definición del constructor para la clase concreta
#             constructor_args = []
#             super_args = []
#             for param_name, param in constructor_params.items():
#                 if param_name == 'self':
#                     continue
#                 param_str = str(param).replace('pandas.core.frame.DataFrame', 'pd.DataFrame')
#                 constructor_args.append(param_str)
#                 super_args.append(param_name)

#             constructor_args_str = ', '.join(constructor_args)
#             super_args_str = ', '.join(super_args)
#             class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, {constructor_args_str}):\n        super().__init__({super_args_str})\n\n"

#             # Generar métodos abstractos vacíos
#             methods = ""
#             for method_name, method in abstract_class.__dict__.items():
#                 if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
#                     methods += f"    def {method_name}(self, *args, **kwargs):\n        pass\n\n"

#             # Guardar la clase concreta en un archivo
#             file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
#             with open(file_path, 'w', encoding='utf-8') as class_file:
#                 class_file.write(class_definition + methods)

#         # Generar la clase Main y añadirla a __init__.py
#         generate_main_class(concrete_classes_path, f)
#         all_classes.append("Main")

#         # Escribir la variable __all__ en el archivo __init__.py
#         f.write("\n__all__ = [\n")
#         for cls in all_classes:
#             f.write(f"    '{cls}',\n")
#         f.write("]\n")

#     print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# def generate_main_class(concrete_classes_path, init_file_handle):
#     main_class_file = os.path.join(concrete_classes_path, 'Main.py')
#     main_class_content = """
# import pandas as pd
# from src.my_models_._abstract_model_.AbstractMain import AbstractMain
# from .GroupAggregation import GroupAggregation
# from .Preprocessor import Preprocessor
# from .Transform import Transform

# class Main(AbstractMain):

#     def __init__(self, dataframe: pd.DataFrame):
#         super().__init__(dataframe)
#         self.group_agg = GroupAggregation(dataframe)
#         self.preprocessor = Preprocessor(dataframe)
#         self.transform = Transform(dataframe)

#     def run_all(self):
#         # Implementar una secuencia de operaciones que utilicen los métodos de las instancias
#         pass
# """
#     with open(main_class_file, 'w', encoding='utf-8') as f:
#         f.write(main_class_content)
    
#     init_file_handle.write("from .Main import Main\n")
#     print(f"Clase Main generada exitosamente en {main_class_file}")

# # Función para mostrar la cabecera del constructor de la clase abstracta
# def show_constructor_signature(abstract_class):
#     constructor = abstract_class.__init__
#     constructor_signature = inspect.signature(constructor)
#     return str(constructor_signature)



# ######################### v2
# import os
# import importlib.util
# import inspect
# from abc import ABC

# # Ruta de la carpeta abstract_model
# base_path = os.path.dirname(os.path.abspath(__file__))
# abstract_model_path = os.path.join(base_path, 'src/_src_abstract_model_')

# # Función para cargar un módulo dinámicamente
# def load_module(module_path):
#     module_name = os.path.splitext(os.path.basename(module_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, module_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# # Función para leer el contenido de un archivo existente
# def leer_archivo(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     return None

# # Función para copiar clases abstractas y eliminar el prefijo "Src" de los nombres de las clases y archivos
# def copiar_clases_abstractas(origen, destino):
#     if not os.path.exists(destino):
#         os.makedirs(destino)
    
#     for filename in os.listdir(origen):
#         if filename.endswith('.py'):
#             with open(os.path.join(origen, filename), 'r', encoding='utf-8') as f_src:
#                 content = f_src.read()
#                 # Quitar el prefijo "Src" de los nombres de las clases
#                 content = content.replace("class Src", "class ")
            
#             # Quitar el prefijo "Src" del nombre del archivo
#             new_filename = filename.replace('Src', '', 1)
#             with open(os.path.join(destino, new_filename), 'w', encoding='utf-8') as f_dest:
#                 f_dest.write(content)

# # Función para generar clases concretas
# def generate_concrete_classesV2(output_dir, concrete_models):
#     concrete_classes_path = os.path.join(output_dir, concrete_models)
#     common_abstract_path = os.path.join(output_dir, '_abstract_model_')
    
#     # Verificar si la carpeta ya existe
#     if os.path.exists(concrete_classes_path):
#         print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
#         return
    
#     os.makedirs(concrete_classes_path, exist_ok=True)

#     # Copiar las clases abstractas a la nueva ubicación si no se ha hecho antes
#     if not os.path.exists(common_abstract_path):
#         copiar_clases_abstractas(abstract_model_path, common_abstract_path)

#     # Inicializar la lista para __all__
#     all_classes = []

#     # Crear el archivo __init__.py dentro de concrete_models
#     init_file = os.path.join(concrete_classes_path, '__init__.py')
#     with open(init_file, 'w', encoding='utf-8') as f:
#         f.write("# Archivo __init__.py para el paquete concrete_models\n")
#         f.write("\n")

#         # Leer todas las clases abstractas
#         abstract_classes = {}
#         for filename in os.listdir(common_abstract_path):
#             if filename.endswith('.py'):
#                 module = load_module(os.path.join(common_abstract_path, filename))
#                 for name, obj in module.__dict__.items():
#                     if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
#                         abstract_classes[name] = obj

#         # Generar clases concretas y escribir importaciones en __init__.py
#         for name, abstract_class in abstract_classes.items():
#             concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
#             f.write(f"from .{concrete_class_name} import {concrete_class_name}\n")
#             all_classes.append(concrete_class_name)

#             # Ajuste de la ruta de importación para las clases abstractas
#             imports = f"from src.my_models_._abstract_model_ import {name}\nimport pandas as pd\n\n"

#             # Obtener el constructor de la clase abstracta
#             constructor = abstract_class.__init__
#             constructor_signature = inspect.signature(constructor)
#             constructor_params = constructor_signature.parameters

#             # Generar la definición del constructor para la clase concreta
#             constructor_args = []
#             super_args = []
#             for param_name, param in constructor_params.items():
#                 if param_name == 'self':
#                     continue
#                 param_str = str(param).replace('pandas.core.frame.DataFrame', 'pd.DataFrame')
#                 constructor_args.append(param_str)
#                 super_args.append(param_name)

#             constructor_args_str = ', '.join(constructor_args)
#             super_args_str = ', '.join(super_args)
#             class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, {constructor_args_str}):\n        super().__init__({super_args_str})\n\n"

#             # Generar métodos abstractos vacíos
#             methods = ""
#             for method_name, method in abstract_class.__dict__.items():
#                 if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
#                     methods += f"    def {method_name}(self, *args, **kwargs):\n        pass\n\n"

#             # Guardar la clase concreta en un archivo
#             file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
#             with open(file_path, 'w', encoding='utf-8') as class_file:
#                 class_file.write(imports + class_definition + methods)

#         # Generar la clase Main y añadirla a __init__.py
#         generate_main_class(concrete_classes_path, f)
#         all_classes.append("Main")

#         # Escribir la variable __all__ en el archivo __init__.py
#         f.write("\n__all__ = [\n")
#         for cls in all_classes:
#             f.write(f"    '{cls}',\n")
#         f.write("]\n")

#     print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# def generate_main_class(concrete_classes_path, init_file_handle):
#     main_class_file = os.path.join(concrete_classes_path, 'Main.py')
#     main_class_content = """
# import pandas as pd
# from src.my_models_._abstract_model_.AbstractMain import AbstractMain
# from .GroupAggregation import GroupAggregation
# from .Preprocessor import Preprocessor
# from .Transform import Transform

# class Main(AbstractMain):

#     def __init__(self, dataframe: pd.DataFrame):
#         super().__init__(dataframe)
#         self.group_agg = GroupAggregation(dataframe)
#         self.preprocessor = Preprocessor(dataframe)
#         self.transform = Transform(dataframe)

#     def run_all(self):
#         # Implementar una secuencia de operaciones que utilicen los métodos de las instancias
#         pass
# """
#     with open(main_class_file, 'w', encoding='utf-8') as f:
#         f.write(main_class_content)
    
#     init_file_handle.write("from .Main import Main\n")
#     print(f"Clase Main generada exitosamente en {main_class_file}")

# # Función para mostrar la cabecera del constructor de la clase abstracta
# def show_constructor_signature(abstract_class):
#     constructor = abstract_class.__init__
#     constructor_signature = inspect.signature(constructor)
#     return str(constructor_signature)



##################### funciona maso menos 1 
# import os
# import importlib.util
# import inspect
# from abc import ABC

# # Ruta de la carpeta abstract_model
# base_path = os.path.dirname(os.path.abspath(__file__))
# abstract_model_path = os.path.join(base_path, 'src/_src_abstract_model_')

# # Función para cargar un módulo dinámicamente
# def load_module(module_path):
#     module_name = os.path.splitext(os.path.basename(module_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, module_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# # Función para leer el contenido de un archivo existente
# def leer_archivo(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     return None

# # Función para copiar clases abstractas y eliminar el prefijo "Src" de los nombres de las clases y archivos
# def copiar_clases_abstractas(origen, destino):
#     if not os.path.exists(destino):
#         os.makedirs(destino)
    
#     for filename in os.listdir(origen):
#         if filename.endswith('.py'):
#             with open(os.path.join(origen, filename), 'r', encoding='utf-8') as f_src:
#                 content = f_src.read()
#                 # Quitar el prefijo "Src" de los nombres de las clases
#                 content = content.replace("class Src", "class ")
            
#             # Quitar el prefijo "Src" del nombre del archivo
#             new_filename = filename.replace('Src', '', 1)
#             with open(os.path.join(destino, new_filename), 'w', encoding='utf-8') as f_dest:
#                 f_dest.write(content)

# # Función para generar clases concretas
# def generate_concrete_classesV2(output_dir, concrete_models):
#     concrete_classes_path = os.path.join(output_dir, concrete_models)
#     common_abstract_path = os.path.join(output_dir, '_abstract_model_')
    
#     # Verificar si la carpeta ya existe
#     if os.path.exists(concrete_classes_path):
#         print(f"La carpeta '{concrete_classes_path}' ya existe. No se generarán nuevas clases concretas para evitar sobrescritura.")
#         return
    
#     os.makedirs(concrete_classes_path, exist_ok=True)

#     # Copiar las clases abstractas a la nueva ubicación si no se ha hecho antes
#     if not os.path.exists(common_abstract_path):
#         copiar_clases_abstractas(abstract_model_path, common_abstract_path)

#     # Inicializar la lista para __all__
#     all_classes = []

#     # Crear el archivo __init__.py dentro de concrete_models
#     init_file = os.path.join(concrete_classes_path, '__init__.py')
#     with open(init_file, 'w', encoding='utf-8') as f:
#         f.write("# Archivo __init__.py para el paquete concrete_models\n")
#         f.write("\n")

#         # Leer todas las clases abstractas
#         abstract_classes = {}
#         for filename in os.listdir(common_abstract_path):
#             if filename.endswith('.py'):
#                 module = load_module(os.path.join(common_abstract_path, filename))
#                 for name, obj in module.__dict__.items():
#                     if isinstance(obj, type) and issubclass(obj, ABC) and obj is not ABC:
#                         abstract_classes[name] = obj

#         # Generar clases concretas y escribir importaciones en __init__.py
#         for name, abstract_class in abstract_classes.items():
#             concrete_class_name = name.replace('Abstract', '', 1)  # Eliminar el prefijo "Abstract"
#             f.write(f"from .{concrete_class_name} import {concrete_class_name}\n")
#             all_classes.append(concrete_class_name)

#             module_name = abstract_class.__module__.replace('src._abstract_model_', '_abstract_model_')
#             imports = f"from {module_name} import {name}\nimport pandas as pd\n\n"
            
#             # Obtener el constructor de la clase abstracta
#             constructor = abstract_class.__init__
#             constructor_signature = inspect.signature(constructor)
#             constructor_params = constructor_signature.parameters

#             # Generar la definición del constructor para la clase concreta
#             constructor_args = []
#             super_args = []
#             for param_name, param in constructor_params.items():
#                 if param_name == 'self':
#                     continue
#                 param_str = str(param).replace('pandas.core.frame.DataFrame', 'pd.DataFrame')
#                 constructor_args.append(param_str)
#                 super_args.append(param_name)

#             constructor_args_str = ', '.join(constructor_args)
#             super_args_str = ', '.join(super_args)
#             class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, {constructor_args_str}):\n        super().__init__({super_args_str})\n\n"

#             # Generar métodos abstractos vacíos
#             methods = ""
#             for method_name, method in abstract_class.__dict__.items():
#                 if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
#                     methods += f"    def {method_name}(self, *args, **kwargs):\n        pass\n\n"

#             # Guardar la clase concreta en un archivo
#             file_path = os.path.join(concrete_classes_path, f"{concrete_class_name}.py")
#             with open(file_path, 'w', encoding='utf-8') as class_file:
#                 class_file.write(imports + class_definition + methods)

#         # Generar la clase Main y añadirla a __init__.py
#         generate_main_class(concrete_classes_path, f)
#         all_classes.append("Main")

#         # Escribir la variable __all__ en el archivo __init__.py
#         f.write("\n__all__ = [\n")
#         for cls in all_classes:
#             f.write(f"    '{cls}',\n")
#         f.write("]\n")

#     print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# def generate_main_class(concrete_classes_path, init_file_handle):
#     main_class_file = os.path.join(concrete_classes_path, 'Main.py')
#     main_class_content = """
# import pandas as pd
# from _abstract_model_.AbstractMain import AbstractMain
# from .GroupAggregation import GroupAggregation
# from .Preprocessor import Preprocessor
# from .Transform import Transform

# class Main(AbstractMain):

#     def __init__(self, dataframe: pd.DataFrame):
#         super().__init__(dataframe)
#         self.group_agg = GroupAggregation(dataframe)
#         self.preprocessor = Preprocessor(dataframe)
#         self.transform = Transform(dataframe)

#     def run_all(self):
#         # Implementar una secuencia de operaciones que utilicen los métodos de las instancias
#         pass
# """
#     with open(main_class_file, 'w', encoding='utf-8') as f:
#         f.write(main_class_content)
    
#     init_file_handle.write("from .Main import Main\n")
#     print(f"Clase Main generada exitosamente en {main_class_file}")

# # Función para mostrar la cabecera del constructor de la clase abstracta
# def show_constructor_signature(abstract_class):
#     constructor = abstract_class.__init__
#     constructor_signature = inspect.signature(constructor)
#     return str(constructor_signature)