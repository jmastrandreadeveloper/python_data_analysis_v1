# src/__init__.py
"""
El archivo __init__.py dentro del directorio src (y también dentro de tests en algunos casos) 
tiene varias funciones importantes en un proyecto de Python:

Convertir el Directorio en un Paquete: El archivo __init__.py 
le dice a Python que el directorio debe ser tratado como un paquete. 

Esto es necesario para que puedas importar los módulos dentro del directorio. 
Sin este archivo, Python no reconocería el directorio como un paquete 
y no permitiría importar sus submódulos de la manera estándar.

Inicialización del Paquete: Puedes usar __init__.py para ejecutar código 
de inicialización cuando se importa el paquete. 
Esto podría incluir la configuración de variables de paquete, 
la importación de submódulos, o cualquier otra configuración necesaria.

Controlar las Exportaciones del Paquete: Puedes especificar qué submódulos 
y nombres deben estar disponibles cuando alguien importe el paquete. Esto se hace usando la lista __all__.

En resumen, __init__.py es esencial para definir un directorio como un paquete en Python 
y puede ser utilizado para configurar el entorno del paquete, 
simplificar las importaciones y controlar la inicialización del paquete.

"""

# Importar submódulos para que estén disponibles directamente desde el paquete
from .tools.data_loading import DataLoader
from .tools.utils import ensure_dir, save_dataframe_to_csv

# Opcional: Define qué submódulos están disponibles para importación
__all__ = ['DataLoader',  'ensure_dir', 'save_dataframe_to_csv']
