from src.tools.data_loading import DataLoader
import src.tools.utils as u
from src.my_models_.__process.conservar_filas import conservar_filas_
# from src.my_models_.__process.fix_columna_edad import fix_columna_edad_
from src.my_models_.__process.agregar_columna_Nivel_Unificado import agregar_columna_Nivel_Unificado_
from src.my_models_.__process.reordenar_columnas import reordenar_columnas_
from src.my_models_.__process.calcular_DESEMPEÑO_por_Alumno_ID import calcular_DESEMPEÑO_por_Alumno_ID_
from src.my_models_.__process.get_alumnos_incluidos_SI import get_alumnos_incluidos_SI
from src.my_models_.__process.get_alumnos_incluidos_NO import get_alumnos_incluidos_NO
from src.my_models_.__process.get_alumnos_con_DESEMPEÑO import get_alumnos_con_DESEMPEÑO
from src.my_models_.__process.get_alumnos_sin_DESEMPEÑO import get_alumnos_sin_DESEMPEÑO
from src.my_models_.__process.get_alumnos_con_menos_de_300_palabras import get_alumnos_con_menos_de_300_palabras
from src.my_models_.__process.get_alumnos_con_más_de_300_palabras import get_alumnos_con_más_de_300_palabras
from src.my_models_.__process.get_mejor_medición_por_alumno import get_mejor_medición_por_alumno


# from src.my_models_.__process.quitar_columnas import quitar_columnas_
# from src.my_models_.__process.obtener_datos_de_columna import obtener_datos_de_columna_
# from src.my_models_.__process.ordenar_dataframe_por_columnas import ordenar_dataframe_por_columnas_
class FluidezLectora():

    def __init__(self):        
        # acá empiezo con la ejecución 
        self.run_all()

    def run_all(self):
        loader = DataLoader('Fluidez Lectora 1.csv')
        dfluidez = loader.load_csv()        
        print('inicializando..Fluidez Lectora 1')
        df_sin_duplicados = dfluidez.drop_duplicates()
        # dejo las filas que me interesan
        _dataframe_1 = conservar_filas_(df_sin_duplicados , 'CURSO_NORMALIZADO',['1°' , '2°' , '3°' , '4°' , '5°' , '6°' , '7°'])
        # agregar columna Nivel_Unificado  
        _dataframe_2 = agregar_columna_Nivel_Unificado_(_dataframe_1)
        # reordenar columnas
        _dataframe_3 = reordenar_columnas_(
            _dataframe_2,
            [
                'Alumno_ID','Operativo','CURSO_NORMALIZADO','Curso','División','Ausente','Cantidad_de_palabras','Prosodia','Incluido','Turno','Modalidad','Nivel','Nivel_Unificado','Gestión','Supervisión','Escuela_ID','Departamento','Localidad','zona','Regional','ciclo_lectivo','separador'
            ]
        )        
        # calcular desempeño por alumno, crear columna DESEMPEÑO
        _dataframe_4 = calcular_DESEMPEÑO_por_Alumno_ID_(_dataframe_3)        
        # filtrar dataframe
        # filtrar el dataframe para su análisis
        # alumnos incluidos = Si
        self._df_alumnos_incluidos_SI = get_alumnos_incluidos_SI(_dataframe_4)
        # alumnos incluidos = No
        self._df_alumnos_incluidos_NO = get_alumnos_incluidos_NO(_dataframe_4)
        # alumnos con DESEMPEÑO
        self._df_alumnos_con_DESEMPEÑO = get_alumnos_con_DESEMPEÑO(self._df_alumnos_incluidos_NO)
        # alumnos sin DESEMPEÑO
        self._df_alumnos_sin_DESEMPEÑO = get_alumnos_sin_DESEMPEÑO(self._df_alumnos_incluidos_NO)
        # alumnos con < de 300 palabras leídas
        self._df_alumnos_menor_a_300_palabras = get_alumnos_con_menos_de_300_palabras(self._df_alumnos_con_DESEMPEÑO)
        # alumnos con > de 300 palabras leídas
        self._df_alumnos_mayor_a_300_palabras = get_alumnos_con_más_de_300_palabras(self._df_alumnos_con_DESEMPEÑO)
        # alumnos con máxima cantidad de palabras leídas
        self._df_alumnos_con_MÁXIMA_cant_palabras = get_mejor_medición_por_alumno(self._df_alumnos_menor_a_300_palabras)

        # # crear el objeto para agrupar el df de fluidez
        # self.group_agg = GroupAggregation(self.preprocessor._df_alumnos_con_MÁXIMA_cant_palabras)
        # # agrupar dataframe por criterios
        # self.group_agg.groupby(self.preprocessor._df_alumnos_con_MÁXIMA_cant_palabras)
        # # calcular el porcentaje de desempeño de acuerdo a diferentes criterios
        # # creo un objeto para tal fin
        # self.calculador = CalculadorDePorcentajes(self.group_agg)
        # self.calculador.calcular_porcentajes_desempeño()

        u.save_dataframe_to_csv(_dataframe_4,'data/processed/transformed/Fluidez_1/DESEMPEÑO_por alumno calculado en Main.csv')

        u.save_dataframe_to_csv(self._df_alumnos_incluidos_SI,'data/processed/transformed/Fluidez_1/_df_alumnos_incluidos_SI.csv')
        u.save_dataframe_to_csv(self._df_alumnos_incluidos_NO,'data/processed/transformed/Fluidez_1/_df_alumnos_incluidos_NO.csv')
        u.save_dataframe_to_csv(self._df_alumnos_con_DESEMPEÑO,'data/processed/transformed/Fluidez_1/_df_alumnos_con_DESEMPEÑO.csv')
        u.save_dataframe_to_csv(self._df_alumnos_menor_a_300_palabras,'data/processed/transformed/Fluidez_1/_df_alumnos_menor_a_300_palabras.csv')
        u.save_dataframe_to_csv(self._df_alumnos_mayor_a_300_palabras,'data/processed/transformed/Fluidez_1/_df_alumnos_mayor_a_300_palabras.csv')
        u.save_dataframe_to_csv(self._df_alumnos_con_MÁXIMA_cant_palabras,'data/processed/transformed/Fluidez_1/_df_alumnos_con_MÁXIMA_cant_palabras.csv')
        return