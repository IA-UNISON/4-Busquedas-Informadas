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

        h(s) = número de stickers de colores fuera de su posición objetivo

    donde s es el estado actual del cubo.

    La heurística cuenta cuántos stickers de colores no coinciden con el color
    que deberían tener en el estado meta.

    Esta heurística es admisible porque nunca sobreestima el costo real
    para llegar a la meta. Cada movimiento del cubo puede corregir varios
    stickers al mismo tiempo, por lo que el número de stickers de colores mal
    colocados siempre es una cota inferior del número real de movimientos
    necesarios para resolver el cubo.
    """
    problema = nodo.problema
    estado = nodo.estado

    return sum(1 for i in range(54)
               if estado[i] != problema.meta[i])


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
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico( 100 )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    # pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    # problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    