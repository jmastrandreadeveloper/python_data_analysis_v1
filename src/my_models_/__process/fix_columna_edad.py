import pandas as pd
import numpy as np
from src.my_models_.__process.reordenar_columnas import reordenar_columnas_

def fix_columna_edad_(dataframe) -> pd.DataFrame:
    print('...arreglando datos de la columna edad...')
    
    def create_age_reference() -> dict:
        """
        Crear un diccionario de referencia de edades.
        """
        age_reference = {
            ('Primario', '1°'): 6,
            ('Primario', '2°'): 7,
            ('Primario', '3°'): 8,
            ('Primario', '4°'): 9,
            ('Primario', '5°'): 10,
            ('Primario', '6°'): 11,
            ('Primario', '7°'): 12,

            ('Secundario Orientado', '1°'): 13,
            ('Secundario Orientado', '2°'): 14,
            ('Secundario Orientado', '3°'): 15,
            ('Secundario Orientado', '4°'): 16,
            ('Secundario Orientado', '5°'): 17,
            ('Secundario Orientado', '6°'): 18,

            ('Secundario Técnico', '1°'): 13,
            ('Secundario Técnico', '2°'): 14,
            ('Secundario Técnico', '3°'): 15,
            ('Secundario Técnico', '4°'): 16,
            ('Secundario Técnico', '5°'): 17,
            ('Secundario Técnico', '6°'): 18,
        }
        return age_reference

    def get_correct_age(row, age_reference, distancia):
        """
        Función para obtener la edad correcta.
        """
        key = (row['Nivel'], row['Curso'])
        if key in age_reference:
            reference_age = age_reference[key]
            try:
                current_age = int(row['Edad'])
                if abs(current_age - reference_age) > distancia:
                    return reference_age
                else:
                    return current_age
            except ValueError:
                return reference_age
        else:
            try:
                return int(row['Edad'])
            except ValueError:
                return np.nan

    def correct_invalid_ages(dataframe, age_reference, distancia):
        """
        Corrige las edades inválidas utilizando la referencia de edades.
        """
        dataframe['Edad_Correcta'] = dataframe.apply(get_correct_age, axis=1, age_reference=age_reference, distancia=distancia)
        dataframe = reordenar_columnas_(
            dataframe,
            [
                'ciclo_lectivo', 'Alumno_ID', 'Sexo', 'Edad', 'Edad_Correcta', 'CURSO_NORMALIZADO', 'Curso', 'División',
                'Turno', 'Modalidad', 'Nivel', 'Gestión', 'Supervisión', 'Escuela_ID', 'Departamento', 'Localidad',
                'zona', 'AMBITO', 'Regional'
            ]
        )
        return dataframe

    age_reference = create_age_reference()
    distancia_entre_edades = 2

    # Evitar SettingWithCopyWarning
    dataframe = dataframe.copy()
    dataframe = correct_invalid_ages(dataframe, age_reference, distancia_entre_edades)

    return dataframe