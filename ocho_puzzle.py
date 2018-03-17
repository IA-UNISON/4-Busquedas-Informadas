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


def probando(pos_ini, tipo):
    """
    Muestra el resultado de aplicar un tipo de búsqeda
    al problema del 8 puzzle con una posición inicial
    determinada.

    Por el momento muy manual, solamente descomentar
    las búsquedas que se deseen realizar.

    Recuerda que las búsquedas no informadas pueden ser
    muy lentas.

    Tipo:
        0: busqueda_ancho,
        1: busqueda_profundo,
        2: busqueda_profundidad_iterativa,
        3: busqueda_costo_uniforme,
        4: busqueda_A_estrella con heuristica h1,
        5: busqueda_A_estrella con heuristica h2
    """
    print(Modelo8puzzle.dibuja(pos_ini))
    tipos = ["BFS", "DFS", "IDS", "UCS", "A* con h1", "A* con h2"]
    print("---------- Utilizando {} -------------".format(tipos[tipo]))
    problema = Ocho_puzzle(pos_ini)
    t_inicial = time()
    solucion = (busquedas.busqueda_ancho(problema) if tipo is 0 else
                busquedas.busqueda_profundo(problema, 50) if tipo is 1 else
                busquedas.busqueda_profundidad_iterativa(problema, 50) if tipo is 2 else
                busquedas.busqueda_costo_uniforme(problema) if tipo is 3 else
                busquedas.busqueda_A_estrella(problema, h_1) if tipo is 4 else
                busquedas.busqueda_A_estrella(problema, h_2))
    t_final = time()
    print(solucion)
    print("Explorando {} nodos".format(solucion.nodos_visitados))
    print("Tiempo: {} segundos".format(t_final-t_inicial))

if __name__ == "__main__":

    #probando((1, 0, 2, 3, 4, 5, 6, 7, 8), tipo=0)

    print("\n\n\ny con otro problema de 8 puzzle")
    probando((5, 1, 3, 4, 0, 2, 6, 7, 8), tipo=5)

    print("\n\n\ny por último")
    probando((1, 7, 8, 2, 3, 4, 5, 6, 0), tipo=5)


"""

    Estado inicial:  (5, 1, 3, 4, 0, 2, 6, 7, 8)

    |       Busqueda                |  Costo  |  Profundidad  |  Nodos Explorados  |   Tiempo   |

              Ancho                     14           14               4158             0.10 seg
            Profundo                    50           50              64951             1.80 seg
       Profundidad iterativa            14           14              17026             0.37 seg      
          Costo Uniforme                14           14               5240             0.31 seg
              A* h1                     14           14                298             0.02 seg
              A* h2                     14           14                 97             0.01 seg

    Estado inicial :  (1, 7, 8, 2, 3, 4, 5, 6, 0)            

    |       Busqueda                |  Costo  |  Profundidad  |  Nodos Explorados  |   Tiempo   |
    
              Ancho                     24           24             133152             4.28 seg
            Profundo                    50           50             162865             4.94 seg             
       Profundidad iterativa            24           24             883191            22.90 seg    
          Costo Uniforme                24           24             129515             9.62 seg
              A* h1                     24           24              17622             1.92 seg
              A* h2                     24           24               1677             0.25 seg

"""