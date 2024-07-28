# en este archivo vamos a hacer la llamada para crear todos los grupos y sus filtros
# va a ser creados en archivos separados, el grupo y el filtro estarán en un archivo 
# la idea es la de suministrar casi los mismos datos que cuando se hacían los grupos
# pero ahora hay que darle el nombre de la función que va a tener
# generando los grupos que serán comunes a ambos dataframes
group_params_list = [
    (['Escuela_ID'] , {'Alumno_ID': 'count'} , ('matrícula_por_Escuela_ID') , {'reset_index': True}),
    (['Escuela_ID', 'CURSO_NORMALIZADO'] , {'Alumno_ID': 'count'} , ('matrícula_por_Escuela_ID_y_Curso') , {'reset_index': True}),
    (['Escuela_ID','CURSO_NORMALIZADO','División'] , {'Alumno_ID': 'count'} , ('matrícula_por_Escuela_ID_Curso_y_División') , {'reset_index': True}),    
    (['Nivel_Unificado','CURSO_NORMALIZADO'] , {'Alumno_ID':'count'} , ('matrícula_por_Nivel_Unificado_y_Curso') , {'reset_index': True}),
    (['Supervisión','CURSO_NORMALIZADO'] , {'Alumno_ID':'count'} , ('matrícula_por_Supervisión_y_Curso') , {'reset_index': True}),

]
# generate_group_aggregation_class(group_params_list , os.path.dirname(os.path.abspath(__file__)),'GroupAggregationNominal')
        