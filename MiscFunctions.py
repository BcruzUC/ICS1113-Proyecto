def competidoresPorCat(num, cat):
    return [num for _ in range(cat)]

def duration_between(prueba):
    return [elem for elem in time_between if prueba in elem[0]]  #Decidir si queda para cualquiera con 'prueba' o solo en primer puesto

# Retorna las tuplas iguales al principio en orden inverso de como se ingresan.
def tuple_gen(_list):
    tuple_list = []
    for first in _list:
        for second in _list:
            tupla = (first, second)
            if tupla not in tuple_list:
                if first == second:
                    tuple_list.insert(0, tupla)
                else:
                    tuple_list.append(tupla)
    return tuple_list


if __name__ == '__main__':
    test = tuple_gen(['velocidad', 'vallas', 'saltoAlto', 'saltoLargo'])
    for elem in test:
        print(elem)
