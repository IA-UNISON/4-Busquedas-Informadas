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
class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    Estado: (x, N)
    Meta: x == N
    """
    def __init__(self, N):
        self.N = int(N)
        if self.N < 1:
            raise ValueError("N debe ser >= 1")

    def acciones(self, estado):
        x, N = estado
        acc = []
        if x < N:
            acc.append('caminar')
        if 2 * x <= N:
            acc.append('camion')
        return acc

    def sucesor(self, estado, accion):
        x, N = estado
        if accion == 'caminar':
            return (x + 1, N), 1
        elif accion == 'camion':
            return (2 * x, N), 2
        else:
            raise ValueError(f"Accion desconocida: {accion}")

    def terminal(self, estado):
        x, N = estado
        return x == N

    @staticmethod
    def bonito(estado):
        x, N = estado
        return f"Posición: {x} / Meta: {N}"


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    h1(x,N) = N - x

    Admisible: caminar todo lo que falta siempre logra la meta con costo N-x,
    entonces el costo óptimo desde (x,N) nunca es mayor que N-x. No sobreestima.
    """
    x, N = nodo.estado
    return max(0, N - x)

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    h2(x,N) = ceil((N - x)/2)

    Admisible (cota inferior):
    Aunque imagináramos que puedes avanzar 2 posiciones por cada 1 de costo (optimista),
    todavía necesitarías al menos ceil((N-x)/2) de costo para cubrir la diferencia.
    Como es optimista, no sobreestima al costo real: admisible.

    Nota: Es más informada que 0, pero no necesariamente domina a h1.
    """
    x, N = nodo.estado
    d = max(0, N - x)
    return (d + 1) // 2

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
    plan1, nodos1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    plan2, nodos2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)

    print('-' * 60)
    print('Método'.ljust(15) + 'Costo'.ljust(15) + 'Nodos visitados')
    print('-' * 60)
    print('A* con h1'.ljust(15) + str(plan1.costo if plan1 else None).ljust(15) + str(nodos1))
    print('A* con h2'.ljust(15) + str(plan2.costo if plan2 else None).ljust(15) + str(nodos2))
    print('-' * 60 + '\n')

if __name__ == "__main__":
    # Camión mágico: ejemplo
    N = 31
    problema = PbCamionMagico(N)
    pos_inicial = (1, N)

    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)