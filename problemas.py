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
    def __init__(self, meta):
        self.meta = meta
        PbCamionMagico.meta_global = meta

    def acciones(self, estado):
        acciones = []

        # Caminamos si no nos pasamos de la meta
        if estado + 1 <= self.meta:
            acciones.append("caminar")

        # Usamos el camion si podemos
        if estado * 2 <= self.meta:
            acciones.append("camion")

        return acciones

    def sucesor(self, estado, accion):

        # Aaqui regresamos tanto el estado en el que nos encontramos como el costo
        # de la accion
        if accion == "caminar":
            return estado + 1, 1
        
        if accion == "camion":
            return estado * 2, 2

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posicion actual: {estado}"

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Calcula cuantos pasos faltan para llegar a la meta
    si solo se pudiera caminar.

    Es admisible porque nunca sobreestima el costo real,
    ya que el camion magico puede hacer que el costo real
    sea incluso menor.

    """
    estado = nodo.estado
    meta = PbCamionMagico.meta_global
    return max(0, meta - estado)

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Estima el costo restante como el minimo numero de
    duplicaiones necesarias para alcanzar o superar la meta.

    es admisible porque solo considera el costo del camion
    e ignora los pasos de caminar.

    """
    estado = nodo.estado
    meta = PbCamionMagico.meta_global

    if estado >= meta:
        return 0

    duplicaciones = 0
    actual = estado

    while actual < meta:
        actual *= 2
        duplicaciones += 1

    return duplicaciones * 2

# Ninguna de las heuristicas domina a la otra porque existen estados
# en los que h1 produce una estimacion mayor que h2 y viceversa.

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    def __init__(self, estado_inicial):
        # Tenemos 6 caras
        self.meta = (True, True, True, True, True, True)
        self.inicial = estado_inicial

    def acciones(self, estado):
        return ["giro_F", "giro_R", "giro_U"]
    
    def sucesor(self, estado, accion):
        nuevo_estado = list(estado)

        #Cada giro funciona como un toggle
        if accion == "giro_F":
            nuevo_estado[0] = not nuevo_estado[0]
            nuevo_estado[1] = not nuevo_estado[1]
            nuevo_estado[2] = not nuevo_estado[2]

        elif accion == "giro_R":
            nuevo_estado[2] = not nuevo_estado[2]
            nuevo_estado[3] = not nuevo_estado[3]
            nuevo_estado[4] = not nuevo_estado[4]

        elif accion == "giro_U":
            nuevo_estado[4] = not nuevo_estado[4]
            nuevo_estado[5] = not nuevo_estado[5]
            nuevo_estado[0] = not nuevo_estado[0]

        return tuple(nuevo_estado), 1

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        caras = ["F", "B", "L", "R", "U", "D"]
        return " | ".join(f"{c}:{e}" for c, e in zip(caras, estado))
    
# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Cuenta cuantas caras estan en False.
    
    Es admisible porque cada movimiento puede corregir
    como maximo 3 caras a la vez. pero nunca sobreestima
    el costo minimo real.

    """
    return sum(1 for cara in nodo.estado if not cara)


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Divide las caras malas entre 3, porque cada giro
    afecta exactamente 3 caras.

    Es admisible porque en el mejor caso, cada movimiento
    corrige las 3 caras a la vez.

    """
    caras_mal = sum(1 for cara in nodo.estado if not cara)
    return math.ceil(caras_mal / 3)

# h1 domina a h2 porque h1 es siempre mayor o igual y h1 da una estimacion
# mas informativa

def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)

    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)

    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')

    print('A* con h1'.center(12)
          + str(solucion1.costo).center(18)
          + str(nodos1))

    print('A* con h2'.center(12)
          + str(solucion2.costo).center(18)
          + str(nodos2))

    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(20)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    pos_inicial = (False, False, False, True, True, True)  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCuboRubik(pos_inicial)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_problema_1, h_2_problema_1)
    