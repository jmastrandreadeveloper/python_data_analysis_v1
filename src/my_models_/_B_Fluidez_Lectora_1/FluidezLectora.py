from src.tools.data_loading import DataLoader
import src.tools.utils as u
# from src.my_models_.__process.conservar_filas import conservar_filas_
# from src.my_models_.__process.fix_columna_edad import fix_columna_edad_
# from src.my_models_.__process.agregar_columna_Nivel_Unificado import agregar_columna_Nivel_Unificado_
# from src.my_models_.__process.reordenar_columnas import reordenar_columnas_
# from src.my_models_.__process.quitar_columnas import quitar_columnas_
# from src.my_models_.__process.obtener_datos_de_columna import obtener_datos_de_columna_
# from src.my_models_.__process.ordenar_dataframe_por_columnas import ordenar_dataframe_por_columnas_
class FluidezLectora():

    def __init__(self):        
        # acá empiezo con la ejecución 
        self.run_all()

    def run_all(self):
        loader = DataLoader('Fluidez Lectora 1.csv')
        dfnom = loader.load_csv()        
        print('inicializando..Fluidez Lectora 1')
        return