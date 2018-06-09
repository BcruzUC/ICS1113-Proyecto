from gurobipy import *
from MiscFunctions import *

NUM_COLEGIOS = 5
NUM_POR_CATEGORIA = 2
CATEGORIAS = 3



category, num_byCat, trials_num = multidict({
    'Infantil': [6, 2],
    'Intermedia': [6, 2],
    'Superior': [6, 2]})


schools, juvenil, intermedia, superior = multidict({
    'VerboDivino': competidoresPorCat(2, 3),
    'SanAnselmo':  competidoresPorCat(2, 3),
    'VillaMaria':  competidoresPorCat(2, 3),
    'Cumbres':     competidoresPorCat(2, 3),
    'SaintGeorge': competidoresPorCat(2, 3)})

# crear con modulos

days = ['viernes', 'sabado']
modules = ['mod'+str(i) for i in range(5)]

trials, duration, rest, place = multidict({
    'velocidad':  [10, 5, 1],
    'vallas':     [10, 5, 1],
    'saltoAlto': [20, 5, 2],
    'saltoLargo':  [25, 5, 2]})

# time_between = tupledict({('velocidad', 'saltoLargo'): 10,
#                            ('saltoLargo', 'velocidad'): 5,})

## Tiempos de espera entre pruebas
delay_list = [35, 40, 35, 20, 25, 25, 25, 25, 20, 25, 25, 20]
delay_couples = tuple_gen(trials)
time_between = {delay_couples[i]: delay_list[i] for i in range(len(delay_list))}


## PRUEBA DE FUNCION DE TIEMPOS

# for tupla in duration_between('velocidad', time_between):
#         print('tiempo entre {} es de {}'.format(tupla, time_between[tupla]))

m = Model('Interescolar')

"""  VARIABLES  """

# falta agregar categoria
x = m.addVars(days, modules, trials, category, vtype=GRB.BINARY, name='x')

y = m.addVars(num_byCat, schools, days, modules, trials, vtype=GRB.BINARY, name='y')  # Categoria k del colegio c, la prueba p en modulo m


"""" RESTRICCIONES X """

## Cantidad de pruebas por dia mayor igual a 2
rx1 = m.addConstrs((x.sum(d, '*') >= 12 for d in days), "Cant_pruebas")

## Solo puede asignarse 2 pruebas en cada modulo
rx2 = m.addConstrs((x.sum(d, m, p,'*') <= 2 for d in days for m in modules for p in trials), name='flujo')

## Numero total de  pruebas a hacer tiene que ser igual o menor a 30
rx3 = m.addConstr((x.sum('*') <= 30), name='total_pruebas')

## Maximo numero de pruebas tipo velocidad igual a 2
# rx4 = m.addConstr((quicksum(x[d, m, 'velocidad'] for d in days for m in modules) <= 2), name='limite_vel')

##
rx4 = m.addConstrs(x.sum(d, '*', p, k) <= 1 for d in days for p in trials for k in category)


"""  RETRICCIONES Y  """

# Solo una categoria de cada colegio asignada a un modulo y dia especifico
ry1 = m.addConstrs(y.sum('*', c, d, m, p)
                   <= 1 for c in schools
                   for d in days for m in modules for p in trials)

# Solo compite una vez en cada prueba, cada categoria
ry2 = m.addConstrs(y.sum(k, c, '*', d, p) <= 1 for k in category for c in schools for d in days for p in trials)


"""  RELACION VARIABLE Y - X  """
# Para que se asigne la variable x=1 entonces tienen que competir los 5 colegios de la categoria debida
rxy1 = m.addConstrs(y.sum(k, '*', d, m, p)/len(schools) >= x[d, m, p, k]
                   for k in category for d in days for m in modules for p in trials)


m.update()

"""  FUNCION OBJETIVO Y SOLUCION  """

# m.setObjective((quicksum(x[d, m, p, k]*duration[p] for d in days for m in modules for p in trials
#                          for k in category)), GRB.MINIMIZE)

m.setObjective((quicksum(x[d, m, p1, k]*time_between[p1, p2] for d in days for m in modules for p1 in trials
                         for p2 in trials for k in category if p1 != p2)), GRB.MINIMIZE)

m.update()

m.optimize()

status = m.status
if status == GRB.Status.UNBOUNDED:
    print('The model cannot be solved because it is unbounded')
    exit(0)
if status == GRB.Status.OPTIMAL:
    print('The optimal objective is %g' % m.objVal)
    # with open('Assignation.txt', 'w') as output:
    #     print(m.printAttr('x', filter='x*'), file=output)
    m.printAttr('x', filter='x*')
    exit(0)
if status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
    print('Optimization was stopped with status %d' % status)
    exit(0)

# do IIS
print('The model is infeasible; computing IIS')
m.computeIIS()
if m.IISMinimal:
  print('IIS is minimal\n')
else:
  print('IIS is not minimal\n')
print('\nThe following constraint(s) cannot be satisfied:')
for c in m.getConstrs():
    if c.IISConstr:
        print('{}: {}'.format(c.constrName, m.getConstrByName(c.constrName)))


