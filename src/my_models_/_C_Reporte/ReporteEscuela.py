import pandas as pd

import src.tools.utils as u
import src.tools.DataFrameToCharJS as DataFrameToCharJS
import src.tools.DataFrameToDict as DataFrameToDict
import src.tools.DataFrameToDict as DataFrameToDict
import src.tools.DataFrameToTabla as DataFrameToTabla
import src.tools.DictToDataFrame as DictToDataFrame

from src.my_models_.__group_and_filter._df_Escuela_ID_Alumno_ID_count import filtrar_df_Escuela_ID_Alumno_ID_count
from src.my_models_.__group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_list import filtrar_df_Escuela_ID_CURSO_NORMALIZADO_list
from src.my_models_.__group_and_filter.filter_datos_institucionales import filtrar_datos_institucionales
from src.my_models_.__group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count import filtrar_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count
from src.my_models_.__group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count import filtrar_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count

from src.my_models_.__group_and_filter._df_Escuela_ID_DESEMPEÑO_Alumno_ID_count import filtrar_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count

class ReporteEscuela() :

    def __init__(self,                 
                 listaEscuelas_IDs: list,
                 df_nominal_datos_institucionales : pd.DataFrame,
                 Nominal_Agrupado_df_Escuela_ID_Alumno_ID_count: pd.DataFrame,
                 Nominal_Agrupado_df_lista_de_cursos_normalizados: pd.DataFrame,
                 Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count: pd.DataFrame,
                 Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count: pd.DataFrame,
                 
                 Fluidez_Agrupado_df_Escuela_ID_Alumno_ID_count: pd.DataFrame):
        
        print('..haciendo reporte por escuela..')
        self.listaEscuelas_IDs = listaEscuelas_IDs
        self.df_nominal_datos_institucionales = df_nominal_datos_institucionales
        self.Nominal_Agrupado_df_Escuela_ID_Alumno_ID_count = Nominal_Agrupado_df_Escuela_ID_Alumno_ID_count
        self.Nominal_Agrupado_df_lista_de_cursos_normalizados = Nominal_Agrupado_df_lista_de_cursos_normalizados        
        self.Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count = Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count
        self.Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count = Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count

        self.Fluidez_Agrupado_df_Escuela_ID_Alumno_ID_count = Fluidez_Agrupado_df_Escuela_ID_Alumno_ID_count
        
        self.do_report()

    def do_report(self):
        self.do_report_escuela()
    
    def do_report_escuela(self, *args, **kwargs): 
        print('reporte por escuela de fluidez lectora')
        
        self.listDictFinal = []
        self.dictDatos = {
            'Escuela_ID' : None,
            'datos institucionales' : None
        }
        for Escuela_ID in self.listaEscuelas_IDs:
            lista_de_cursos_escuela = filtrar_df_Escuela_ID_CURSO_NORMALIZADO_list(Escuela_ID , self.Nominal_Agrupado_df_lista_de_cursos_normalizados)
            dictDatos = {
                'Escuela_ID' : Escuela_ID,
                'data' : {
                    'datos_institucionales' : filtrar_datos_institucionales(Escuela_ID , self.df_nominal_datos_institucionales),                    
                    'lista_de_cursos_escuela' : lista_de_cursos_escuela,
                    'matricula_por_escuela' : filtrar_df_Escuela_ID_Alumno_ID_count(Escuela_ID , self.Nominal_Agrupado_df_Escuela_ID_Alumno_ID_count),
                    'matricula_por_escuela_curso' : filtrar_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count(Escuela_ID ,  self.Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count),
                    'matricula_por_escuela_curso_división' : filtrar_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count(Escuela_ID , self.Nominal_Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count , lista_de_cursos_escuela),
                     'fluidez lectora 1' : {
                        'matricula_por_escuela_fluidez_lectora_1' : filtrar_df_Escuela_ID_Alumno_ID_count(Escuela_ID , self.Fluidez_Agrupado_df_Escuela_ID_Alumno_ID_count),
                    }
                }
            }
            # cuando tengo datos procesados de fluidez 1
            # if dictDatos['data']['fluidez lectora 1']['matricula_por_escuela_fluidez_lectora_1'] != 0 :                
            #     dictDatosFluidez_Lectora = {                    
            #         'matricula_por_escuela_fluidez_lectora_1' : self.filtro._fluidez_df_Escuela_ID_Alumno_ID_count(Escuela_ID),
            #         'listado_de_cursos_fluidez_lectora_1' : self.filtro._fluidez_lista_de_cursos_escuela(Escuela_ID),
            #         'matricula_por_curso_fluidez_lectora_1' : self.filtro._fluidez_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count(Escuela_ID),
            #         'matricula_por_curso_y_división_fluidez_lectora_1' : self.filtro._fluidez_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count(Escuela_ID),
            #         'desempeño_por_escuela' : self.filtro._fluidez_df_Desempeño_por_Escuela(Escuela_ID),
            #         'desempeño_por_escuela_y_curso' : self.filtro._fluidez_df_Desempeño_por_Escuela_CURSO_NORMALIZADO(Escuela_ID),
            #         'total_alumnos_por_tipo_de_desempeño_por_curso' : self.filtro._fluidez_total_alumnos_por_desempeño_por_escuela_y_curso(Escuela_ID),
            #         'desempeño_por_escuela_curso_y_division' : self.filtro._fluidez_df_Desempeño_por_Escuela_CURSO_NORMALIZADO_Division(Escuela_ID),
            #     }

                # reemplazdo la clave de fl anterior con la nueva generada
                #dictDatos['data']['fluidez lectora 1'] = dictDatosFluidez_Lectora

            self.listDictFinal.append(dictDatos)
        print(dictDatos)
        dataDict = u.obtener_data_de_la_lista(
            self.listDictFinal,
            'Escuela_ID',
            9,
            [
                'data'
            ]
        )
        print(dataDict)
        u.imprimirDiccionario(dataDict)
        pass