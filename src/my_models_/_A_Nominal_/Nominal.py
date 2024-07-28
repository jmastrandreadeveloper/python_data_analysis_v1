from src.tools.data_loading import DataLoader
import src.tools.utils as u
from src.my_models_.__process.conservar_filas import conservar_filas_
from src.my_models_.__process.fix_columna_edad import fix_columna_edad_
from src.my_models_.__process.agregar_columna_Nivel_Unificado import agregar_columna_Nivel_Unificado_
from src.my_models_.__process.reordenar_columnas import reordenar_columnas_
from src.my_models_.__process.quitar_columnas import quitar_columnas_
from src.my_models_.__process.obtener_datos_de_columna import obtener_datos_de_columna_
from src.my_models_.__process.ordenar_dataframe_por_columnas import ordenar_dataframe_por_columnas_
class Nominal():

    def __init__(self):        
        # acá empiezo con la ejecución 
        self.run_all()

    def run_all(self):
        loader = DataLoader('Nominal.csv')
        dfnom = loader.load_csv()        
        print('inicializando..Nominal')
        # eliminar filas repetidas
        df_sin_duplicados = dfnom.drop_duplicates()
        # dejo las filas que me interesan
        _dataframe_1 = conservar_filas_(df_sin_duplicados , 'CURSO_NORMALIZADO',['1°' , '2°' , '3°' , '4°' , '5°' , '6°' , '7°'])
        # arreglar la columna edad para que queden todos en formato numérico
        _dataframe_2 = fix_columna_edad_(_dataframe_1)
        # agregar columna Nivel_Unificado
        _dataframe_3 = agregar_columna_Nivel_Unificado_(_dataframe_2)
        # reordenar columnas
        self.dataframe_4 = reordenar_columnas_(
            _dataframe_3,
            [
                'ciclo_lectivo','Alumno_ID','Sexo','Edad','Edad_Correcta','CURSO_NORMALIZADO','Curso','División','Turno','Modalidad','Nivel','Nivel_Unificado','Gestión','Supervisión','Escuela_ID','Departamento','Localidad','zona','AMBITO','Regional'
            ]
        )
        # quitar columnas para deja solamente las que me interesan
        _dataframe_5 = quitar_columnas_(self.dataframe_4 , ['ciclo_lectivo','Alumno_ID','Sexo','Edad','Edad_Correcta','CURSO_NORMALIZADO','Curso','División','Turno','Modalidad'] , True)        
        # ordenamos el df
        self.df_nominal_datos_institucionales = ordenar_dataframe_por_columnas_(_dataframe_5 , ['Escuela_ID'] , ascendente = True )
        # obtener la lista de las escuelas a analizar buscando en la columna Escuela_ID y devolviendo una lista de ellas
        self.listaEscuelas_IDs = obtener_datos_de_columna_(self.df_nominal_datos_institucionales,'Escuela_ID' , True)        
        # guardamos el procesado
        u.save_dataframe_to_csv(self.df_nominal_datos_institucionales,'data/processed/transformed/Nominal/Nominal_final_procesado.csv')
        # borrramos lo que no usamos
        dfnom,_dataframe_1,_dataframe_2,_dataframe_3,_dataframe_5,df_nominal_datos_institucionales = None,None,None,None,None,None