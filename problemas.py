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
    def __init__(self, pos_inicial=1, meta=50):
        inicio_seguro = int(pos_inicial)
        meta_segura = int(meta)

        if inicio_seguro >= meta_segura:
            raise ValueError("Error: La meta debe ser mayor a la posición inicial.")

        if inicio_seguro < 1:
            raise ValueError("Error: La posición inicial debe ser al menos 1.")

        self.estado_inicial = (inicio_seguro, meta_segura)
        self.meta = meta_segura

    def acciones(self, estado):
        posicion_actual, meta = estado
        acciones = []

        if posicion_actual < meta:
            acciones.append("A pie")

        if (posicion_actual * 2) <= meta:
            acciones.append("Camion magico")

        return acciones

    def sucesor(self, estado, accion):
        posicion_actual, meta = estado

        if accion == 'A pie':
            return (posicion_actual + 1, meta), 1

        if accion == 'Camion magico':
            return (posicion_actual * 2, meta), 2

        raise ValueError(f"Accion no válida: {accion}")

    def terminal(self, estado):
        posicion_actual, meta = estado
        return posicion_actual == meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        posicion_actual, meta = estado
        return f"Posicion actual: {posicion_actual} | Meta: {meta}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    x, meta = nodo.estado

    h_caminar = meta - x

    x_temp = x
    costo = 0

    while x_temp * 2 <= meta:
        x_temp *= 2
        costo += 2

    costo += (meta - x_temp)

    return min(h_caminar, costo)

    """
    Justificación:
    La heurística estima el costo restante considerando dos escenarios: caminar toda la distancia hasta la meta o seguir 
    un plan en el que se usa el camión mágico mientras sea posible y luego se camina lo que falta, entonces, al tomar 
    el menor de ambos valores, se obtiene una estimación del tiempo mínimo bajo condiciones ideales.
    
    ¿Por qué es admisible?
    La política de las heurísticas se basa en que no sobreestime el costo real mínimo, y en ambas estimaciones son cotas
    inferiores al costo real: caminar nunca sobreestima y el plan con camión asume decisiones perfectas, por ende, como
    se toma el mínimo entre ellas, el valor resultante nunca supera el costo óptimo, por lo que no sobreestima.
    """


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

    x, meta = nodo.estado
    return (meta - x) // max(1, x)

    """
        Justificación:
        En esta heurística se piensa que mientras mas grande es x menos acciones faltan, es decir, estima cuántos 
        avances grandes, faltan para llegar a la meta, ya que, cuando la posicion es grande el camión hace que
        avance mas rápido, por lo tanto, los pasos disminuyen. La división calcula una aproximación
        del número mínimo de acciones necesarias.
        

        ¿Por qué es admisible?
        Porque solo toma en cuenta una proporción de la distancia restante e ignora dar pasos innecesarios entonces
        nunca sobreestima el tiempo para llegar a la meta haciendo que el valor calculado sea menor o igual al costo 
        real en todos los casos
        """

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
    solucion1, visitados1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2, visitados2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18)
          + str(visitados1).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(visitados2).center(20))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = (1,50) # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(pos_inicial=1, meta=50)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    #pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    #problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    #compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    