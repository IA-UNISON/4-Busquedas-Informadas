#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

from math import log2
import math
import numpy as np
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
    def __init__(self,s,a,s0=1,N=100):
        self.N=N
        self.s0=s0
        self.s=np.arange(s0,N+1)
        self.a=['caminar','camion']

    def acciones(self, estado):
        if estado == self.s[-1]:
            return []
        else:
            acciones = ['caminar']
            if 2*estado in self.s:
                acciones.append('camion')
            return acciones

    def sucesor(self, estado, accion):
        if accion == 'caminar':
            return estado + 1
        elif accion == 'camion':
            return 2 * estado
        

    def terminal(self, estado):
        if estado == self.s[-1]:
            return True

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return print('Posición actual: {}'.format(estado))
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

        La heurística que propongo es la siguiente:
        h(n) = log2(N / nodo.estado)

        La idea detrás de esta heurística es que el camión mágico puede llevarnos 
        a la posición 2x en un tiempo de 2 minutos, lo que significa que cada vez 
        que usamos el camión, podemos avanzar significativamente. La función 
        logarítmica refleja esta capacidad de avanzar rápidamente, ya que a 
        medida que nos acercamos a N, el valor de h(n) disminuye, indicando
        que estamos más cerca del objetivo.

    """
    if nodo.estado >= nodo.problema.N:
        return 0
    else:
        return math.log2(nodo.problema.N / nodo.estado)   


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

        La heurística que propongo es la siguiente:
        h(n) = N - nodo.estado

        Esta heurística es admisible porque siempre sobreestima el costo real para llegar a la meta. 
        En el peor de los casos, si solo pudiéramos caminar, el costo sería exactamente N - nodo.estado, 
        lo que significa que esta heurística nunca sobrepasa la meta. Sin embargo, no es dominante 
        respecto a la primera porque no tiene en cuenta la capacidad del camión mágico para avanzar rápidamente
        por que puede llevar a sobrestimar significativamente el costo real.
    """
    if nodo.estado >= nodo.problema.N:
        return 0
    else:
        return nodo.problema.N - nodo.estado


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

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    