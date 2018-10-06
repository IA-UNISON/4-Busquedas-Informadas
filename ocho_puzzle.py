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
    Primer heurística para el 8-puzzle:

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
    Muestra el resultado de aplicar un tipo de búsqeda
    al problema del 8 puzzle con una posición inicial
    determinada.

    Por el momento muy manuel, solamente descomentar
    las búsquedas que se deseen realizar.

    Recuerda que las búsquedas no informadas pueden ser
    muy lentas.

    """
    print(Modelo8puzzle.dibuja(pos_ini))

    # ------- BFS -----------
    #print("---------- Utilizando BFS -------------")
    #problema = Ocho_puzzle(pos_ini)
    #solucion = busquedas.busqueda_ancho(problema)
    #print(solucion)
    #print("Explorando {} nodos\n\n".format(solucion.nodos_visitados))

    # ------- DFS -----------
    #print("---------- Utilizando DFS -------------")
    #problema = Ocho_puzzle(pos_ini)
    #solucion = busquedas.busqueda_profundo(problema, 50)
    #print(solucion)
    #print("Explorando {} nodos\n\n".format(solucion.nodos_visitados))

    # ------- IDS -----------
    #print("---------- Utilizando IDS -------------")
    #problema = Ocho_puzzle(pos_ini)
    #solucion = busquedas.busqueda_profundidad_iterativa(problema, 50)
    #print(solucion)
    #print("Explorando {} nodos\n\n".format(solucion.nodos_visitados))

    # ------- UCS -----------
    #print("---------- Utilizando UCS -------------")
    #problema = Ocho_puzzle(pos_ini)
    #solucion = busquedas.busqueda_costo_uniforme(problema)
    #print(solucion)
    #print("Explorando {} nodos\n\n".format(solucion.nodos_visitados))

    # # ------- A* con h1 -----------
    print("---------- Utilizando A* con h1 -------------")
    problema = Ocho_puzzle(pos_ini)
    solucion = busquedas.busqueda_A_estrella(problema, h_1)
    print(solucion)
    print("Explorando {} nodos".format(solucion.nodos_visitados))

     # ------- A* con h2 -----------
    print("---------- Utilizando A* con h2 -------------")
    problema = Ocho_puzzle(pos_ini)
    solucion = busquedas.busqueda_A_estrella(problema, h_2)
    print(solucion)
    print("Explorando {} nodos".format(solucion.nodos_visitados))


if __name__ == "__main__":

    probando((1, 0, 2, 3, 4, 5, 6, 7, 8))

    print("\n\n\ny con otro problema de 8 puzzle")
    probando((5, 1, 3, 4, 0, 2, 6, 7, 8))

    print("\n\n\ny por último")
    probando((1, 7, 8, 2, 3, 4, 5, 6, 0))
