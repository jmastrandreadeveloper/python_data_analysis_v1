import pandas as pd

def ordenar_dataframe_por_columnas_(dataframe: pd.DataFrame, listaDeColumnasParaOrdenar: list, ascendente: bool = True) -> pd.DataFrame:
    """
    Ordena un DataFrame según las columnas especificadas.

    Parámetros:
    - dataframe (pd.DataFrame): El DataFrame a ordenar.
    - listaDeColumnasParaOrdenar (list): Lista de nombres de columnas por las cuales ordenar el DataFrame.
    - ascendente (bool): Orden ascendente si es True, descendente si es False. Por defecto es True.

    Retorna:
    - pd.DataFrame: DataFrame ordenado.
    """
    return dataframe.sort_values(by=listaDeColumnasParaOrdenar, ascending=ascendente)
