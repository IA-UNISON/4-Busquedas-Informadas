#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas



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

#class PbCuboRubik(busquedas.ProblemaBusqueda):
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
#def h_1_problema_1(nodo):
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
#def h_2_problema_1(nodo):
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
    #pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    #problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    #compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    