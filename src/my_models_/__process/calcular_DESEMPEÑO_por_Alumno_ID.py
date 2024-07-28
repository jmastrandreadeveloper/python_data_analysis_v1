import pandas as pd

def calcular_DESEMPEÑO_por_Alumno_ID_(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['DESEMPEÑO'] = dataframe.apply(lambda row: determinar_desempeño_por_fila( row ), axis=1)
    # reordenar columnas..
    dataframe = dataframe.reindex(columns=[
        'DESEMPEÑO',
        'Alumno_ID',
        'Operativo',
        'CURSO_NORMALIZADO',
        'Curso',
        'División',
        'Ausente',
        'Cantidad_de_palabras',
        'Prosodia',
        'Incluido',
        'Turno',
        'Modalidad',
        'Nivel',
        'Nivel_Unificado',
        'Gestión',
        'Supervisión',
        'Escuela_ID',
        'Departamento',
        'Localidad',
        'zona',
        'Regional',
        'ciclo_lectivo',
        'separador'])
    return dataframe


def determinar_desempeño_por_fila(row):
    condiciones = {
        ('2°', 'Primario'): [(0, 15, 'Crítico'), (16, 45, 'Básico'), (46, 70, 'Medio'), (71, float('inf'), 'Avanzado')],
        ('3°', 'Primario'): [(0, 30, 'Crítico'), (31, 60, 'Básico'), (61, 90, 'Medio'), (91, float('inf'), 'Avanzado')],
        ('4°', 'Primario'): [(0, 45, 'Crítico'), (46, 75, 'Básico'), (76, 110, 'Medio'), (111, float('inf'), 'Avanzado')],
        ('5°', 'Primario'): [(0, 60, 'Crítico'), (61, 90, 'Básico'), (91, 125, 'Medio'), (126, float('inf'), 'Avanzado')],
        ('6°', 'Primario'): [(0, 75, 'Crítico'), (76, 105, 'Básico'), (106, 140, 'Medio'), (141, float('inf'), 'Avanzado')],
        ('7°', 'Primario'): [(0, 85, 'Crítico'), (86, 115, 'Básico'), (116, 155, 'Medio'), (156, float('inf'), 'Avanzado')],
        ('1°', 'Secundario Orientado'): [(0, 95, 'Crítico'), (96, 125, 'Básico'), (126, 165, 'Medio'), (166, float('inf'), 'Avanzado')],
        ('1°', 'Secundario Técnico'): [(0, 95, 'Crítico'), (96, 125, 'Básico'), (126, 165, 'Medio'), (166, float('inf'), 'Avanzado')],
        ('1º Bilingüe', 'Secundario Orientado'): [(0, 95, 'Crítico'), (96, 125, 'Básico'), (126, 165, 'Medio'), (166, float('inf'), 'Avanzado')],
        ('1º Bilingüe', 'Secundario Técnico'): [(0, 95, 'Crítico'), (96, 125, 'Básico'), (126, 165, 'Medio'), (166, float('inf'), 'Avanzado')],
        ('2°', 'Secundario Orientado'): [(0, 105, 'Crítico'), (106, 135, 'Básico'), (136, 170, 'Medio'), (171, float('inf'), 'Avanzado')],
        ('2°', 'Secundario Técnico'): [(0, 105, 'Crítico'), (106, 135, 'Básico'), (136, 170, 'Medio'), (171, float('inf'), 'Avanzado')],
        ('2º Bilingüe', 'Secundario Orientado'): [(0, 105, 'Crítico'), (106, 135, 'Básico'), (136, 170, 'Medio'), (171, float('inf'), 'Avanzado')],
        ('2º Bilingüe', 'Secundario Técnico'): [(0, 105, 'Crítico'), (106, 135, 'Básico'), (136, 170, 'Medio'), (171, float('inf'), 'Avanzado')],
        ('3°', 'Secundario Orientado'): [(0, 115, 'Crítico'), (116, 145, 'Básico'), (146, 175, 'Medio'), (176, float('inf'), 'Avanzado')],
        ('3°', 'Secundario Técnico'): [(0, 115, 'Crítico'), (116, 145, 'Básico'), (146, 175, 'Medio'), (176, float('inf'), 'Avanzado')],
        ('3º Bilingüe', 'Secundario Orientado'): [(0, 115, 'Crítico'), (116, 145, 'Básico'), (146, 175, 'Medio'), (176, float('inf'), 'Avanzado')],
        ('3º Bilingüe', 'Secundario Técnico'): [(0, 115, 'Crítico'), (116, 145, 'Básico'), (146, 175, 'Medio'), (176, float('inf'), 'Avanzado')],
        ('4°', 'Secundario Orientado'): [(0, 120, 'Crítico'), (121, 150, 'Básico'), (151, 180, 'Medio'), (181, float('inf'), 'Avanzado')],
        ('4°', 'Secundario Técnico'): [(0, 120, 'Crítico'), (121, 150, 'Básico'), (151, 180, 'Medio'), (181, float('inf'), 'Avanzado')],
        ('4º Bilingüe', 'Secundario Orientado'): [(0, 120, 'Crítico'), (121, 150, 'Básico'), (151, 180, 'Medio'), (181, float('inf'), 'Avanzado')],
        ('4º Bilingüe', 'Secundario Técnico'): [(0, 120, 'Crítico'), (121, 150, 'Básico'), (151, 180, 'Medio'), (181, float('inf'), 'Avanzado')],
        ('5°', 'Secundario Orientado'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('5°', 'Secundario Técnico'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('5º Bilingüe', 'Secundario Orientado'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('5º Bilingüe', 'Secundario Técnico'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('6°', 'Secundario Orientado'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('6°', 'Secundario Técnico'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('6º Bilingüe', 'Secundario Orientado'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
        ('6º Bilingüe', 'Secundario Técnico'): [(0, 125, 'Crítico'), (126, 155, 'Básico'), (156, 185, 'Medio'), (186, float('inf'), 'Avanzado')],
    }

    key = (row['CURSO_NORMALIZADO'], row['Nivel'])
    if key in condiciones:
        for min_val, max_val, desempeño in condiciones[key]:
            if min_val <= row['Cantidad_de_palabras'] <= max_val:
                return desempeño
    return None  # or some default value if no condition matches