#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
import math

# lo hard codee porque las heuristicas solo reciben el nodo
# y no quise mover mucho la estructura de los metodos
META_CAMION = 161

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
        self.meta = N

    def acciones(self, estado):
        acciones = []

        if estado + 1 <= self.meta:
            acciones.append('caminar')

        if estado * 2 <= self.meta:
            acciones.append('camion')

        return acciones

    def sucesor(self, estado, accion):
        if accion == 'caminar':
            return estado + 1, 1
        elif accion == 'camion':
            return estado * 2, 2

    def terminal(self, estado):
        return estado == self.meta

    # no entendi para que tendria que ser estatico entonces lo quite, 
    # aparte queria usar self.meta
    def bonito(self, estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posición actual: {estado}, meta: {self.meta}, faltan {self.meta - estado} metros"

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    0 siempre es una heuristica admisible.
    Ademas no se me ocurre nada mas aparte de la 
    que use en h_2 !
    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Esta es cuantas veces tengo que multiplicar por 2, para llegar
    de la posicion a la meta. Hace floor() para que no sobreestime.

    Explora algunos nodos menos.
    """
    actual = nodo.estado
    dupes = math.log2(META_CAMION / actual)
    costo = dupes * 2
    return costo

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    El estado es una tupla con 54 numeros, y cada
    numero es tambien, un color de 0 a 5

    Cara U (0-8):    Cara D (9-17):   Cara F (18-26):

    0 1 2            9  10 11         18 19 20
    3 4 5            12 13 14         21 22 23
    6 7 8            15 16 17         24 25 26

    Cara B (27-35):  Cara R (36-44):  Cara L (45-53):

    27 28 29         36 37 38         45 46 47
    30 31 32         39 40 41         48 49 50
    33 34 35         42 43 44         51 52 53
    
    0 = blanco(U), 
    1 = amarillo(D), 
    2 = rojo(F), 
    3 = naranja(B), 
    4 = verde(R), 
    5 = azul(L)
    
    El estado resuelto lo dibuje abajo, en su declaracion
    
    """

    MOVIMIENTOS = {
        'U': [
            (0,2,8,6), (1,5,7,3),                           # el primer parentesis son las esquinas, el segundo las aristas
            (18,36,27,45), (19,37,28,46), (20,38,29,47)     # estas son los 12 colores (3 por cara) de las 4 caras q estan pegadas a la que se mueve
        ],                                                  # un ciclo hace (0, 2, 8, 6) -> (6, 0, 2, 8), por ejemplo
        'D': [                                              # esto esta dibujado arriba por si no se entiende
            (9,11,17,15), (10,14,16,12),
            (24,48,33,42), (25,49,34,43), (26,50,35,44)
        ],
        'F': [
            (18,20,26,24), (19,23,25,21),
            (6,36,17,45), (7,39,16,48), (8,42,15,51)
        ],
        'B': [
            (27,29,35,33), (28,32,34,30),
            (0,47,11,38), (1,50,10,41), (2,53,9,44)  
        ],
        'R': [
            (36,38,44,42), (37,41,43,39),
            (2,27,15,20), (5,30,12,23), (8,33,9,26)  
        ],
        'L': [
            (45,47,53,51), (46,50,52,48),
            (0,18,11,35), (3,21,14,32), (6,24,17,29) 
        ],
    }

    ESTADO_RESUELTO = tuple(color for color in range(6) for _ in range(9))
    """
    ^ esto genera

    (0,0,0,0,0,0,0,0,0,  # cara U, color 0 (blanco)
    1,1,1,1,1,1,1,1,1,   # cara D, color 1 (amarillo)
    ,2,2,2,2,2,2,2,2,    # cara F, color 2 (rojo)
    3,3,3,3,3,3,3,3,3,   # cara B, color 3 (naranja)
    4,4,4,4,4,4,4,4,4,   # cara R, color 4 (verde)
    5,5,5,5,5,5,5,5,5)   # cara L, color 5 (azul)

    9 stickers por cara y todos del mismo color

    """
    

    def __init__(self, estado_inicial=None):
        if estado_inicial:
            self.estado_inicial = estado_inicial
        else:
            self.ESTADO_RESUELTO

    def _aplica_ciclos(self, estado, ciclos):
        lista = list(estado)
        for ciclo in ciclos:
            temp = lista[ciclo[-1]] 
            for i in range(len(ciclo)-1, 0, -1):
                lista[ciclo[i]] = lista[ciclo[i-1]]
            lista[ciclo[0]] = temp
        return tuple(lista)

    def acciones(self, estado):
        return ['U', "U'", 'U2',
                'D', "D'", 'D2',
                'F', "F'", 'F2',
                'B', "B'", 'B2',
                'R', "R'", 'R2',
                'L', "L'", 'L2']

    def sucesor(self, estado, accion):
        """
        aqui implemente los movimientos antihorarios y los dobles

        un movimiento antihorario (U' por ejemplo) tambien es 
        simplemente, un movimiento horario 3 veces

        el doble pues es dos veces (U2 por ejemplo)
        """
        cara = accion[0]  # 'U', 'D', 'F', 'B', 'R' o 'L'
        ciclos = self.MOVIMIENTOS[cara]

        if accion.endswith("'"):
            nuevo = self._aplica_ciclos(estado, ciclos)
            nuevo = self._aplica_ciclos(nuevo, ciclos)
            nuevo = self._aplica_ciclos(nuevo, ciclos)
        elif accion.endswith('2'):
            nuevo = self._aplica_ciclos(estado, ciclos)
            nuevo = self._aplica_ciclos(nuevo, ciclos)
        else:
            nuevo = self._aplica_ciclos(estado, ciclos)

        return nuevo, 1

    def terminal(self, estado):
        return estado == self.ESTADO_RESUELTO

    @staticmethod
    def bonito(estado):
        """
        Imprime el cubo asi:
                U U U
                U U U
                U U U
        L L L   F F F   R R R   B B B
        L L L   F F F   R R R   B B B
        L L L   F F F   R R R   B B B
                D D D
                D D D
                D D D

        aqui y en aplica_ciclos me ayudo claude !
        """
        nombres = ['U','D','F','B','R','L'] 
        caras = [estado[i*9:(i+1)*9] for i in range(6)]
        colores = {0:'W', 1:'Y', 2:'R', 3:'O', 4:'G', 5:'B'}
        c = [[colores[x] for x in cara] for cara in caras]

        U, D, F, B, R, L = c
        lineas = [
            f"                       {U[0]} {U[1]} {U[2]}",
            f"                       {U[3]} {U[4]} {U[5]}",
            f"                       {U[6]} {U[7]} {U[8]}",
            f"{L[0]} {L[1]} {L[2]}   {F[0]} {F[1]} {F[2]}   {R[0]} {R[1]} {R[2]}   {B[0]} {B[1]} {B[2]}",
            f"{L[3]} {L[4]} {L[5]}   {F[3]} {F[4]} {F[5]}   {R[3]} {R[4]} {R[5]}   {B[3]} {B[4]} {B[5]}",
            f"{L[6]} {L[7]} {L[8]}   {F[6]} {F[7]} {F[8]}   {R[6]} {R[7]} {R[8]}   {B[6]} {B[7]} {B[8]}",
            f"                       {D[0]} {D[1]} {D[2]}",
            f"                       {D[3]} {D[4]} {D[5]}",
            f"                       {D[6]} {D[7]} {D[8]}",
        ]
        return "\n".join(lineas)
 

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
    solucion1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)

    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados)
          + "\n")

    plan = solucion1.genera_plan()
    for estado, accion, costo in plan:
        print(f"{problema.bonito(estado)} | acción: {accion} | costo: {costo}")

    print('\nA* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados)
          + "\n")
    
    plan = solucion1.genera_plan()
    for estado, accion, costo in plan:
        print(f"{problema.bonito(estado)} | acción: {accion} | costo: {costo}")
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    # pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    # problema = PbCamionMagico( META_CAMION )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    # pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    # problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    
    cubo = PbCuboRubik()

    for movimiento in ['U', 'D', 'F', 'B', 'R', 'L']:
        estado = cubo.ESTADO_RESUELTO
        for _ in range(4):
            estado, _ = cubo.sucesor(estado, movimiento)
        print(f"{movimiento} x4 = resuelto: {estado == cubo.ESTADO_RESUELTO}")