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
    def __init__(self, N):
        """
        @param N: pos meta
        """
        self.N = N
        
    
    def acciones(self, estado):
        """
        Regresa las acciones legales desde el estado actual
        """
        acciones = []

        # Siempre pse puede caminar si aun no llego a la meta
        if estado < self.N:
            acciones.append("caminar")

        # Se puede usar el camión mágico si no se pasa de la meta
        if 2 * estado <= self.N:
            acciones.append("camion")

        return acciones
    
    
    def sucesor(self, estado, accion):
        """
        Regresa el estado sucesor y el costo local
        """
        if accion == "caminar":
            return estado + 1, 1

        if accion == "camion":
            return 2 * estado, 2

        raise ValueError("Acción no válida")
    

    def terminal(self, estado):
        """
        Verifica si el estado es meta
        """
        return estado == self.N
    

    @staticmethod
    def bonito(estado):
        """
        Pretty print del estado
        """
        return f"Posición actual: {estado}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    
    """
    Heurística logarítmica entera para el problema del Camión Mágico.

    Se define como:

        h(x) = 2 * floor(log2(N / x))

    donde x es la posición actual y N es la posición meta.

    Esta heurística es admisible porque estima el costo suponiendo un caso
    ideal en el que siempre se puede duplicar el valor de x tantas veces
    como sea posible sin sobrepasar N.

    La función floor se utiliza para considerar únicamente el número entero
    de duplicaciones completas que pueden realizarse antes de alcanzar o
    superar la meta.

    Como en el problema real a veces es necesario caminar y no siempre se
    puede duplicar perfectamente hasta llegar exactamente a N, el costo real
    nunca será menor que esta estimación ideal. Por lo tanto, no sobreestima
    el costo y es admisible.
    
    Originalmente esta era h2 pero al calar me di cuenta que estaban al reves en cuestion resultados entonces las voltee
    y dan esto correctamente ahora:
    --------------------------------------------------
    Método         Costo         Nodos visitados   
    --------------------------------------------------

    A* con h1          13                 61         
    A* con h2          13                 32         
    --------------------------------------------------
    
    Con:
    pos_inicial = 1  
    problema = PbCamionMagico( 100 )
    
    Lo que si mientras mas se acerca la posición inicial a la meta, mas eficiente es esta heurística, 
    ya que se pueden hacer mas duplicaciones completas, lo que hace que h1 le pueda competir e igualar a h2.
    """
    
    problema = nodo.problema
    estado = nodo.estado
    
    if estado >= problema.N:
        return 0
    
    return 2 * math.floor(math.log2(problema.N / estado))

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Heurística logarítmica para el problema del Camión Mágico.

    Se define como:

        h(x) = 2 * log2(N / x)

    donde x es la posición actual y N es la posición meta.

    Esta heurística es admisible porque estima el costo suponiendo un caso
    ideal en el que siempre se puede duplicar exactamente hasta llegar a N,
    sin necesidad de caminar ni preocuparse por pasarse.

    Como en el problema real a veces es necesario caminar y no siempre se
    puede duplicar perfectamente, el costo real nunca será menor que esta
    estimación ideal Por lo tanto, no sobreestima el costo y es admisible.
    
    Esta es dominante respecto a h1 porque requiere aproximadamente la mitad de nodos visitados 
    para encontrar la solución óptima, aunque ambas heurísticas encuentran la misma solución óptima 
    con el mismo costo, h2 es más eficiente en términos de nodos visitados cuando la posicion inicial
    esta mas lejos de la meta.
    
    Ej. de ejecucion
    --------------------------------------------------
    Método         Costo         Nodos visitados   
    --------------------------------------------------

    A* con h1          9                  30         
    A* con h2          9                  10         
    --------------------------------------------------
    
    Con:
    pos_inicial = 99  
    problema = PbCamionMagico( 1600 )
    
    --------------------------------------------------
    Método         Costo         Nodos visitados   
    --------------------------------------------------

    A* con h1          30                 31         
    A* con h2          30                 31         
    --------------------------------------------------
    
    Con:
    pos_inicial = 70  
    problema = PbCamionMagico( 100 )
    """
    
    problema = nodo.problema
    estado = nodo.estado

    if estado >= problema.N:
        return 0

    return 2 * math.log2(problema.N / estado)



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
        self.estado_inicial = estado_inicial
        self.meta = tuple(sum(([i] * 9 for i in range(6)), []))

        # Movimientos posibles, cada movimiento es una tupla de 4 tuplas, cada una con 4 posiciones a rotar en sentido horario
        self.movimientos = {

            "U": [(0,6,8,2),(1,3,7,5),
                  (18,9,45,36),
                  (19,10,46,37),
                  (20,11,47,38)],

            "R": [(9,15,17,11),(10,12,16,14),
                  (2,20,29,51),
                  (5,23,32,48),
                  (8,26,35,45)],

            "F": [(18,24,26,20),(19,21,25,23),
                  (6,38,27,9),
                  (7,41,28,12),
                  (8,44,29,15)],

            "D": [(27,33,35,29),(28,30,34,32),
                  (24,42,51,15),
                  (25,43,52,16),
                  (26,44,53,17)],

            "L": [(36,42,44,38),(37,39,43,41),
                  (0,45,27,18),
                  (3,48,30,21),
                  (6,51,33,24)],

            "B": [(45,51,53,47),(46,48,52,50),
                  (0,11,33,36),
                  (1,14,34,39),
                  (2,17,35,42)],
        }

    def acciones(self, estado):
        return ["U", "U'", "R", "R'", "F", "F'",
                "D", "D'", "L", "L'", "B", "B'"]

    # Funcion auxiliar para aplicar un movimiento, recibe una lista y una tupla de ciclos a rotar
    def _aplicar(self, s, ciclos):
        for a,b,c,d in ciclos:
            s[a], s[b], s[c], s[d] = s[d], s[a], s[b], s[c]

    def sucesor(self, estado, accion):
        nuevo = list(estado)

        if "'" in accion:
            base = accion[0]
            for _ in range(3):
                self._aplicar(nuevo, self.movimientos[base])
        else:
            self._aplicar(nuevo, self.movimientos[accion])

        return tuple(nuevo), 1

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        caras = ["U", "R", "F", "D", "L", "B"]
        salida = ""

        for i in range(6):
            salida += f"\nCara {caras[i]}:\n"
            cara = estado[i*9:(i+1)*9]
            for j in range(3):
                salida += " ".join(str(x) for x in cara[j*3:(j+1)*3]) + "\n"

        return salida
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    
    """
    Heurística simple para el problema del Cubo de Rubik 3x3.

    Se define como:

        h(s) = número de stickers de colores fuera de su posición objetivo / 8

    donde s es el estado actual del cubo.

    La heurística cuenta cuántos stickers no coinciden con el color
    que deberían tener en el estado meta y divide ese valor entre 8,
    ya que un solo movimiento del cubo puede afectar como máximo
    8 stickers.

    Esta heurística es admisible porque en el mejor caso cada movimiento
    podría corregir simultáneamente hasta 8 stickers mal colocados.
    Por lo tanto, el número de movimientos necesarios para resolver el
    cubo nunca puede ser menor que el número total de stickers mal
    colocados dividido entre 8.

    Como esta estimación nunca sobreestima el número real de movimientos
    requeridos, es admisible.
    """
    
    problema = nodo.problema
    estado = nodo.estado

    return sum(1 for i in range(54)
               if estado[i] != problema.meta[i]) / 8


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Heurística basada en aristas y esquinas para el Cubo de Rubik 3x3.

    Se define como:

        h(s) = (aristas fuera de lugar / 4) + (esquinas fuera de lugar / 4)

    donde se cuentan únicamente las piezas (no los stickers).

    Un movimiento del cubo puede afectar como máximo 4 aristas y 4 esquinas.
    Por lo tanto, el número mínimo de movimientos necesarios no puede ser
    menor que el número de piezas mal colocadas dividido entre 4.

    Esta heurística es admisible porque nunca sobreestima el número real
    de movimientos requeridos para alcanzar el estado meta.
    
    Y además es dominante sobre a h1 porque es mas informada y por lo tanto requiere menos 
    nodos visitados para encontrar la solución óptima.
    """

    problema = nodo.problema
    estado = nodo.estado

    # Índices de aristas 
    bordes = [1, 3, 5, 7,
              10, 12, 14, 16,
              19, 21, 23, 25,
              28, 30, 32, 34,
              37, 39, 41, 43,
              46, 48, 50, 52]

    # Índices de esquinas 
    esquinas = [0, 2, 6, 8,
                9, 11, 15, 17,
                18, 20, 24, 26,
                27, 29, 33, 35,
                36, 38, 42, 44,
                45, 47, 51, 53]

    bordes_fuera_lugar = sum(
        1 for i in bordes if estado[i] != problema.meta[i]
    )

    esquinas_fuera_lugar = sum(
        1 for i in esquinas if estado[i] != problema.meta[i]
    )

    return (bordes_fuera_lugar / 4) + (esquinas_fuera_lugar / 4)



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
          + str(nodos1).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(18) 
          + str(nodos2).center(20))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = 70  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico( 100 )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    pos_inicial = (0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,4,4,4,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,5,5,5,4,4,4,4,4,4,
                   1,1,1,5,5,5,5,5,5)  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCuboRubik( pos_inicial )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_problema_1, h_2_problema_1)
    
    # En teoria deberia de jalar pero el cubo de rubik es un problema muy grande y trone mi arch en el intento de correrlo
    # en local entonces confio en que en teoria estoy bien pq las heuristicas son admisibles y h2 es mas informada que h1
    # pero no lo puedo correr.