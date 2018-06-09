def competidoresPorCat(num, cat):
    return [num for _ in range(cat)]

def duration_between(prueba):
    return [elem for elem in time_between if prueba in elem[0]]  #Decidir si queda para cualquiera con 'prueba' o solo en primer puesto

def tuple_gen(_list):
    tuple_list = []
    for first in _list:
        for second in _list:
            if first != second:
                tupla = (first, second)
                tuple_list.append(tupla)
    return tuple_list
