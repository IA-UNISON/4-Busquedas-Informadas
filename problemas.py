#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas

import math

# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):

    def __init__(self, N):
        self.N = N
        PbCamionMagico.N_GLOBAL = N
    def acciones(self, estado):
        acciones = []
        if estado + 1 <= self.N:
            acciones.append("caminar")
        if estado * 2 <= self.N:
            acciones.append("camion")
        return acciones

    def sucesor(self, estado, accion):
        if accion == "caminar":
            return (estado + 1, 1)   # ← ahora regresa tupla
        elif accion == "camion":
            return (estado * 2, 2)   # ← ahora regresa tupla

    def terminal(self, estado):
        return estado == self.N

    @staticmethod
    def bonito(estado):
        return f"Posición: {estado}"

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    estado = nodo.estado
    N = PbCamionMagico.N_GLOBAL
    return N - estado

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    estado = nodo.estado
    N = PbCamionMagico.N_GLOBAL

    if estado >= N:
        return 0

    # Mejor caso: alternar duplicar y caminar
    return (N - estado) // 2

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones(self, estado):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def terminal(self, estado):
        raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        raise NotImplementedError('Hay que hacerlo de tarea')
 

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



def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Camión mágico
    pos_inicial = 1
    problema = PbCamionMagico(100)
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)

    # Cubo Rubik (lo hacemos después)
    # pos_inicial = ...
    # problema = PbCuboRubik(...)
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)