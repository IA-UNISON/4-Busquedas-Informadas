#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas




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
        self.n = n # posicion final

    def acciones_legales(self, estado):
        acciones = []
        if estado + 1 <= self.n:
             acciones.append("caminar")
        if estado * 2 <= self.n:
             acciones.append("camionMagico")
        return acciones
             

    def sucesor(self, estado, accion):
        if accion == "caminar":
             return estado + 1
        elif accion == "camionMagico":
             return estado * 2
        return estado

    def costo_local(self, estado, accion):
        if accion == "caminar":
             return 1
        elif accion == "camionMagico":
             return 2
        return float("inf")

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posición actual: {estado}"
 
class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self):
        self.N = N
        super().__init__(estado_inicial = 1, modelo = CamionMagico(N), meta = N)
    



def h_1_camion_magico(nodo):

    return (nodo.estado - 1) # el peor caso es moverse unicamente a pie

# ------------------------------------------------------------
#  h1: Esta política es admisible ya que no sobreestima el costo real, yo asumi que siempre
# nos estaremos moviendo de uno en uno entonces el costo estimado será la distancia lineal al objetivo
#

def h_2_camion_magico(nodo):
 
    return (nodo.estado -1) // 2 #

# ------------------------------------------------------------
#  h2: Esta política es admisible ya que tampoco sobreestima el costo real, el numero de movimientos que s eocupan
# aquí pensé en que la mitad del camino se puede hacer en saltos
#
# ------------------------------------------------------------
# Dominancia de una sobre otra: 
# h1 nomas considera movimientos de uno en uno y h2 se mueve de x a x+1 q toma 1 min o usa el camion magico de x a 2x y hace 2 min
# entonces si la distancia restante es muy grande es mejor duplicarlo con el camion magico y se reduce a la mitad con cada salto pero si
# el num es chico algunos pasos serán +1 pero la h2 aproxima los pasos justamente dividiendo.
# h2 es dominante sobre h1
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):

    
    
    def __init__(self):
        self.estado_inicial = tuple(range(54)) # una tupla con los numeros del 1 al 54 para simular las "casillas" del cubo

    def acciones_legales(self, estado):
        """
        En el cubo rubik se tienen 6 acciones legales por cada cara:
        - Rotar la cara hacia el frente (F), hacia atrás (B), hacia arriba (U), hacia abajo (D), hacia la izquierda (L), hacia la derecha (R).
        
        - F', B', U', D', L', R' -> rotación en sentido antihorario
        - F2, B2, U2, D2, L2, R2 -> rotación en 180 grados
        """

        caras = ['F', 'B', 'U', 'D', 'L', 'R']
        acciones = []

        for cara in caras:
             acciones.append(f"{cara}")
             acciones.append(f"{cara}'")
             acciones.append(f"{cara}2")

        return acciones
    

    def sucesor(self, estado, accion):
        """
        AL aplcar una acción de rotación, devuelve un nuevo estado.
        """

        nuevo_estado = estado[ : ]
        
        """
        caras = {
             'F' : [9, 10, 11, 12, 13, 14, 15, 16, 17]
             'B' : [27, 28, 29, 30, 31, 32, 33, 34, 35]
             'U' : [45, 46, 47, 48, 49, 50, 51, 52, 53]
             'L' : [0, 1, 2, 3, 4, 5, 6, 7, 8]
             'R' : [18, 19, 20, 21, 22, 23, 24, 25, 26]
             'D' : [36, 37, 38, 39, 40, 41, 42, 43, 44]
        }
        """

        #bordes que serán afectados por la rotación en sentido horario de la cara frontal
        bordes = { 
             'F' : [[51, 52, 53], [18, 21, 24], [36, 37, 38], [8, 5, 2]],
             'B' : [[45, 46, 47], [20, 23, 26], [42, 43, 44], [0, 3, 6]],
             'U' : [[36, 37, 38], [9, 10, 11], [18, 19, 20], [27, 28, 29]],
             'L' : [[0, 3, 6], [9, 18, 27], [45, 48, 51], [36, 39, 42]],
             'R' : [[2, 5, 8], [11, 20, 29], [47, 50, 53] [38, 41, 44]],
             'D' : [[45, 46, 47], [33, 34, 35], [24, 25, 26], [15, 16, 17]]
        }

        cara = accion[0]
        rotacion = accion[1:] if len(accion) > 1 else '' # 'para la rotación antihorario, 2 para la de 180 gradis

        borde1, borde2, borde3, borde4 = bordes[cara]

        #rotacion horaria
        if rotacion == '':
             temporal = [nuevo_estado[i] for i in borde1]
             for i in range(3):
                  nuevo_estado[borde2[i]] = temporal[i]
             temporal = [nuevo_estado[i] for i in borde2]
             for i in range(3):
                  nuevo_estado[borde3[i]] = temporal[i]
             temporal = [nuevo_estado[i] for i in borde3]
             for i in range(3):
                  nuevo_estado[borde4[i]] = temporal[i]
             temporal = [nuevo_estado[i] for i in borde4]
             for i in range(3):
                  nuevo_estado[borde1[i]] = temporal[i]


        elif rotacion == "'":
             temporal = [nuevo_estado[i] for i in borde1]
             for i in range(3):
                  nuevo_estado[borde4[i]] = temporal[i]
             temporal = [nuevo_estado[i] for i in borde4]
             for i in range(3):
                  nuevo_estado[borde3[i]] = temporal[i]
             temporal = [nuevo_estado[i] for i in borde3]
             for i in range(3):
                  nuevo_estado[borde2[i]] = temporal[i]
             temporal = [nuevo_estado[i] for i in borde2]
             for i in range(3):
                  nuevo_estado[borde1[i]] = temporal[i]

        elif rotacion == "2":
             temporal1 = [nuevo_estado[i] for i in borde1]
             temporal2 = [nuevo_estado[i] for i in borde2]
             for i in range(3):
                  nuevo_estado[borde1[i]] = nuevo_estado[b3[i]]
                  nuevo_estado[borde3[i]] = temporal1[i]
                  nuevo_estado[borde2[i]] = nuevo_estado[borde4[i]]
                  nuevo_estado[borde4[i]] = temporal2[i]

        return nuevo_estado

                    

    def costo_local(self, estado, accion):
        if "2" in accion:
             return 2
        return 1
    

    @staticmethod
    def bonito(estado):
        
        """
        El prettyprint de un estado dado

        """

        def obtener_fila(indices):
             """
             para obtener una fila del cubo en un indice dado
             """
             return " " .join(f"{estado[i]:2}" for i in indices)
        
        U = [45, 46, 47, 48, 49, 50, 51, 52, 53] 
        L = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        F = [9, 10, 11, 12, 13, 14, 15, 16, 17]  
        R = [18, 19, 20, 21, 22, 23, 24, 25, 26]
        B = [27, 28, 29, 30, 31, 32, 33, 34, 35]
        D = [36, 37, 38, 39, 40, 41, 42, 43, 44]

        resultado = []
    
         # Up
        resultado.append("      " + obtener_fila(U[:3]))
        resultado.append("      " + obtener_fila(U[3:6]))
        resultado.append("      " + obtener_fila(U[6:9]))
        resultado.append("")  # Espacio
        
        for i in range(3):
          resultado.append(obtener_fila(L[i*3:i*3+3]) + " " +
          obtener_fila(F[i*3:i*3+3]) + " " +
           obtener_fila(R[i*3:i*3+3]) + " " +
           obtener_fila(B[i*3:i*3+3]))
         
          resultado.append("") # para espaciar
    
          resultado.append("      " + obtener_fila(D[:3]))
          resultado.append("      " + obtener_fila(D[3:6]))
          resultado.append("      " + obtener_fila(D[6:9]))
    
          return "\n".join(resultado)


# ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):

    def __init__(self):
        self.estado_inicial = estado_inicial 
        self.estado_objetivo = list(range(54))
        super()._init_(estado_inicial) #constructor de la clase base
     

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


if __name__ == "__main__":


    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PblCamionMágico( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)