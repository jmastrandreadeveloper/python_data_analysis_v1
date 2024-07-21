import os
import pandas as pd
import src.tools.utils as u
import re

class DataLoader:
    def __init__(self, filename):
        # Construye la ruta completa al archivo CSV
        self.filepath = os.path.join(os.path.dirname(__file__), '..' , 'data', 'raw', filename)
        # recortar la el nombre tools para que no lo tenga en cuenta
        
        # quito el 'tools/' del path 
        #self.filepath = self.filepath.replace('tools/','')        
        
        self.filepath = self.clean_path(self.filepath)
    
    def load_csv(self):
        # Verifica que el archivo exista
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"No se encontró el archivo: {self.filepath}")        
        return u.quitar_retorno_de_columnas(pd.read_csv(self.filepath , header=0 , delimiter=";" , encoding = "UTF-8" , lineterminator = '\n'))

    def load_excel(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"No se encontró el archivo: {self.filepath}")
        return pd.read_excel(self.filepath)
    
    def clean_path(self,path):
        # Divide la ruta en componentes
        parts = path.split(os.sep)
        
        # Elimina cualquier componente que sea 'tools'
        cleaned_parts = [part for part in parts if part != 'tools']
        
        # Vuelve a ensamblar la ruta
        cleaned_path = os.sep.join(cleaned_parts)
        
        return cleaned_path
