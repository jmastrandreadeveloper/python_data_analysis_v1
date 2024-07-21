import os
import importlib.util
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

            module_name = abstract_class.__module__.replace('src.abstract_model.', '')
            imports = f"from src.abstract_model.{module_name} import {name}\nimport pandas as pd\n\n"
            
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
from src.abstract_model.AbstractMain import AbstractMain
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




"""
import os
import importlib.util
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

        # Escribir la variable __all__ en el archivo __init__.py
        f.write("\n__all__ = [\n")
        for cls in all_classes:
            f.write(f"    '{cls}',\n")
        f.write("]\n")

    print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# Función para mostrar la cabecera del constructor de la clase abstracta
def show_constructor_signature(abstract_class):
    constructor = abstract_class.__init__
    constructor_signature = inspect.signature(constructor)
    return str(constructor_signature)

# # Ejemplo de uso para mostrar la cabecera del constructor
# if __name__ == "__main__":
#     # Cargar una clase abstracta para demostrar la función
#     abstract_class = load_module(os.path.join(abstract_model_path, 'AbstractReport.py')).AbstractReport
#     print("Constructor Signature:", show_constructor_signature(abstract_class))

#     my_models_path = os.path.join(base_path, 'my_models')
#     generate_concrete_classes(my_models_path, 'concrete_models')
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
                constructor_args.append(str(param))
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

        # Escribir la variable __all__ en el archivo __init__.py
        f.write("\n__all__ = [\n")
        for cls in all_classes:
            f.write(f"    '{cls}',\n")
        f.write("]\n")

    print(f"Clases concretas generadas exitosamente en {concrete_classes_path}.")

# Función para mostrar la cabecera del constructor de la clase abstracta
def show_constructor_signature(abstract_class):
    constructor = abstract_class.__init__
    constructor_signature = inspect.signature(constructor)
    return str(constructor_signature)
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
                constructor_args.append(param_name)
                super_args.append(param_name)

            constructor_args_str = ', '.join(constructor_args)
            super_args_str = ', '.join(super_args)
            class_definition = f"class {concrete_class_name}({name}):\n    def __init__(self, {constructor_args_str}):\n        super().__init__({super_args_str})\n\n"

            # Generar métodos abstractos vacíos
            methods = ""
            for method_name, method in abstract_class.__dict__.items():
                if inspect.isfunction(method) and getattr(method, "__isabstractmethod__", False):
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

# # Llamar a la función si el script se ejecuta directamente
# if __name__ == "__main__":
#     my_models_path = os.path.join(base_path, 'my_models')
#     generate_concrete_classes(my_models_path, 'concrete_models')
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
