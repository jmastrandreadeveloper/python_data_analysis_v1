#from src.my_models_._abstract_model_.AbstractReport import AbstractReport
import src.tools.utils as u
import src.tools.DataFrameToCharJS as DataFrameToCharJS
import src.tools.DataFrameToDict as DataFrameToDict
import src.tools.DataFrameToDict as DataFrameToDict
import src.tools.DataFrameToTabla as DataFrameToTabla
import src.tools.DictToDataFrame as DictToDataFrame
import pandas as pd

import src.my_models_._A_Nominal_.classNominal as mainNom

class ReporteEscuela() :

    def __init__(self, nominal : mainNom):
        print('..haciendo reporte por escuela..')
        self.nominal = nominal

    def do_report(self):
        self.do_report_escuela()
    
    def do_report_escuela(self, *args, **kwargs): 
        print('reporte por escuela de fluidez lectora')
        
        self.listDictFinal = []
        self.dictDatos = {
            'Escuela_ID' : None,
            'datos institucionales' : None
        }
        for Escuela_ID in self.nominal.xxx:
            dictDatos = {
                'Escuela_ID' : Escuela_ID,
                'data' : {
                    #'datos_institucionales' : self.filtro._nominal_df_nominal_datos_institucionales(Escuela_ID),                    
                    #'lista_de_cursos_escuela' : self.filtro._nominal_lista_de_cursos_escuela(Escuela_ID),
                    'matricula_por_escuela' : self.nominal.agrupado_df_Escuela_ID_Alumno_ID_count ,
                    #'matricula_por_escuela_curso' : self.filtro._nominal_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count(Escuela_ID),
                    #'matricula_por_escuela_curso_división' : self.filtro._nominal_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count(Escuela_ID),
                    #'fluidez lectora 1' : {
                    #   'matricula_por_escuela_fluidez_lectora_1' : self.filtro._fluidez_df_Escuela_ID_Alumno_ID_count(Escuela_ID),
                    #}
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