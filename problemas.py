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
    Los estados son una tupla con un número que representa la posición. 
    Las acciones legales son ['P', 'C'], 'P' es caminar a pie y 'C' es usar el camión.
    ----------------------------------------------------------------------------------
    """
    def acciones_legales(self, estado):
        return ['P','C']

    def sucesor(self, estado, accion):
        return (estado[0] + (1 if accion == 'P' else estado[0]),)

    def costo_local(self, estado, accion):
        return (1 if accion == 'P' else 2)

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        print("Posicion: " + str(estado[0]))
 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, N):
        def es_meta(estado):
            self.num_nodos += 1
            return (estado[0] == N)

        self.es_meta = es_meta
        self.x0 = (1,)
        self.modelo = CamionMagico()
        self.num_nodos = 0


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def heuristicas_cambion_magico(N):
    def h1(nodo):
        """
        DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
        PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
        --------------------------------------------------------------
        La idea de esta heurística es que por por ejemplo si estoy en 
        la posición x y debo llegar a la posición 2x, a excepcion de 
        cuando x es 1, el costo va a ser 2 al usar el camión.

        Si estoy en 3 y quiero llegar a 12 debo duplicar dos veces, por
        eso hago math.log(N/nodo.estado[0],2), luego lo multiplico por 2 
        porque ese es el costo de tomar el camión.

        Hago la condición de que esto solo sea cuando arg >= 1 porque si no 
        salen números negativos, que sería cuando N < nodo.estado[0], 
        en ese caso ya no se debería poder llegar a la meta.

        abs(N - nodo.estado[0]) estaba pensando que era porque cuando
        estoy despues de la mitad del camino, por ejemplo estoy en 9 y 
        quiero llegar a 16 no puedo duplicar, y que cuando me pasó de N
        siga aumentando o algo así, pero esto lo devuelvo nomas cuando
        me pasé de N, así que en realidad no tengo justificación, pero
        al correrlo el número de nodos explorados con N de 1 hasta 1000
        siempre es menor que con la heurística 0, asi que voy a suponer
        que probablemente si funcione pero no lo aseguro y no entiendo
        porque.
        """
        arg = N / nodo.estado[0]
        return (2*math.log(arg , 2) if arg > 1 else abs(N - nodo.estado[0]))
    # ------------------------------------------------------------
    #  Desarrolla otra política admisible.
    #  Analiza y di porque piensas que es (o no es) dominante una
    #  respecto otra política
    # ------------------------------------------------------------

    def h2(nodo):
        """
        DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
        PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
        ----------------------------------------------------------
        La idea de esta heurística es que para encontrar el camino
        mas corto de 1 hasta N es tomar el camino más corto de 1 
        hasta N/2, caminar un paso si N es impar y tomar el camión,
        
        Aunque si ya estoy después de N/2, por ejemplo si estoy en 
        9 y quiero llegar a 16, no puedo retroceder, asi que nomas
        me queda caminar.


        """
        estado = nodo.estado[0]    
        costo = 0
        x, y = N // 2 , N

        # cada iteración agrega el coste para ir de `x a `y
        while estado <= x and x > 1:
            costo += 2 + y % 2
            y = x
            x = x // 2

        return costo + y - estado # agrego el costo de caminar de `estado a `y

    return (h1, h2)




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
        raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        raise NotImplementedError('Hay que hacerlo de tarea')
 
 # ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """
    def __init__(self):
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



def compara_metodos(problema, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo 
    de la solución de varios métodos de búsqueda,

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 )
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(18)
          + str(solucion2.nodos_visitados - solucion1.nodos_visitados).center(20))
    print('-' * 50 + '\n')



if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste

    N = 3
    problema = PblCamionMágico(N)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    h1_camion_magico, h2_camion_magico = heuristicas_cambion_magico(N)
    compara_metodos(problema, h1_camion_magico, h2_camion_magico)

    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    # problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    