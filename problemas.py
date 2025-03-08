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
    def __init__(self, n):
        assert n >=1, "El número de pasajeros debe ser mayor o igual que 1"
        self.n = n

    def acciones_legales(self, estado):
        a = []
        if estado < self.n:
            a.append('camina')
        if 2 * estado <= self.n:
            a.append('pasa')
        return a
    
    def sucesor(self, estado, accion):
        if accion == 'camina':
            return estado + 1
        if accion == 'pasa':
            return 2 * estado
        raise ValueError('Acción no válida')

    def costo_local(self, estado, accion):
        if accion == 'camina':
            return 1
        if accion == 'pasa':
            return 2
        raise ValueError('Acción no válida')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Estado actual :  {estado} pasajeros"
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, n):
        assert n >=1, "El número de pasajeros debe ser mayor o igual que 1"
        self.estado_inicial = 1
        self.n = n
        self.modelo = CamionMagico(n)

    def es_meta(self, estado):
        """Verifca si el estado actual es meta"""
    
        return estado == self.n
    
    def acciones_legales(self, estado):
        """Devuelve las acciones legales"""
        return self.modelo.acciones_legales(estado)
    
    def sucesor(self, estado, accion):
        """Devuelve el estado sucesor"""
        return self.modelo.sucesor(estado, accion)
    
    def costo_local(self, estado, accion):
        """Devuelve el costo local"""
        return self.modelo.costo_local(estado, accion)
    

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    estado = nodo.estado
    n = nodo.problema.n
    pasos = 0

    while estado * 2 <= n:
        estado *= 2
        pasos += 1
    pasos += (n - estado)
    return pasos


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
    
    """
    Mejora sobre h_1: Permite caminar algunos pasos antes de empezar a duplicar,
    reduciendo el número total de movimientos en ciertos casos.
    """
    estado = nodo.estado
    n = nodo.problema.n
    pasos = 0
    
    # Opcionalmente caminar algunos pasos antes de duplicar
    while (estado % 2 != 0) and (estado < n):
        estado += 1
        pasos += 1
    
    # Ahora, realizar las duplicaciones
    while estado * 2 <= n:
        estado *= 2
        pasos += 1
    
    # Pasos restantes para llegar exactamente a N
    pasos += (n - estado)
    return pasos

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


if __name__ == "__main__":


    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    n = 20
    problema = PblCamionMágico(20)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # # Compara los métodos de búsqueda para el problema del cubo de rubik
    # # con las heurísticas que desarrollaste
    # problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    