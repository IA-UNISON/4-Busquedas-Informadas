#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
from collections import deque

# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class CamionMagico(busquedas.ModeloBusqueda):
    """x
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

    def acciones_legales(self, estado):
        acciones = []

        if estado + 1 <= self.N:
            acciones.append("caminar")
        if 2 * estado <= self.N:
            acciones.append("camion")

        return acciones        

    def sucesor(self, estado, accion):
        if accion == 'caminar':
            return estado + 1
        elif accion == 'camion':
            return 2 * estado
        else:
            raise ValueError("Juégale bien, caminas o usas el camión, no hay de otra...")

    def costo_local(self, estado, accion):
        if accion == "caminar":
            return 1  
        if accion == "camion":
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
        super().__init__(1, lambda estado: estado == N, CamionMagico(N))
        self.N = N


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_camion_magico(nodo, N):
    """
    Heurística 1: Distancia mínima considerando solo movimientos a pie.
    
    Justificación: 
    Si solo nos movemos a pie, la distancia restante es N - estado_actual. 
    Esto es admisible porque nunca sobreestima el costo real.
    """
    return (N - nodo)/2


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_camion_magico(nodo, N):
    """
    Heurística 2: Distancia mínima considerando el camión mágico.

    Justificación:
    Si usamos el camión, podemos reducir la distancia mucho más rápido.
    La idea es contar cuántos saltos de camión son posibles hasta N.
    """
    return N - (2 * nodo.estado)


# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------
class CuboRubik(busquedas.ModeloBusqueda):
    """
    El problema del cubo rubik.

    El estado es un conjunto de 6 matrices de 3x3 en representación de un cubo, 
    donde cada elemento de la matriz es un color. Por ejemplo, 'R' para rojo, 
    'G' para verde, etc.

    Por ejemplo, la cara frontal iniciaría como una cara completamente azul.
       -------------
       | B | B | B |
       -------------
       | B | B | B |
       -------------
       | B | B | B |
       ------------

    Además, es posible rotar sus caras en sentido horario, afectando así a los
    elementos adyacentes. Siendo así, estas rotaciones sus acciones legales.

    Acciones_legales = {'F', 'L', 'R', 'B', 'U', 'D'}

    """
    def __init__(self):
        self.cara_frontal = tuple(tuple('B' for _ in range(3)) for _ in range(3))  # Rojo
        self.cara_izquierda = [['O' for _ in range(3)] for _ in range(3)]  # Naranja
        self.cara_derecha = [['R' for _ in range(3)] for _ in range(3)]  # Verde
        self.cara_trasera = [['G' for _ in range(3)] for _ in range(3)]  # Blanco
        self.cara_superior = [['Y' for _ in range(3)] for _ in range(3)]  # Amarillo
        self.cara_inferior = [['W' for _ in range(3)] for _ in range(3)]  # Azul

        self.estado = self.cara_frontal, self.cara_izquierda, self.cara_derecha, self.cara_trasera, self.cara_superior, self.cara_inferior

    def acciones_legales(self, estado):
        return {'F', 'L', 'R', 'B', 'U', 'D'}

    def sucesor(self, estado, accion):
        """
        Rota la cara 90° en sentido horario.

        Regresa una matríz con sus elementos traspuestos en sentido del reloj.
        """
        def rotar_cara(cara):
            return [list(x) for x in zip(*cara[::-1])]
        
        """
        Mueve las piezas adyacentes.

        Al rotar una cara, se espera que se muevan las piezas adyacentes a esa cara.

        Regresa el conjunto de matrices que conforman al estado actualizado.
        """
        def mover(estado, movimiento):
            caras = [[list(fila[:]) for fila in cara] for cara in estado]      
            cara_frontal, cara_izquierda, cara_derecha, cara_trasera, cara_superior, cara_inferior = caras

            #print("Movimiento: ", movimiento)
            if movimiento == 'F': 
                cara_frontal = rotar_cara(cara_frontal) #rota la cara frontal 90° en el sentido del reloj
                temp = [cara_izquierda[i][2] for i in range(3)] #guarda la columna derecha de la cara izquierda  
                temp2 = [cara_derecha[i][0] for i in range(3)] #guarda la columna izquierda de la cara derecha
                temp3 = cara_superior[2][:] #guarda la fila inferior de la cara superior
                temp4 = cara_inferior[0][:] #guarda la fila superior de la cara inferior
                # Cambia la cara superior
                for i in range(3):
                    cara_superior[2][i] = temp[::-1][i]
                # Cambia la cara inferior
                for i in range(3):
                    cara_inferior[0][i] = temp2[::-1][i]
                # Cambia la cara izquierda
                for i in range(3):
                    cara_izquierda[i][2] = temp4[i] 
                # Cambia la cara derecha
                for i in range(3):
                    cara_derecha[i][0] = temp3[i]        
                 #print("Cara front dsp de cambio: ", cara_frontal)        

            elif movimiento == 'L':
                cara_izquierda = rotar_cara(cara_izquierda) #rota la cara izquierda 90° en sentido del reloj
                temp = [cara_frontal[i][0] for i in range(3)] #guarda la columna izquierda de la cara frontal
                temp2 = [cara_trasera[i][2] for i in range(3)] #guarda la columna derecha de la cara trasera
                temp3 = [cara_superior[i][0] for i in range(3)] #guarda la columna izquierda de la cara superior
                temp4 = [cara_inferior[i][0] for i in range(3)] #guarda la columna izquierda de la cara inferior
                # Cambia la cara superior
                for i in range(3):
                    cara_superior[i][0] = temp2[::-1][i] 
                # Cambia la cara inferior
                for i in range(3):
                    cara_inferior[i][0] = temp[i]
                # Cambia la cara frontal
                for i in range(3):
                    cara_frontal[i][0] = temp3[i]
                # Cambia la cara trasera
                for i in range(3):
                    cara_trasera[i][2] = temp4[::-1][i]
                #print("Cara izq dsp de cambio: ", cara_izquierda)  
        
            elif movimiento == 'R':
                cara_derecha = rotar_cara(cara_derecha) #rota la cara derecha 90° en sentido del reloj
                temp = [cara_frontal[i][2] for i in range(3)] #guarda la columna derecha de la cara frontal
                temp2 = [cara_trasera[i][0] for i in range(3)] #guarda la columna izquierda de la cara trasera
                temp3 = [cara_superior[i][2] for i in range(3)] #guarda la columna derecha de la cara superior
                temp4 = [cara_inferior[i][2] for i in range(3)] #guarda la columna derecha de la cara inferior
                # Cambia la cara superior
                for i in range(3):
                    cara_superior[i][2] = temp[i]
                # Cambia la cara inferior
                for i in range(3):
                    cara_inferior[i][2] = temp2[::-1][i]
                # Cambia la cara frontal
                for i in range(3):
                    cara_frontal[i][2] = temp4[i]
                # Cambia la cara trasera
                for i in range(3):
                    cara_trasera[i][0] = temp3[::-1][i]
                #print("Cara der dsp de cambio: ", cara_derecha)  
        
            elif movimiento == 'B':
                cara_trasera = rotar_cara(cara_trasera)
                temp = [cara_izquierda[i][0] for i in range(3)] #guarda la columna izquierda de la cara izquierda
                temp2 = [cara_derecha[i][2] for i in range(3)] #guarda la columna derecha de la cara derecha
                temp3 = cara_superior[0][:] #guarda la fila superior de la cara superior
                temp4 = cara_inferior[2][:] #guarda la fila inferior de la cara inferior
                # Cambia la cara superior
                for i in range(3):
                    self.cara_superior[0][i] = temp2[i]
                # Cambia la cara inferior
                for i in range(3):
                    self.cara_inferior[2][i] = temp[i]
                # Cambia la cara izquierda
                for i in range(3):
                    self.cara_izquierda[i][0] = temp3[::-1][i]
                # Cambia la cara derecha
                for i in range(3):
                    self.cara_derecha[i][2] = temp4[::-1][i]
                #print("Cara tras dsp de cambio: ", cara_trasera)  
        
            elif movimiento == 'U':
                cara_superior = rotar_cara(cara_superior)
                temp = cara_frontal[0][:] #guarda la fila superior de la cara frontal
                temp2 = cara_izquierda[0][:] #guarda la fila superior de la cara izquierda
                temp3 = cara_derecha[0][:] #guarda la fila superior de la cara derecha
                temp4 = cara_trasera[0][:] #guarda la fila superior de la cara trasera
                # Cambia la cara izquierda
                for i in range(3):
                    cara_izquierda[0][i] = temp[i]
                # Cambia la cara derecha
                for i in range(3):
                    cara_derecha[0][i] = temp4[i]
                # Cambia la cara frontal
                for i in range(3):
                    cara_frontal[0][i] = temp3[i]
                # Cambia la cara trasera
                for i in range(3):
                    cara_trasera[0][i] = temp2[i]
                #print("Cara sup dsp de cambio: ", cara_superior)  
            
            elif movimiento == 'D':
                cara_inferior = rotar_cara(cara_inferior)
                temp = cara_frontal[2][:] #guarda la fila inferior de la cara frontal
                temp2 = cara_izquierda[2][:] #guarda la fila inferior de la cara izquierda
                temp3 = cara_derecha[2][:] #guarda la fila inferior de la cara derecha
                temp4 = cara_trasera[2][:] #guarda la fila inferior de la cara trasera
                # Cambia la cara izquierda
                for i in range(3):
                    cara_izquierda[2][i] = temp4[i]
                # Cambia la cara derecha
                for i in range(3):
                    cara_derecha[2][i] = temp[i]
                # Cambia la cara frontal
                for i in range(3):
                    cara_frontal[2][i] = temp2[i]
                # Cambia la cara trasera
                for i in range(3):
                    cara_trasera[2][i] = temp3[i]
                #print("Cara inf dsp de cambio: ", cara_inferior)  
            
            nuevo_estado = tuple(tuple(tuple(fila) for fila in cara) for cara in [cara_frontal, cara_izquierda, cara_derecha, cara_trasera, cara_superior, cara_inferior])   
            return nuevo_estado
        
        estado_actualizado = mover(estado,accion)
        return estado_actualizado

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        cara_frontal, cara_izquierda, cara_derecha, cara_trasera, cara_superior, cara_inferior = estado
        
        print("\nCara Frontal:")
        for fila in cara_frontal:
            print(' '.join(fila))
        print("\nCara Izquierda:")
        for fila in cara_izquierda:
            print(' '.join(fila))
        print("\nCara Derecha:")
        for fila in cara_derecha:
            print(' '.join(fila))       
        print("\nCara Trasera:")
        for fila in cara_trasera:
            print(' '.join(fila)) 
        print("\nCara Superior:")
        for fila in cara_superior:
            print(' '.join(fila))       
        print("\nCara Inferior:")
        for fila in cara_inferior:
            print(' '.join(fila))
 

# ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------
class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """
    def __init__(self):
        print("Este estado inicial se giró la cara derecha 3 veces y la cara superior 3 veces.")
        print("Estado inicial: ")

        estado_inicial = tuple(
            tuple(tuple(row) for row in cara) for cara in [
                [['O', 'O', 'O'], ['B', 'B', 'Y'], ['B', 'B', 'Y']],  # Frontal
                [['W', 'G', 'G'], ['O', 'O', 'O'], ['O', 'O', 'O']],  # Izquierda
                [['B', 'B', 'Y'], ['R', 'R', 'R'], ['R', 'R', 'R']],  # Derecha
                [['R', 'R', 'R'], ['W', 'G', 'G'], ['W', 'G', 'G']],  # Trasera
                [['G', 'G', 'G'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],  # Superior
                [['W', 'W', 'B'], ['W', 'W', 'B'], ['W', 'W', 'B']]   # Inferior
            ]
        )

        CuboRubik.bonito(estado_inicial)
        print("\nSe necesita girar la cara superior 1 vez y luego la cara derecha 1 vez para solucionarlo.")
        print("Estado meta: ")

        modelo = CuboRubik()

        #meta = lambda estado: estado == tuple(tuple(tuple(row) for row in cara) for cara in modelo.estado)
        meta = tuple(tuple(tuple(row) for row in cara) for cara in modelo.estado)
        CuboRubik.bonito(meta)

        super().__init__(estado_inicial, lambda estado: estado == meta, modelo)


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Calcula la heurística basada en la cantidad de movimientos que necesita
    cada esquina y cada arista para llegar a su posición y orientación correctas.

    @param nodo: Nodo del cubo de Rubik con el estado actual del cubo.
    @return: Estimación del número mínimo de movimientos necesarios para resolver el cubo.
    """
    estado = nodo.estado  # Obtenemos las 6 caras del cubo
    meta = CuboRubik()  # Estado resuelto del cubo
    meta_estado = meta.estado

    movimientos_necesarios = 0

    # Comparar cada cara del cubo con la meta
    for cara_actual, cara_objetivo in zip(estado, meta_estado):
        for i in range(3):
            for j in range(3):
                if cara_actual[i][j] != cara_objetivo[i][j]:  # Si el color no está en su lugar
                    movimientos_necesarios += 1  # Se asume que al menos un movimiento será necesario

    return movimientos_necesarios / 8


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Heurística admisible para el Cubo de Rubik:
    Cuenta el número de esquinas y aristas mal ubicadas y lo divide por 8.
    """
    estado = nodo.estado  # Extraemos el estado actual del nodo
    
    # Estado final
    estado_meta = (
        (('B', 'B', 'B'), ('B', 'B', 'B'), ('B', 'B', 'B')),  # Frontal
        (('O', 'O', 'O'), ('O', 'O', 'O'), ('O', 'O', 'O')),  # Izquierda
        (('R', 'R', 'R'), ('R', 'R', 'R'), ('R', 'R', 'R')),  # Derecha
        (('G', 'G', 'G'), ('G', 'G', 'G'), ('G', 'G', 'G')),  # Trasera
        (('Y', 'Y', 'Y'), ('Y', 'Y', 'Y'), ('Y', 'Y', 'Y')),  # Superior
        (('W', 'W', 'W'), ('W', 'W', 'W'), ('W', 'W', 'W'))   # Inferior
    )

    esquinas_mal = 0
    aristas_mal = 0

    esquinas = [
        (0, 0, 0), (0, 0, 2), (0, 2, 0), (0, 2, 2),  # Frontal
        (3, 0, 0), (3, 0, 2), (3, 2, 0), (3, 2, 2)   # Trasera
    ]

    aristas = [
        (0, 0, 1), (0, 1, 0), (0, 1, 2), (0, 2, 1),  # Frontal
        (1, 0, 1), (1, 1, 0), (1, 1, 2), (1, 2, 1),  # Izquierda
        (2, 0, 1), (2, 1, 0), (2, 1, 2), (2, 2, 1)   # Derecha
    ]

    # Contar esquinas incorrectas
    for cara, fila, col in esquinas:
        if estado[cara][fila][col] != estado_meta[cara][fila][col]:
            esquinas_mal += 1

    # Contar aristas incorrectas
    for cara, fila, col in aristas:
        if estado[cara][fila][col] != estado_meta[cara][fila][col]:
            aristas_mal += 1

    return (esquinas_mal + aristas_mal) / 8


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
        current_x = nodo.estado
        return max(N - current_x, 0)
    
    def h2(nodo):
        current_x = nodo.estado
        if current_x >= N:
            return 0
        k = 0
        while current_x * (2 ** (k + 1)) <= N:
            k += 1
        return 2 * k + (N - current_x * (2 ** k))
    return h1, h2

if __name__ == "__main__":

    # # Compara los métodos de búsqueda para el problema del camión mágico
    # # con las heurísticas que desarrollaste
    N = 15
    problema = PblCamionMágico(N)
    h_1, h_2 = crear_heuristicas(N)
    compara_metodos(problema, h_1, h_2)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PblCuboRubik() 
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
