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


class Pb8Puzzle(busquedas.ProblemaBusqueda):
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

    El último número es la posición del espacio vacío, es decir, el índice del 0.

    Las acciones posibles son A = {N,S,E,O}

    """
    def __init__(self, meta = (1, 2, 3, 4, 5, 6, 7, 8, 0)):
        self.meta = meta[:]
        self.acciones_legales = {0: ['S', 'E'],
                         1: ['S', 'E', 'O'],
                         2: ['S', 'O'],
                         3: ['N', 'S', 'E'],
                         4: ['N', 'S', 'E', 'O'],
                         5: ['N', 'S', 'O'],
                         6: ['N', 'E'],
                         7: ['N', 'E', 'O'],
                         8: ['N', 'O']}

    def acciones(self, estado):
        return self.acciones_legales[estado[-1]]

    def sucesor(self, estado, accion):
        costo_local = 1
        s = list(estado[:])
        ind = s[-1]
        bias = (-3 if accion == 'N' else
                3 if accion == 'S' else
                -1 if accion == 'O' else
                1)
        s[ind], s[ind + bias] = s[ind + bias], s[ind]
        s[-1] += bias
        return tuple(s), costo_local
    
    def terminal(self, estado):
        return estado[:-1] == self.meta

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


def h_1(nodo):
    """
    Primer heurística para el 8-puzzle:
    Regresa el número de piezas mal colocadas.

    """
    return sum([1 for i in range(1, 9) if i != nodo.estado[i]])


def h_2(nodo):
    """
    Segunda heurística para el 8-puzzle:
    Regresa la suma de las distancias de manhattan de los numeros mal colocados.

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
    print(Pb8Puzzle.dibuja(pos_ini))
    problema = Pb8Puzzle()
    s0 = pos_ini[:] + (pos_ini.index(0),)  # Agrega la posición del espacio vacío al estado inicial

    print("---------- Utilizando BFS -------------")
    plan, nodos_visitados = busquedas.busqueda_ancho(problema, s0)
    print(plan)
    print(f"Explorando {nodos_visitados} nodos\n\n")

    print("---------- Utilizando DFS -------------")
    plan, nodos_visitados = busquedas.busqueda_profundo(problema, s0, 50)
    print(plan)
    print(f"Explorando {nodos_visitados} nodos\n\n")

    # ------- IDS -----------
    print("---------- Utilizando IDS -------------")
    plan, nodos_visitados = busquedas.busqueda_profundidad_iterativa(problema, s0, 50)
    print(plan)
    print(f"Explorando {nodos_visitados} nodos\n\n")

    # ------- UCS -----------
    print("---------- Utilizando UCS -------------")
    plan, nodos_visitados = busquedas.busqueda_costo_uniforme(problema, s0)
    print(plan)
    print(f"Explorando {nodos_visitados} nodos\n\n")

    print("---------- Utilizando A* con h1 -------------")
    solucion,nodos_visitados = busquedas.busqueda_A_estrella(problema, h_1, s0)
    print(solucion)
    print("Explorando {} nodos".format(nodos_visitados))

    print("---------- Utilizando A* con h2 -------------")
    solucion,nodos_visitados = busquedas.busqueda_A_estrella(problema, h_2, s0)
    print(solucion)
    print("Explorando {} nodos".format(nodos_visitados))


if __name__ == "__main__":

    probando((1, 0, 2, 3, 4, 5, 6, 7, 8))

    print("\n\n\ny con otro problema de 8 puzzle")
    probando((5, 1, 3, 4, 0, 2, 6, 7, 8))

    print("\n\n\ny por último")
    probando((1, 7, 8, 2, 3, 4, 5, 6, 0))
