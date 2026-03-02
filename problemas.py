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
    def __init__(self, N):
        self.N = N

    def acciones(self, estado):
        acciones = []
        if estado + 1 <= self.N:
            acciones.append(('pie', estado + 1))
        if estado * 2 <= self.N:
            acciones.append(('camion', estado * 2))
        return acciones

    def sucesor(self, estado, accion):
        if accion[0] == 'pie':
            return (accion[1], 1)
        elif accion[0] == 'camion':
            return (accion[1], 2)

    def terminal(self, estado):
        return estado == self.N

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Estado: {estado}"


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Esta heurística siempre devueve 0, ya que el costo real
    nunca puede ser negativo. Así que sí es admisible, porque
    nunca sobrestima el costo real para llegar al objetivo.

    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(N):
    """
    Esta heurística calcula (N - x) / 2, donde x es el estado actual
    y N es la meta.

    La idea es que todavía faltan N - x posiciones para llegar al
    objetivo. Como existe la opción de usar el camión mágico, que
    permite avanzar más rápido que ir solo a pie, divido entre 2
    para que la estimación no sea tan grande.
    """
    def h(nodo):
        x = nodo.estado
        return max(0, (N - x) / 2)
    return h

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """

    estado_objetivo = (
        'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', #Cara blanca
        'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', #Cara roja
        'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', #Cara azul
        'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', 'V', #Cara verde
        'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', #Cara amarilla
        'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'  #Cara naranja
    )

    def __init__(self, estado_inicial, estado_objetivo):
        self.estado_inicial = estado_inicial
        self.estado_objetivo = estado_objetivo

    def acciones(self, estado):
        return [
            "U", "U'", "U2",
            "D", "D'", "D2",
            "R", "R'", "R2",
            "L", "L'", "L2",
            "F", "F'", "F2",
            "B", "B'", "B2"
            ]

    """
    Mapeo de las caras del cubo:

    Cara U:         Cara D:
    0  1  2         9  10 11
    3  4  5         12 13 14
    6  7  8         15 16 17

    Cara R:         Cara L:
    18 19 20        27 28 29
    21 22 23        30 31 32
    24 25 26        33 34 35

    Cara F:         Cara B:
    36 37 38        45 46 47
    39 40 41        48 49 50
    42 43 44        51 52 53

    """

    def sucesor(self, estado, accion):
        rotaciones = {
            "U": self.U,
            "U'": self.U_prima,
            "U2": self.U2,
            "D": self.D,
            "D'": self.D_prima,
            "D2": self.D2,
            "R": self.R,
            "R'": self.R_prima,
            "R2": self.R2,
            "L": self.L,
            "L'": self.L_prima,
            "L2": self.L2,
            "F": self.F,
            "F'": self.F_prima,
            "F2": self.F2,
            "B": self.B,
            "B'": self.B_prima,
            "B2": self.B2
        }
        return rotaciones[accion](estado), 1

    def terminal(self, estado):
        return estado == self.estado_objetivo

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        print("Estado actual:")
        for i in range(0, 54, 9):
            print(" ".join(estado[i:i+9]))
        print()

    # --------------- Movimientos de U

    def U(self, estado):
        nuevo = list(estado)
        # Rotación de la cara U
        nuevo[0] = estado[6]
        nuevo[1] = estado[3]
        nuevo[2] = estado[0]
        nuevo[3] = estado[7]
        nuevo[4] = estado[4]
        nuevo[5] = estado[1]
        nuevo[6] = estado[8]
        nuevo[7] = estado[5]
        nuevo[8] = estado[2]

        # F a R
        nuevo[18] = estado[36]
        nuevo[19] = estado[37]
        nuevo[20] = estado[38]
        # R a B
        nuevo[47] = estado[18]
        nuevo[46] = estado[19]
        nuevo[45] = estado[20]
        # B a L
        nuevo[27] = estado[47]
        nuevo[28] = estado[46]
        nuevo[29] = estado[45]
        # L a F
        nuevo[36] = estado[27]
        nuevo[37] = estado[28]
        nuevo[38] = estado[29]
        return tuple(nuevo)

    def U_prima(self, estado):
        return self.U(self.U(self.U(estado))) 
    
    def U2(self, estado):
        return self.U(self.U(estado))
    
    # --------------- Movimientos de D
    
    def D(self, estado):
        nuevo = list(estado)
        # Rotación de la cara D
        nuevo[9]  = estado[15]
        nuevo[10] = estado[12]
        nuevo[11] = estado[9]
        nuevo[12] = estado[16]
        nuevo[13] = estado[13]
        nuevo[14] = estado[10]
        nuevo[15] = estado[17]
        nuevo[16] = estado[14]
        nuevo[17] = estado[11]

        #F a L
        nuevo[33] = estado[42]
        nuevo[34] = estado[43]
        nuevo[35] = estado[44]
        #L a B
        nuevo[51] = estado[33]
        nuevo[52] = estado[34]
        nuevo[53] = estado[35]
        #B a R
        nuevo[24] = estado[51]
        nuevo[25] = estado[52]
        nuevo[26] = estado[53]
        #R a F
        nuevo[42] = estado[24]
        nuevo[43] = estado[25]
        nuevo[44] = estado[26]
        return tuple(nuevo)
    
    def D_prima(self, estado):
        return self.D(self.D(self.D(estado)))

    def D2(self, estado):
        return self.D(self.D(estado))
    
    # --------------- Movimientos de R

    def R(self, estado):
        nuevo = list(estado)
        # Rotación de la cara R
        nuevo[18] = estado[24]
        nuevo[19] = estado[21]
        nuevo[20] = estado[18]
        nuevo[21] = estado[25]
        nuevo[22] = estado[22]
        nuevo[23] = estado[19]
        nuevo[24] = estado[26]
        nuevo[25] = estado[23]
        nuevo[26] = estado[20]

        # U a F
        nuevo[38] = estado[2]
        nuevo[41] = estado[5]
        nuevo[44] = estado[8]
        # F a D
        nuevo[11] = estado[38]
        nuevo[14] = estado[41]
        nuevo[17] = estado[44]
        # D a B 
        nuevo[45] = estado[17]
        nuevo[48] = estado[14]
        nuevo[51] = estado[11]
        # B a U 
        nuevo[2]  = estado[51]
        nuevo[5]  = estado[48]
        nuevo[8]  = estado[45]
        return tuple(nuevo)

    def R_prima(self, estado):
        return self.R(self.R(self.R(estado)))

    def R2(self, estado):
        return self.R(self.R(estado))

    # --------------- Movimientos de L

    def L(self, estado):
        nuevo = list(estado)
        # Rotación de la cara L
        nuevo[27] = estado[33]
        nuevo[28] = estado[30]
        nuevo[29] = estado[27]
        nuevo[30] = estado[34]
        nuevo[31] = estado[31]
        nuevo[32] = estado[28]
        nuevo[33] = estado[35]
        nuevo[34] = estado[32]
        nuevo[35] = estado[29]

        # U a F
        nuevo[36] = estado[0]
        nuevo[39] = estado[3]
        nuevo[42] = estado[6]
        # F a D
        nuevo[9]  = estado[36]
        nuevo[12] = estado[39]
        nuevo[15] = estado[42]
        # D a B 
        nuevo[53] = estado[15]
        nuevo[50] = estado[12]
        nuevo[47] = estado[9]
        # B a U 
        nuevo[0]  = estado[47]
        nuevo[3]  = estado[50]
        nuevo[6]  = estado[53]
        return tuple(nuevo)

    def L_prima(self, estado):
        return self.L(self.L(self.L(estado)))

    def L2(self, estado):
        return self.L(self.L(estado))

    # --------------- Movimientos de F

    def F(self, estado):
        nuevo = list(estado)
        # Rotación de la cara F
        nuevo[36] = estado[42]
        nuevo[37] = estado[39]
        nuevo[38] = estado[36]
        nuevo[39] = estado[43]
        nuevo[40] = estado[40]
        nuevo[41] = estado[37]
        nuevo[42] = estado[44]
        nuevo[43] = estado[41]
        nuevo[44] = estado[38]

        # U a R
        nuevo[18] = estado[6]
        nuevo[21] = estado[7]
        nuevo[24] = estado[8]
        # R a D 
        nuevo[9]  = estado[24]
        nuevo[10] = estado[21]
        nuevo[11] = estado[18]
        # D a L 
        nuevo[35] = estado[9]
        nuevo[32] = estado[10]
        nuevo[29] = estado[11]
        # L a U
        nuevo[6]  = estado[29]
        nuevo[7]  = estado[32]
        nuevo[8]  = estado[35]
        return tuple(nuevo)
    
    def F_prima(self, estado):
        return self.F(self.F(self.F(estado)))

    def F2(self, estado):
        return self.F(self.F(estado))

    # --------------- Movimientos de B

    def B(self, estado):
        nuevo = list(estado)
        # Rotación de la cara B
        nuevo[45] = estado[51]
        nuevo[46] = estado[48]
        nuevo[47] = estado[45]
        nuevo[48] = estado[52]
        nuevo[49] = estado[49]
        nuevo[50] = estado[46]
        nuevo[51] = estado[53]
        nuevo[52] = estado[50]
        nuevo[53] = estado[47]

        # U a L (invertido)
        nuevo[27] = estado[2]
        nuevo[30] = estado[1]
        nuevo[33] = estado[0]
        # L a D
        nuevo[15] = estado[27]
        nuevo[16] = estado[30]
        nuevo[17] = estado[33]
        # D a R (invertido)
        nuevo[20] = estado[15]
        nuevo[23] = estado[16]
        nuevo[26] = estado[17]
        # R a U
        nuevo[0]  = estado[20]
        nuevo[1]  = estado[23]
        nuevo[2]  = estado[26]
        return tuple(nuevo)

    def B_prima(self, estado):
        return self.B(self.B(self.B(estado)))

    def B2(self, estado):
        return self.B(self.B(estado))

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Heurística que siempre devuelve 0, y as admisible ya que
    nunca sobreestima el costo para llegar al objetivo.
    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Esta heurística cuenta cuántas piezas están fuera de su lugar
    comparando el estado actual con el estado objetivo.

    La idea es que mientras más piezas estén desordenadas,
    más movimientos podrían ser necesarios para resolver el cubo.
    Y como en un solo movimiento se pueden acomodar varias piezas 
    al mismo tiempo, por lo que divido el total entre 8 para que 
    la estimación no sea demasiado grande.
    """
    objetivo = PbCuboRubik.estado_objetivo
    return sum(1 for i in range(54) if nodo.estado[i] != objetivo[i]) / 8


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
    N = 10
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico( N )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    h2 = h_2_camion_magico(N)
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h2)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    estado_resuelto = PbCuboRubik.estado_objetivo
    problema_rubik = PbCuboRubik(estado_resuelto, estado_resuelto)
    pos_inicial_rubik = problema_rubik.U(estado_resuelto)  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema_rubik = PbCuboRubik(pos_inicial_rubik, estado_resuelto)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema_rubik, pos_inicial_rubik, h_1_problema_1, h_2_problema_1)

    """
    Conclusión:
    En ambos problemas, la heurística h2 es dominante sobre h1 debido que devuelve 
    valores mayores o iguales para todos los estados, además de reducir la cantidad
    de nodos expandidos en la búsqueda.
    """