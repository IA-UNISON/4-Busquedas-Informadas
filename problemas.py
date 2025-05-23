#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
import numpy as np


# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------


class CamionMagico(busquedas.ModeloBusqueda):
    """
    ---------------------------------------------------------------------------------
     Supongamos que quiero trasladarme desde la posición discreta $1$ hasta
     la posicion discreta $N$ en una vía recta usando un camión mágico.

     Puedo trasladarme de dos maneras:
      1. A pie, desde el punto $x$ hasta el punto $x + 1$ en un tiempo de 1 minuto.
      2. Usando un camión mágico, desde el punto $x$ hasta el punto $2x$ con un tiempo
         de 2 minutos.

     Desarrollar la clase del modelo del camión mágico
    ----------------------------------------------------------------------------------

    """

    def __init__(self):
        self.acciones = ["W", "B"]

    def acciones_legales(self, estado):
        destino, posicion = estado
        if 2 * posicion <= destino:
            return self.acciones
        else:
            return ["W"]

    def sucesor(self, estado, accion):
        destino, posicion = estado
        if accion == "B":
            return (destino, 2 * posicion)
        else:
            return (destino, posicion + 1)

    def costo_local(self, estado, accion):
        if accion == "B":
            return 2
        else:
            return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        posicion, destino = estado
        print("pos = " + posicion + ", destino = " + destino)


# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------


class PblCamionMagico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """

    def __init__(self, estado_inicial):
        def meta(estado):
            destino, posicion = estado
            if destino == posicion:
                return True
            else:
                return False

        super().__init__(estado_inicial, meta, CamionMagico())


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------


def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    destino, posicion = nodo.estado
    heurisica_nodo = 0
    while posicion < destino:
        posicion *= 2
        heurisica_nodo += 1
    return heurisica_nodo


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------


def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    destino, posicion = nodo.estado
    if posicion > (destino / 2):
        return destino - posicion
    else:
        return 2


def h_3_camion_magico(nodo):
    h_1, h_2 = h_1_camion_magico(nodo), h_2_camion_magico(nodo)
    if h_1 > h_2:
        return h_1
    else:
        return h_2


def h_4_camion_magico(nodo):
    return min(h_1_camion_magico(nodo), h_2_camion_magico(nodo))


# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------


class CuboRubik(busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.

    https://en.wikipedia.org/wiki/Rubik%27s_Cube

    """

    def __init__(self):
        self.acciones = ["U", "D", "R", "F", "L", "B"]

    def acciones_legales(self, estado):
        return self.acciones

    def sucesor(self, estado, accion):
        raise NotImplementedError("Hay que hacerlo de tarea")

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        raise NotImplementedError("Hay que hacerlo de tarea")


# ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------


class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """

    def __init__(self, estado_ini):
        estado = []
        for i in range(1, 7):
            x = np.array([i, i, i, i, i, i, i, i, i])
            x = x.reshape((3, 3))
            estado.append(x)

        def meta(estado):
            raise NotImplementedError("Hay que hacerlo de tarea")


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0


def compara_metodos(problema, heuristica_1, heuristica_2, heuristica_3, heuristica_4):
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
    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2)
    solucion3 = busquedas.busqueda_A_estrella(problema, heuristica_3)
    solucion4 = busquedas.busqueda_A_estrella(problema, heuristica_4)

    print("-" * 50)
    print("Método".center(12) + "Costo".center(18) + "Nodos visitados".center(20))
    print("-" * 50 + "\n\n")
    print(
        "A* con h1".center(12)
        + str(solucion1.costo).center(20)
        + str(solucion1.nodos_visitados)
    )
    print(
        "A* con h2".center(12)
        + str(solucion2.costo).center(20)
        + str(solucion2.nodos_visitados)
    )
    print(
        "A* con h3".center(12)
        + str(solucion3.costo).center(20)
        + str(solucion3.nodos_visitados)
    )
    print(
        "A* con h4".center(12)
        + str(solucion4.costo).center(20)
        + str(solucion4.nodos_visitados)
    )
    print("-" * 50 + "\n\n")


if __name__ == "__main__":
    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PblCamionMagico((543, 1))  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(
        problema,
        h_1_camion_magico,
        h_2_camion_magico,
        h_3_camion_magico,
        h_4_camion_magico,
    )

    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    # problema = PblCuboRubik(XXXXXXXXXX)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
