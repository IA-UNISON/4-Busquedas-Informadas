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
        super().__init__()

    def acciones_legales(self, estado):
        # acciones = []
        # if estado * 2 <= self.N:
        #     acciones.append("camion")
        # if estado + 1 <= self.N: 
        #     acciones.append("pie")
        # return acciones
        return ['caminar', 'camion']

    def sucesor(self, estado, accion):
        x = estado[0]
        if accion == 'caminar':
            return (x + 1,)
        elif accion == 'camion':
            return (2 * x,)
        else:
            raise ValueError("Juégale bien, caminas o usas el camión, no hay de otra...")

    def costo_local(self, estado, accion):
        if accion == "caminar":
            return 1  
        if accion == "camion_magico":
            return 2

    @staticmethod
    def bonito(self, estado):
        """
        El prettyprint de un estado dado

        """
        print("-" * (self.N + 2))
        print(" ".join(str(i) if i <= self.N else " " for i in range(1, self.N + 1)))
        print(" " * (2 * (estado - 1)) + "🚛")
        print("-" * (self.N + 2))
 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, N):
        self.N = N 
        modelo = CamionMagico()
        estado_inicial = (1,)
        estados_objetivo = {(N,)}
        super().__init__(modelo, estado_inicial, estados_objetivo)


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo, N):
    """
    Esta heurística se basa en el tiempo mínimo caminando desde x hasta N.
    Es admisible porque caminar es la opción más lenta, y cualquier uso del
    camión reducirá o igualará el tiempo.
    """
    #problema = nodo.problema
    N = nodo.problema.N
    x_actual = nodo.estado[0]
    return max(N - x_actual, 0)


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo, N):
    """
    Esta heurística es sobre el tiempo usando el camión máximo posible y 
    luego caminando. Es admisible porque asume el mejor escenario posible con el camión.

    """
    #problema = nodo.problema
    N = nodo.problema.N
    x_actual = nodo.estado[0]
    if x_actual >= N:
        return 0
    k = 0
    while x_actual * (2 ** (k + 1)) <= N:
        k += 1
    tiempo_camion = 2 * k
    nueva_x = x_actual * (2 ** k)
    restante = N - nueva_x
    return tiempo_camion + restante

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
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')

def crear_heuristicas(N):
    def h1(nodo):
        current_x = nodo.estado[0]
        return max(N - current_x, 0)
    
    def h2(nodo):
        current_x = nodo.estado[0]
        if current_x >= N:
            return 0
        k = 0
        while current_x * (2 ** (k + 1)) <= N:
            k += 1
        return 2 * k + (N - current_x * (2 ** k))
    return h1, h2

if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    N = 15
    problema = PblCamionMágico(N)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    h_1, h_2 = crear_heuristicas(N)
    compara_metodos(problema, h_1, h_2)
    
    # # Compara los métodos de búsqueda para el problema del cubo de rubik
    # # con las heurísticas que desarrollaste
    # problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    