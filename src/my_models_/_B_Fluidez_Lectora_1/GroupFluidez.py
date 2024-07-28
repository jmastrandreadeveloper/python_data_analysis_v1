import src.tools.utils as u
import pandas as pd

from src.my_models_.__group_and_filter._df_Escuela_ID_Alumno_ID_count import agrupar_df_Escuela_ID_Alumno_ID_count
from src.my_models_.__group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_list import agrupar_df_Escuela_ID_CURSO_NORMALIZADO_list
from src.my_models_.__group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count import agrupar_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count
from src.my_models_.__group_and_filter._df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count import agrupar_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count

from src.my_models_.__group_and_filter._df_Escuela_ID_DESEMPEÑO_Alumno_ID_count import agrupar_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count

class GroupFluidez():

    def __init__(self , dataframe: pd.DataFrame):        
        self._dataframe = dataframe
        self.group()
    
    def group(self):
        self.Agrupado_df_Escuela_ID_Alumno_ID_count = agrupar_df_Escuela_ID_Alumno_ID_count(self._dataframe)
        self.Agrupado_df_lista_de_cursos_normalizados = agrupar_df_Escuela_ID_CURSO_NORMALIZADO_list(self._dataframe)
        self.Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count = agrupar_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count(self._dataframe)
        self.Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count = agrupar_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count(self._dataframe)

        u.save_dataframe_to_csv(self.Agrupado_df_Escuela_ID_Alumno_ID_count,'data/processed/transformed/Fluidez_1/Agrupado_df_Escuela_ID_Alumno_ID_count.csv')        
        u.save_dataframe_to_csv(self.Agrupado_df_lista_de_cursos_normalizados,'data/processed/transformed/Fluidez_1/Agrupado_df_lista_de_cursos_normalizados.csv')
        u.save_dataframe_to_csv(self.Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count,'data/processed/transformed/Fluidez_1/Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count.csv')
        u.save_dataframe_to_csv(self.Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count,'data/processed/transformed/Fluidez_1/Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count.csv')




        self.Agrupado_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count = agrupar_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count(self._dataframe)

        u.save_dataframe_to_csv(self.Agrupado_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count,'data/processed/transformed/Fluidez_1/Agrupado_df_Escuela_ID_DESEMPEÑO_Alumno_ID_count.csv')        
        return