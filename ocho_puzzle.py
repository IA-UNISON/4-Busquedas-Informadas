#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ocho_puzzle.py
------------

Ejemplo del problema del Ocho puzzle resuelto
con diferentes métodos de búsqueda

"""

__author__ = 'juliowaissman'


import busquedas
from time import time

class Modelo8puzzle(busquedas.ModeloBusqueda):
    """
    El problema del 8 puzzle.

    El estado es una lista de 10 números, donde el 0 es
    el espacio vacío. Por ejemplo el estado:

           (1, 0, 2, 3, 4, 5, 6, 7, 8, 1)

    representa la situación:
       -------------
       | 1 |   | 2 |
       -------------
       | 3 | 4 | 5 |
       -------------
       | 6 | 7 | 8 |
       ------------

    Las acciones posibles son A = {N,S,E,O}

    """
    def __init__(self):
        self.acciones = {0: ['S', 'E'],
                         1: ['S', 'E', 'O'],
                         2: ['S', 'O'],
                         3: ['N', 'S', 'E'],
                         4: ['N', 'S', 'E', 'O'],
                         5: ['N', 'S', 'O'],
                         6: ['N', 'E'],
                         7: ['N', 'E', 'O'],
                         8: ['N', 'O']}

    def acciones_legales(self, estado):
        return self.acciones[estado[-1]]

    def sucesor(self, estado, accion):
        s = list(estado)
        ind = s[-1]
        bias = (-3 if accion is 'N' else
                3 if accion is 'S' else
                -1 if accion is 'O' else
                1)
        s[ind], s[ind + bias] = s[ind + bias], s[ind]
        s[-1] += bias
        return tuple(s)

    @staticmethod
    def dibuja(estado):
        """
        Dibuja un estado particular

        """
        cadena = "-------------\n"
        for i in range(3):
            for j in range(3):
                if estado[3 * i + j] > 0:
                    cadena += "| " + str(estado[3 * i + j]) + " "
                else:
                    cadena += "|   "
            cadena += "|\n-------------\n"
        return cadena


class Ocho_puzzle(busquedas.ProblemaBusqueda):

    def __init__(self, pos_ini, pos_meta=None):
        if pos_meta is None:
            pos_meta = (0, 1, 2, 3, 4, 5, 6, 7, 8, 0)

        super().__init__(pos_ini + (pos_ini.index(0),),
                         lambda pos: pos == pos_meta,
                         Modelo8puzzle())


def h_1(nodo):
    """
    Primera heurística para el 8-puzzle:

    Regresa el número de piezas mal colocadas.

    """
    return sum([1 for i in range(1, 9) if i != nodo.estado[i]])


def h_2(nodo):
    """
    Segunda heurística para el 8-puzzle:

    Regresa la suma de las distancias de manhattan
    de los numeros mal colocados.

    """
    return sum([abs(i % 3 - nodo.estado[i] % 3) +
                abs(i // 3 - nodo.estado[i] // 3)
                for i in range(9) if nodo.estado[i] != 0])


def probando(pos_ini):
    """
    Muestra el resultado de aplicar un tipo de búsqueda
    al problema del 8 puzzle con una posición inicial
    determinada.

    Por el momento muy manuel, solamente descomentar
    las búsquedas que se deseen realizar.

    Recuerda que las búsquedas no informadas pueden ser
    muy lentas.

    """
    print(Modelo8puzzle.dibuja(pos_ini))

    # ------- BFS -----------
    problema = Ocho_puzzle(pos_ini)
    tiB = time()
    solucion = busquedas.busqueda_ancho(problema)
    tfB = time()
    nBFS = solucion.nodos_visitados
    tB = tfB - tiB

    # ------- DFS -----------
    problema = Ocho_puzzle(pos_ini)
    tiD = time()
    solucion = busquedas.busqueda_profundo(problema, 50)
    tfD = time()
    nDFS = solucion.nodos_visitados
    tD = tfD - tiD

    # ------- IDS -----------
    problema = Ocho_puzzle(pos_ini)
    tiI = time()
    solucion = busquedas.busqueda_profundidad_iterativa(problema, 50)
    tfI = time()
    nIDS = solucion.nodos_visitados
    tI = tfI - tiI

    # ------- UCS -----------
    problema = Ocho_puzzle(pos_ini)
    tiU = time()
    solucion = busquedas.busqueda_costo_uniforme(problema)
    tfU = time()
    nUCS = solucion.nodos_visitados
    tU = tfU - tiU

    # # ------- A* con h1 -----------
    problema = Ocho_puzzle(pos_ini)
    tiA1 = time()
    solucion = busquedas.busqueda_A_estrella(problema, h_1)
    tfA1 = time()
    nA1 = solucion.nodos_visitados
    tA1 = tfA1 - tiA1

    # # ------- A* con h2 -----------
    problema = Ocho_puzzle(pos_ini)
    tiA2 = time()
    solucion = busquedas.busqueda_A_estrella(problema, h_2)
    tfA2 = time()
    nA2 = solucion.nodos_visitados
    tA2 = tfA2 - tiA2

    genera_tabla(nBFS, nDFS, nIDS, nUCS, nA1, nA2, tB, tD, tI, tU, tA1, tA2)


def genera_tabla(nBFS, nDFS, nIDS, nUCS, nA1, nA2, tB, tD, tI, tU, tA1, tA2):
    print('-' * 167)
    print('-' * 20, "BFS".center(20), "DFS".center(20), "IDS".center(20),
          "UCS".center(20), "H1".center(20), "H2".center(20), '-'*20)
    print()
    print('Nodos exp'.center(20), str(nBFS).center(20), str(nDFS).center(20),
          str(nIDS).center(20), str(nUCS).center(20), str(nA1).center(20),
          str(nA2).center(20))
    print()
    print('tiempo(s)'.center(20), str(format(tB, '.10f')).center(20),
          str(format(tD, '.10f')).center(20),
          str(format(tI, '.10f')).center(20),
          str(format(tU, '.10f')).center(20),
          str(format(tA1, '.10f')).center(20),
          str(format(tA2, '.10f')).center(20))
    print('-' * 167)


if __name__ == "__main__":

    probando((1, 0, 2, 3, 4, 5, 6, 7, 8))

    print("\n\n\ny con otro problema de 8 puzzle")
    probando((5, 1, 3, 4, 0, 2, 6, 7, 8))

    print("\n\n\ny por último")
    probando((1, 7, 8, 2, 3, 4, 5, 6, 0))
