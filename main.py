import os
import sys
from src.tools.data_loading import DataLoader

import src.tools.utils as u

from src.my_models_._A_Nominal_.Nominal import Nominal as mainNom
from src.my_models_._A_Nominal_.GroupNominal import GroupNominal as groupNom
import src.my_models_._C_Reporte.ReporteEscuela as repoEscuela

# obligatorio para poder acceder a todas las funcionalidades de las librerias para el proyecto y todo lo demas
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def main():
    nom = mainNom()    
    gNom = groupNom(nom.dataframe_4)

    rep = repoEscuela(
        nom.listaEscuelas_IDs ,
        nom.df_nominal_datos_institucionales,
        gNom.Agrupado_df_Escuela_ID_Alumno_ID_count,
        gNom.Agrupado_df_lista_de_cursos_normalizados,
        gNom.Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_Alumno_ID_count,
        gNom.Agrupado_df_Escuela_ID_CURSO_NORMALIZADO_División_Alumno_ID_count,
    )
    

    return

if __name__ == "__main__":
    main()