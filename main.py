from gurobipy import *

NUM_COLEGIOS = 5
NUM_POR_CATEGORIA = 2
CATEGORIAS = 3

# NOMBRES_PRUEBAS = ('Velocidad', 'SaltoLargo')

def competidoresPorCat(num, cat):
    return [num for _ in range(cat)]

def duration_between(prueba):
    return [elem for elem in time_between if prueba in elem[0]]  #Decidir si queda para cualquiera con 'prueba' o solo en primer puesto


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
modules = ['mod'+str(i) for i in range(10)]

trials, duration, rest, place = multidict({
    'velocidad':  [10, 5, 1],
    'saltoLargo': [20, 5, 2]})

trial_rest = {'velocidad':  [3, 2, 1],
              'saltoLargo': [4, 3, 2]}

time_between = tupledict({('velocidad', 'saltoLargo'): 10,
                           ('saltoLargo', 'velocidad'): 5})

for tupla in duration_between('velocidad'):
        print('tiempo entre {} es de {}'.format(tupla, time_between[tupla]))

m = Model('Interescolar')

"""  VARIABLES  """

x = m.addVars(days, modules, trials, vtype=GRB.BINARY, name='module')

# y = m.addVars(num_byCat, schools, days, modules, trials, ub=1, name='category')  # Categoria k del colegio c, la prueba p en modulo m

# print(y)

"""" RESTRICCIONES X """

# Cantidad de pruebas por dia mayor igual a 2
rx1 = m.addConstrs((x.sum(day, '*') >= 2
                      for day in days), "Cant_pruebas")

# Solo puede asignarse una prueba en cada modulo
rx2 = m.addConstrs((x.sum(day, mod, '*') <= 1 for day in days for mod in modules), name='flujo')

# Numero total de  pruebas a hacer tiene que ser iguala 6
rx3 = m.addConstr((x.sum('*') == 6), name='total_pruebas')

# Maximo numero de pruebas tipo velocidad igual a 2
rx4 = m.addConstr((quicksum(x[d, m, 'velocidad'] for d in days for m in modules) <= 2), name='limite_vel')

"""  RETRICCIONES Y  """

#REVISAR
# Solo puede haber una categoria en la prueba p en el modulo m
# ry1 = m.addConstrs(y('juvenil', c, d, m, p) +
#                    y('intermedia', c, d, m, p) +
#                    y('superior', c, d, m, p)
#                    <= 1 for c in schools
#                    for d in days for m in modules for p in trials)
#
# ry1 = m.addConstrs(y.sum())
#
# ry2 = m.addConstrs(y.sum(k, '*', d, m, p) >= len(schools)
#                    for k in category for d in days for m in modules for p in trials)

m.update()

# print(ry2)

# ry2 = m.addConstr()

"""  FUNCION OBJETIVO Y SOLUCION  """

m.setObjective((quicksum(x[d, m, p]*duration[p] for d in days for m in modules for p in trials)), GRB.MINIMIZE)

m.update()

m.optimize()

m.printAttr('x')

status = m.status
if status == GRB.Status.UNBOUNDED:
    print('The model cannot be solved because it is unbounded')
    exit(0)
if status == GRB.Status.OPTIMAL:
    print('The optimal objective is %g' % m.objVal)
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
        print('%s' % c.constrName)



