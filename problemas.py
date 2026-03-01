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
        self.x0 = 0
        self.meta = meta

    def acciones(self, estado):
        """
        @param estado: posicion actual
        @return: lista de acciones ["caminar", "camion"]
        """
        acciones= []
        if estado + 1 <= self.meta:
            acciones.append('caminar')
            
        if estado * 2 <= self.meta:
            acciones.append('camion')
        
        return acciones

    def sucesor(self, estado, accion):  
        if accion == 'caminar':
            return estado + 1, 1
        if accion == 'camion':
            return estado * 2, 2
        
        raise ValueError("Acción no válida")

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return print(f"posicion: {estado}")
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo, problema):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    Esta heuristica calcula el costo suponiendo que siempre se va usar el camion y que va a crecer de su posicion actual hasta la meta
    
    Esta heuristica es admisible porque nunca va a sobrestimar el costo real porque es muy optimista y asume que cada accion reduce la distancia exponencialmente y el costo real siempre sera mayor porque incluye los pasos adicionales
     
    """
    estado = nodo.estado
    meta = problema.meta
    
    if estado >= meta:
        return 0
    
    if estado == 0:
        return meta
    
    factor = meta / estado
    duplicaciones = math.ceil(math.log2(factor))
    
    return duplicaciones * 2


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo, problema):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Esta heuristica calcula el costo si usamos el camion todas las veces posibles sin pasarnos de la meta y luego caminamos el resto del camino caminando
    
    Es admisible porque solo usa el camion cuando no se pase de la meta, toma en cuenta el camino ideal en el que todo el trayecto se puede hacer en camion
    
    Esta heuristica es dominante a h_1 porque considera no solo usar el camion si no tambien el caminar por lo que esta mas cerca del costo real
    """
    estado = nodo.estado
    meta = problema.meta
    
    if estado >= meta:
        return 0
    
    n = 0
    pos = estado
    while pos * 2 <= meta:
        pos *= 2
        n += 1
    mejor_costo = n * 2 + (meta - pos)
    return mejor_costo

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
    problema.x0 = pos_inicial 
    
    h1 = lambda nodo: heuristica_1(nodo, problema)
    h2 = lambda nodo: heuristica_2(nodo, problema)
    
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, h1)
    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, h2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(19) 
          + str(nodos1).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(nodos2).center(17))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(50)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    #pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    #problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    #compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    