import os
import sys
from src.tools.data_loading import DataLoader

import src.tools.utils as u
import src.my_models_._A_Nominal_.classNominal as mainNom
import src.my_models_._C_Reporte.ReporteEscuela as repoEscuela

# obligatorio para poder acceder a todas las funcionalidades de las librerias para el proyecto y todo lo demas
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def main():
    nom = mainNom.Nominal()
    rep = repoEscuela(nom)
    

    return

if __name__ == "__main__":
    main()