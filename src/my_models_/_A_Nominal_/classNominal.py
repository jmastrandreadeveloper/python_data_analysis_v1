from src.tools.data_loading import DataLoader
import src.tools.utils as u

from .group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_list import agrupar_df_Escuela_ID_CURSO_NORMALIZADO_list , filtrar_df_Escuela_ID_CURSO_NORMALIZADO_list
from .group_and_filter._df_Escuela_ID_Alumno_ID_count import agrupar_df_Escuela_ID_Alumno_ID_count , filtrar_df_Escuela_ID_Alumno_ID_count

from src.my_models_.__process.conservar_filas import conservar_filas_
from src.my_models_.__process.fix_columna_edad import fix_columna_edad_
from src.my_models_.__process.agregar_columna_Nivel_Unificado import agregar_columna_Nivel_Unificado_
from src.my_models_.__process.reordenar_columnas import reordenar_columnas_
from src.my_models_.__process.quitar_columnas import quitar_columnas_
from src.my_models_.__process.obtener_datos_de_columna import obtener_datos_de_columna_
from src.my_models_.__process.ordenar_dataframe_por_columnas import ordenar_dataframe_por_columnas_

from src.my_models_.__group_and_filter.Class_df_Escuela_ID_Alumno_ID_count import Class_df_Escuela_ID_Alumno_ID_count

class Nominal():

    def __init__(self):        
        # acá empiezo con la ejecución 
        self.run_all()

    def run_all(self):
        loader = DataLoader('Nominal.csv')
        dfnom = loader.load_csv()        
        print('inicializando..')
        _dataframe_1 = conservar_filas_(dfnom , 'CURSO_NORMALIZADO',['1°' , '2°' , '3°' , '4°' , '5°' , '6°' , '7°'])
        # arreglar la columna edad para que queden todos en formato numérico
        _dataframe_2 = fix_columna_edad_(_dataframe_1)                
        # agregar columna Nivel_Unificado    
        _dataframe_3 = agregar_columna_Nivel_Unificado_(_dataframe_2)        
        # reordenar columnas
        _dataframe_4 = reordenar_columnas_(
            _dataframe_3,
            [
                'ciclo_lectivo','Alumno_ID','Sexo','Edad','Edad_Correcta','CURSO_NORMALIZADO','Curso','División','Turno','Modalidad','Nivel','Nivel_Unificado','Gestión','Supervisión','Escuela_ID','Departamento','Localidad','zona','AMBITO','Regional'
            ]
        )
        # quitar columnas para deja solamente las que me interesan
        _dataframe_5 = quitar_columnas_(_dataframe_4 , ['ciclo_lectivo','Alumno_ID','Sexo','Edad','Edad_Correcta','CURSO_NORMALIZADO','Curso','División','Turno','Modalidad'] , True)        
        # ordenamos el df
        df_nominal_datos_institucionales = ordenar_dataframe_por_columnas_(_dataframe_5 , ['Escuela_ID'] , ascendente = True )
        # obtener la lista de las escuelas a analizar buscando en la columna Escuela_ID y devolviendo una lista de ellas
        self.listaEscuelas_IDs = obtener_datos_de_columna_(df_nominal_datos_institucionales,'Escuela_ID' , True)
        # agrupamos a todo el nominal
        self._Objet_df_Escuela_ID_Alumno_ID_count = Class_df_Escuela_ID_Alumno_ID_count()
        self.Agrupado_df_Escuela_ID_Alumno_ID_count = self._Objet_df_Escuela_ID_Alumno_ID_count.agrupar_df_Escuela_ID_Alumno_ID_count(_dataframe_4)
        
        
        self._agrupar_df_lista_de_cursos_normalizados = agrupar_df_Escuela_ID_CURSO_NORMALIZADO_list(_dataframe_4)
        
        # creamos los filtros
        # _filtrar_lista_de_cursos_escuela = filtrar_df_Escuela_ID_CURSO_NORMALIZADO_list(9,self._agrupar_df_lista_de_cursos_normalizados)
        # _filtrar_df_Escuela_ID_Alumno_ID_count = filtrar_df_Escuela_ID_Alumno_ID_count(9,self.Agrupado_df_Escuela_ID_Alumno_ID_count)
        
        # vamos guardando
        u.save_dataframe_to_csv(df_nominal_datos_institucionales,'data/processed/transformed/Nominal/Nominal_final_procesado.csv')
        u.save_dataframe_to_csv(self._agrupar_df_lista_de_cursos_normalizados,'data/processed/transformed/Nominal/_agrupar_df_lista_de_cursos_normalizados.csv')
        u.save_dataframe_to_csv(self.Agrupado_df_Escuela_ID_Alumno_ID_count,'data/processed/transformed/Nominal/_agrupar_df_Escuela_ID_Alumno_ID_count.csv')

    def get_listaEscuelas_IDs(self):
        return self.listaEscuelas_IDs

    def get_Agrupado_df_Escuela_ID_Alumno_ID_count(self):
        return self.Agrupado_df_Escuela_ID_Alumno_ID_count