from problemas import PblCamionMagico
import busquedas
import math
import random

problemaCamion = PblCamionMagico((10, 1))
solucion = busquedas.busqueda_profundo(problemaCamion)
print(solucion)
print("Explorando {} nodos\n\n".format(solucion.nodos_visitados))


def h1(estado):
    _, posicion = estado
    count = 0
    while posicion != 1:
        posicion = posicion / 2
        math.trunc(posicion)
        count += 1
    return count


for i in range(100):
    problema = PblCamionMagico((random.randint(2, 100), 1))
    solucion = busquedas.busqueda_profundo(problemaCamion)
    print("----Prueba numero {}----".format(i))
    # print("Costo: {}, heuristica: {}".format())
