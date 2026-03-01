#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

from math import log2
import math
import numpy as np
import busquedas
import random




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
    def __init__(self,s0=1,N=100):
        self.N=N
        self.s0=s0
        self.s=np.arange(s0,N+1)
        self.a=['caminar','camion']

    def acciones(self, estado):
        if estado == self.s[-1]:
            return []
        else:
            acciones = ['caminar']
            if 2*estado in self.s:
                acciones.append('camion')
            return acciones

    def sucesor(self, estado, accion):
        if accion == 'caminar':
            return (estado + 1),1 # el costo de caminar es 1 minuto
        elif accion == 'camion':
            return (2 * estado), 2 # el costo de usar el camión es 2 minutos
        

    def terminal(self, estado):
        if estado == self.s[-1]:
            return True

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return print('Posición actual: {}'.format(estado))
    
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def crear_h1_camion(problema):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

        La heurística que propongo es la siguiente:
        h(n) = log2(N / nodo.estado)

        La idea detrás de esta heurística es que el camión mágico puede llevarnos 
        a la posición 2x en un tiempo de 2 minutos, lo que significa que cada vez 
        que usamos el camión, podemos avanzar significativamente. La función 
        logarítmica refleja esta capacidad de avanzar rápidamente, ya que a 
        medida que nos acercamos a N, el valor de h(n) disminuye, indicando
        que estamos más cerca del objetivo."""

    def h(nodo):
        posicion = nodo.estado
        meta = problema.N

        if posicion >= meta:
            return 0

        return math.ceil(math.log2(meta / posicion))

    return h

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def crear_h2_camion(problema):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

        La heurística que propongo es la siguiente:
        h(n) = 0.5 * log2(N / nodo.estado)

        Esta heurística es más conservadora que la primera, ya que asigna un valor más bajo a los estados intermedios.
        Sin embargo, sigue siendo admisible porque cada movimiento puede avanzar al menos una posición, lo que significa
        que el número de movimientos necesarios para alcanzar N siempre será mayor o igual a h(n). No es dominante respecto
        a la primera porque puede subestimar el costo real en casos donde el camión mágico puede ser utilizado de manera más
        efectiva para avanzar rápidamente hacia el objetivo.
    """
    def h(nodo):
        posicion = nodo.estado
        meta = problema.N

        if posicion >= meta:
            return 0
        else:
            return 0.5*math.log2(meta / posicion)

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
    #Constantes de caras
    F=0 #Front
    U=1 #Up
    R=2 #Right
    B=3 #Back
    D=4 #Down
    L=5 #Left


    Colores = {
        0: 'BL', #blanco 
        1: 'RO', #rojo
        2: 'AZ', #azul
        3: 'AM', #amarillo
        4: 'NA', #naranja
        5: 'VE' #verde
    }


    def __init__(self,s0=None):
        #estado inicial, acciones, etc
        self.meta = np.array([np.full((3,3), i) for i in range(6)])
        self.a = ['F', 'U', 'R', 'B', 'D', 'L']  # Front, Up, Right, Back, Down, Left

        if s0 is None:
            self.s0 = self.revolver_cubo(self.meta)
        else:
            self.s0 = s0


    def acciones(self, estado):
        return self.a
        #Todas las acciones son posibles en cualquier estado.

    def sucesor(self, estado, accion):
        #Aquí se implementaría la lógica para rotar las caras del cubo según la acción dada.
        #Esto es bastante complejo y requiere una representación adecuada del estado del cubo.
        movimientos = {
            'F': self.rotar_frontal,
            'U': self.rotar_superior,
            'R': self.rotar_derecha,
            'B': self.rotar_trasera,
            'D': self.rotar_inferior,
            'L': self.rotar_izquierda
        }
        nuevo_estado = movimientos[accion](estado)
        return (nuevo_estado,1) # el costo de cada movimiento es 1
    
    def rotar_frontal(self, estado):
        # Implementa la lógica para rotar la cara frontal del cubo
        nuevo_estado = np.copy(estado)

        #rotar la cara frontal
        nuevo_estado[self.F] = np.rot90(nuevo_estado[self.F], -1)  # Rotar la cara frontal en sentido horario

        #rotar las filas/columnas adyacentes
        nuevo_estado[self.U][2, :] = estado[self.L][:, 2][::-1]  # La fila inferior de U se convierte en la columna derecha de L (invertida)
        nuevo_estado[self.R][:, 0] = estado[self.U][2, :]
        nuevo_estado[self.D][0, :] = estado[self.R][:, 0]
        nuevo_estado[self.L][:, 2] = estado[self.D][0, :][::-1]  # Invertir la fila inferior de D antes de asignarla a L
        return nuevo_estado

    def rotar_superior(self, estado):
        # Implementa la lógica para rotar la cara superior del cubo
        nuevo_estado = np.copy(estado)
        #rotar la cara frontal
        nuevo_estado[self.U] = np.rot90(nuevo_estado[self.U], -1)  # Rotar la cara superior en sentido horario

        #rotar las filas/columnas adyacentes
        temp = estado[self.F][0, :].copy()

        nuevo_estado[self.F][0, :] = estado[self.R][0, :]
        nuevo_estado[self.R][0, :] = estado[self.B][0, :]
        nuevo_estado[self.B][0, :] = estado[self.L][0, :]
        nuevo_estado[self.L][0, :] = temp
        return nuevo_estado
    
    def rotar_derecha(self, estado):
        # Implementa la lógica para rotar la cara derecha del cubo
        nuevo_estado = np.copy(estado)
        #rotar la cara derecha
        nuevo_estado[self.R] = np.rot90(nuevo_estado[self.R], -1)

    
        #rotar las filas/columnas adyacentes
        temp = estado[self.U][:, 2].copy()

        nuevo_estado[self.U][:, 2] = estado[self.B][:, 0][::-1]
        nuevo_estado[self.B][:, 0] = estado[self.D][:, 2][::-1]
        nuevo_estado[self.D][:, 2] = estado[self.F][:, 2]
        nuevo_estado[self.F][:, 2] = temp
        return nuevo_estado
    
    def rotar_trasera(self, estado):
        # Implementa la lógica para rotar la cara trasera del cubo
        nuevo_estado = np.copy(estado)
        #rotar la cara trasera
        nuevo_estado[self.B] = np.rot90(nuevo_estado[self.B], -1)
        #rotar las filas/columnas adyacentes
        nuevo_estado[self.U][0, :] = estado[self.R][2, :][::-1]  # Invertir la fila inferior de R antes de asignarla a U
        nuevo_estado[self.L][:, 0] = estado[self.U][0, :]
        nuevo_estado[self.D][2, :] = estado[self.L][:, 0][::-1]  # Invertir la columna izquierda de L antes de asignarla a D
        nuevo_estado[self.R][2, :] = estado[self.D][2, :]
        return nuevo_estado
    
    def rotar_inferior(self, estado):
        # Implementa la lógica para rotar la cara inferior del cubo
        nuevo_estado = np.copy(estado)
        #rotar la cara inferor
        nuevo_estado[self.D] = np.rot90(nuevo_estado[self.D], -1)
        #rotar las filas/columnas adyacentes
        nuevo_estado[self.F][2, :] = estado[self.L][2, :]
        nuevo_estado[self.R][2, :] = estado[self.F][2, :]
        nuevo_estado[self.B][2, :] = estado[self.R][2, :]
        nuevo_estado[self.L][2, :] = estado[self.B][2, :]
        return nuevo_estado
    
    def rotar_izquierda(self, estado):
        # Implementa la lógica para rotar la cara izquierda del cubo
        nuevo_estado = np.copy(estado)
        #rotar la cara izquierda
        nuevo_estado[self.L] = np.rot90(nuevo_estado[self.L], -1)
        #rotar las filas/columnas adyacentes
        nuevo_estado[self.U][:, 0] = estado[self.B][:, 2][::-1]  # Invertir la columna derecha de B antes de asignarla a U
        nuevo_estado[self.F][:, 0] = estado[self.U][:, 0]
        nuevo_estado[self.D][:, 0] = estado[self.F][:, 0]
        nuevo_estado[self.B][:, 2] = estado[self.D][:, 0][::-1]  # Invertir la columna izquierda de D antes de asignarla a B
        return nuevo_estado
        

    def terminal(self, estado):
        if np.array_equal(estado, self.meta):
            return True
        
    def clave_estado(self, estado):
        """
        Devuelve una clave hash para un estado dado, esto es, un valor que sea igual para estados iguales y diferente para estados diferentes.

        @param estado: Una tupla con un estado válido.
        @return: Un valor hash del estado.

        """
        return tuple(estado.flatten())

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        fila_a_str = lambda fila: ' '.join(PbCuboRubik.Colores[color] for color in fila)
        U = estado[0]
        D = estado[1]
        F = estado[2]
        B = estado[3]
        L = estado[4]
        R = estado[5]

        print("\n")

        # Cara superior
        for i in range(3):
            print(" " * 10 + fila_a_str(U[i]))

        print()

        # L F R B
        for i in range(3):
            print(
            fila_a_str(L[i]) + "   " +
                fila_a_str(F[i]) + "   " +
                fila_a_str(R[i]) + "   " +
                fila_a_str(B[i])
            )

        print()

        # Cara inferior
        for i in range(3):
            print(" " * 10 + fila_a_str(D[i]))
            print("\n")
    
    def revolver_cubo(self, estado, movimientos=2):
        estado_actual = estado.copy()
        
        for _ in range(movimientos):
            accion = random.choice(self.a)
            estado_actual, _ = self.sucesor(estado_actual, accion)
        
        return estado_actual
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def crear_h1_cubo(problema):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

        La heurística que propongo es la siguiente:
        h(n) = número de piezas mal colocadas

        La idea detrás de esta heurística es contar el número de piezas (aristas y esquinas) que no están en su posición correcta. 
        Esta heurística es admisible porque cada movimiento puede corregir como máximo una pieza mal colocada, lo que significa
         el número de piezas mal colocadas siempre será menor o igual al número real de movimientos necesarios para resolver el cubo.
    
    """
    def h(nodo):
        estado = nodo.estado
        objetivo = problema.meta
        
        piezas_mal = 0
        
        # Recorremos todas las posiciones excepto centros
        for cara in range(6):
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1:
                        continue
                    if estado[cara][i][j] != objetivo[cara][i][j]:
                        piezas_mal += 1
        
        return piezas_mal

    return h

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def crear_h2_cubo(problema):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

        La heurística que propongo es la siguiente:
        h(n) = número de stickers mal colocados

        La idea detrás de esta heurística es contar el número total de stickers que no están en su posición correcta. 
        Esta heurística es admisible porque cada movimiento puede corregir como máximo 8 stickers, lo que significa 
        que el número de stickers mal colocados siempre será menor o igual al número real de movimientos necesarios 
        para resolver el cubo. Sin embargo, no es dominante respecto a la primera porque puede sobreestimar el costo 
        real en casos donde muchas piezas están mal colocadas pero pueden ser corregidas con pocos movimientos.
    
    """
    def h(nodo):
        estado = nodo.estado
        objetivo = problema.s0
        
        stickers_mal = np.sum(estado != objetivo)
        
        return math.ceil(stickers_mal / 8)

    return h

def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1,visitados1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2,visitados2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(visitados1))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(visitados2))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PbCamionMagico(s0=1, N=100)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    pos_inicial = problema.s0  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    h1=crear_h1_camion(problema)
    h2=crear_h2_camion(problema)
    print("Comparando heurísticas para el problema del camión mágico:")
    compara_metodos(problema, pos_inicial, h1, h2)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema_cubo = PbCuboRubik()
    pos_inicial_cubo= problema_cubo.s0 # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS, SI ES None SE GENERA UNA ALEATORIA
    h1_cubo=crear_h1_cubo(problema_cubo)
    h2_cubo=crear_h2_cubo(problema_cubo)
    print("Comparando heurísticas para el problema del cubo de rubik:")
    compara_metodos(problema_cubo, pos_inicial_cubo, h1_cubo, h2_cubo)
    