#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Fco Javier Vicente Tequida'


import busquedas
from collections import Counter


class LightsOut(busquedas.ModeloBusqueda):
    # --------------------------------------------------------
    # Problema 2:  Completa la clase
    # para el modelo de lights out
    # --------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas
    adyacentes cambian (si estan prendidas se apagan y viceversa).

    El juego consiste en una matriz de 5 X 5, cuyo estado puede
    ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------

    Las acciones posibles son de elegir cambiar una luz y sus casillas
    adyacentes, por lo que la accion es un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self):
        # Acciones legales
        self.acciones = range(25)

    def acciones_legales(self, estado):
        # Se obtienen las acciones legales
        return self.acciones

    def sucesor(self, estado, accion):
        estado = list(estado)
        estado[accion] = 0 if estado[accion] == 1 else 1

        columna = accion % 5  # Encontrar la columna del elemento
        renglon = accion // 5  # Encontrar el renglon del elemento

        if columna != 4:  # Es posible agregar a la derecha
            estado[accion + 1] = 0 if estado[accion + 1] == 1 else 1
        if columna != 0:  # Es posible agregar a la izquierda
            estado[accion - 1] = 0 if estado[accion - 1] == 1 else 1

        if renglon != 4:  # Es posible agregar abajo
            estado[accion + 5] = 0 if estado[accion + 5] == 1 else 1
        if renglon != 0:  # Es posible agregar arriba
            estado[accion - 5] = 0 if estado[accion - 5] == 1 else 1

        return tuple(estado)

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        return cadena


# ------------------------------------------------------------
#  Problema 3: Completa el problema de LightsOut
# ------------------------------------------------------------
class ProblemaLightsOut(busquedas.ProblemaBusqueda):
    def __init__(self, pos_ini):
        """
        Utiliza la superclase para hacer el problema

        """
        # Completa el código
        x0 = tuple(pos_ini)

        def meta(x):
            # Ver si el estado es meta o no
            return sum(list(x)) == 0

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Dado un numero n de luces encendidas y suponiendo que cada
    movimiento consige modificar 5 luces, la heuristica se
    define como la cantidad de grupos de 5 luces necesarios a pulsar
    para llegar al estado objetivo.

    Considero la heuristica como admisible ya que para 5 luces o menos
    se requeriria de un paso. Son hasta cantidades multiplos de 5 donde
    los costos se elevan.
    """
    estado = list(nodo.estado)
    a = Counter(estado)
    return a[1]//5


# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Heuristica similar a la anterior pero genera un costo mayor
    debido a que ahora no se consideran meramente a los grupos
    posibles a formar mediante 5 elementos sino que tambien se
    incluye el grupo de luces menor a 5 que en la heuristica
    anterior da un costo de 0.
    Por ahora da mejores resultados que la heuristica 1.
    """
    estado = list(nodo.estado)
    a = Counter(estado)
    n = a[1]
    veces = 0
    while n > 0:
        n -= 5
        veces += 1
    return veces

# Dominancia de heuristicas
# dado que la segunda heuristica no discrimina a los grupos pequenios
# de luces (menores a 5), genera un costo mas elevado a lo que viene a
# ser dominante sobre la heuristica 1, ello se nota con una cantidad de
# nodos expandidos menor.


def prueba_modelo():
    """
    Prueba la clase LightsOut

    """

    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 = (1, 0, 0, 1, 0,
              1, 0, 1, 1, 0,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a4 = (1, 0, 0, 0, 1,
              1, 0, 1, 1, 1,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)

    modelo = LightsOut()

    assert modelo.acciones_legales(pos_ini) == range(25)
    assert modelo.sucesor(pos_ini, 0) == pos_a0
    assert modelo.sucesor(pos_a0, 4) == pos_a4
    assert modelo.sucesor(pos_a4, 24) == pos_a24
    assert modelo.sucesor(pos_a24, 15) == pos_a15
    assert modelo.sucesor(pos_a15, 12) == pos_a12
    print("Paso la prueba de la clase LightsOut")


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_2)

    print('-' * 50)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados')
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(10) + str(solucion1.costo).center(20) +
          str(solucion1.nodos_visitados))
    print('A* con h2'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')


if __name__ == "__main__":

    print("Antes de hacer otra cosa,")
    print("vamos a verificar medianamente la clase LightsOut")
    prueba_modelo()

    # Tres estados iniciales interesantes
    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)

    print("\n\nPara el problema en diagonal")
    print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_2)

    print("\n\nPara el problema simétrico")
    print("\n".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2)

    print("\n\nPara el problema Bonito")
    print("\n".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2)
