#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
from math import log2, ceil
from random import choice

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
    def __init__(self, meta=100):
        self.meta = meta
        self.acciones_legales = ['pie', 'camion']

    def acciones(self, estado):
        x, = estado

        if 2 * x > self.meta:
            return ['pie']
        else:
            return ['pie', 'camion']

    def sucesor(self, estado, accion):
        x, = estado

        if accion == 'pie':
            costo_local = 1
            s_n = x + 1,
        if accion == 'camion':
            costo_local = 2
            s_n = x * 2,

        return s_n, costo_local

    def terminal(self, estado):
        x, = estado
        
        return True if x == self.meta else False

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        print(f"Estado actual: {estado}")

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico_helper(N):
    """
    Clausura para mantener la estructura de la comparación
    """

    def h_1_camion_magico(nodo):
        """
        Mínimo de pasos

        Bajamos el costo del camión a 1. Ahora ambos cuestan lo mismo,
        entonces lo que importa son los pasos. Como la heurística
        calcula el mínimo de pasos y el costo de una acción en el real
        es mínimo 1, la heurística siempre regresará un costo (pasos) menor.

        """
        pasos = 0
        x = nodo.estado[0]
        meta = N

        while meta > x:
            if meta % 2 == 0 and meta/2 >= x:
                pasos += 1
                meta //= 2
            elif meta % 2 == 0 and meta-1 >= x:
                pasos += 1
                meta -= 1
            elif meta % 2 != 0 and meta-1 >= x:
                pasos += 1
                meta -= 1

        return pasos
    
    return h_1_camion_magico
                
# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_camion_magico_helper(N):
    """
    Clausura para mantener la estructura de la comparación
    """

    def h_2_camion_magico(nodo):

        """
        Pasos exactos

        Aquí se relaja aún más, ahora no solo todo cuesta uno,
        ahora podemos dar pasos exactos en camión para llegar a N.
        Multiplicamos x por 2 k veces para llegar a N.
        x * 2^k = N
        Entonces lo que nos interesa son los pasos (k),
        despejamos:
        log_2(2^k) = log_2(N / x) ---> k = log_2(N / x)
        donde k es la cantidad exacta de veces a multiplicar
        x * 2 para llegar a N

        """
        x = nodo.estado[0]

        return log2(N/x)
    
    return h_2_camion_magico

# Conclusión
# La primer heurística es dominante respecto a la segunda porque la segunda es demasiado optimista.
# La primera respeta las reglas del espacio del juego: toma en cuenta que se puede caminar e ir en
# camión. Esto hace que se aproxime más al costo real. La segunda solo toma en cuenta el camión y
# los pasos se vuelven muy pequeños debido al logaritmo. También se puede observar en los resultados,
# donde a* + h1 explora muchos menos nodos que a* + h2.

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube

    Visualización (no integrada al código):
    https://pablington.com/ia/eval_comp/4-busquedas.html
    
    """
    def __init__(self):

        # Representación 6x9
        # Aplanado a un string de len 54
        # 0 1 2
        # 3 4 5
        # 6 7 8

        self.meta = (
            "W" * 9 +  # U Up    - White
            "Y" * 9 +  # D Down  - Yellow
            "G" * 9 +  # F Front - Green
            "B" * 9 +  # B Back  - Blue
            "O" * 9 +  # L Left  - Orange
            "R" * 9    # R Right - Red
        )

    def acciones(self, estado):
        return ['U', 'U_inv',
                'D', 'D_inv', 
                'F', 'F_inv', 
                'B', 'B_inv', 
                'L', 'L_inv', 
                'R', 'R_inv']

    def sucesor(self, estado, accion):
        # 1. Definimos los ciclos (horarios) para cada cara.
        # Cada cara tiene 5 ciclos: 
        # - 2 para rotar su propia cara (esquinas y aristas)
        # - 3 para el anillo o corona

        # Se lee, usando el ejemplo de abajo:
        # 0 a 2, 2 a 8, 8 a 6, 6 a 0

        # Ciclos Up
        ciclos_U = [
            (0, 2, 8, 6),       # Esquinas
            (1, 5, 7, 3),       # Aristas
            (18, 36, 27, 45),   # Corona Izq
            (19, 37, 28, 46),   # Corona Centro
            (20, 38, 29, 47)    # Corona Derecha
        ]

        # Ciclos Down
        ciclos_D = [
            (9, 11, 17, 15),    # Esquinas
            (10, 14, 16, 12),   # Aristas
            (35, 44, 26, 53),   # Corona Izq
            (34, 43, 25, 52),   # Corona Centro
            (33, 42, 24, 51)    # Corona Derecha
        ]

        # Ciclos Front
        ciclos_F = [
            (18, 20, 26, 24),   # Esquinas
            (19, 23, 25, 21),   # Aristas
            (6, 45, 11, 44),    # Corona Izq
            (7, 48, 10, 41),    # Corona Centro
            (8, 51, 9, 38)      # Corona Derecha
        ]

        # Ciclos Back
        ciclos_B = [
            (27, 29, 35, 33),   # Esquinas
            (28, 32, 34, 30),   # Aristas
            (17, 47, 0, 42),    # Corona Izq
            (16, 50, 1, 39),    # Corona Centro
            (15, 53, 2, 36)     # Corona Derecha
        ]

        # Ciclos Left
        ciclos_L = [
            (36, 38, 44, 42),   # Esquinas
            (37, 41, 43, 39),   # Aristas
            (15, 29, 6, 24),    # Corona Izq
            (12, 32, 3, 21),    # Corona Centro
            (9, 35, 0, 18)      # Corona Derecha
        ]

        # Ciclos Right
        ciclos_R = [
            (45, 47, 53, 51),   # Esquinas
            (46, 50, 52, 48),   # Aristas
            (11, 20, 2, 33),    # Corona Izq
            (14, 23, 5, 30),    # Corona Centro
            (17, 26, 8, 27)     # Corona Derecha
        ]
        
        movimientos = {
            'U': ciclos_U,
            'D': ciclos_D,
            'F': ciclos_F,
            'B': ciclos_B,
            'L': ciclos_L,
            'R': ciclos_R
        }
        
        # Si la acción es antihoraria volteamos los ciclos
        if accion.endswith('_inv'):
            accion_base = accion.replace('_inv', '')
            ciclos = [c[::-1] for c in movimientos[accion_base]]
        else:
            ciclos = movimientos[accion]

        s = list(estado)
        
        for a, b, c, d in ciclos:
            s[d], s[c], s[b], s[a] = s[c], s[b], s[a], s[d]
        
        s_n = "".join(s)
        return s_n, 1

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado
        En orden: U, D, F, B, L, R

        """
        for i in range(0, len(estado), 9):
            print(estado[i:i+9])

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_problema_1_helper(meta):
    """
    Clausura para mantener la estructura de la compración
    """

    def h_1_problema_1(nodo):
        """
        Colores o stickers descolocados

        Contamos cuantos stickers no estan donde deben respecto al
        estado meta. Luego dividimos entre 20 ya que un movimiento
        mueve 20 stickers (8 de la cara y 12 en la corona).

        Lo que se calcula es el numero de movimientos restantes
        estimados. Esta heurística es muy optimista porque siempre
        asume que al mover esos 20 stickers se llega a un estado
        más cerca a la meta. En realidad, como están conectados,
        usualmente se desacomodan otros. Por lo tanto, el costo (mo-
        vimientos) siempre va a ser igual o menor al real.
        """
        estado_actual = nodo.estado

        descolocadas = sum(1 for i in range(54) if estado_actual[i] != meta[i])

        return ceil(descolocadas / 20.0)
    
    return h_1_problema_1

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_problema_1(nodo):
    """
    Distancia a cara meta

    En esta en vez de la distancia al lugar exacto del sticker,
    calculamos la distancia a la cara correcta en términos de
    movimientos. Es 0 si está en la cara correcta, 1 si el lu-
    gar correcto está en una cara adyacente, y 2 si está en la
    cara opuesta a la en que se encuentra actualmente.

    Dividimos el resultado entre 12, la cantidad de caras en la
    corona, porque son las únicas que viajan a una nueva cara al
    hacer un movimiento.

    Ya que esta es una relajación de h1, es admisible.

    """
    estado = nodo.estado
    
    caras_colores = ['W', 'Y', 'G', 'B', 'O', 'R']
    
    opuestos = {
        'W': 'Y', 'Y': 'W',
        'G': 'B', 'B': 'G',
        'O': 'R', 'R': 'O'
    }
    
    distancia_total = 0
    
    for i, color_actual in enumerate(estado):
        
        # Ignoramos los centros
        if i % 9 == 4:
            continue
            
        # Bloque en el que estamos
        color_cara = caras_colores[i // 9]
        
        if color_actual == color_cara:
            distancia_total += 0
        elif opuestos[color_actual] == color_cara:
            distancia_total += 2
        else:
            distancia_total += 1
            
    return ceil(distancia_total / 12.0)

# Conclusión
# La segunda heurística es dominante respecto a la primera. La primer heurística
# regresa matemáticamente 1/20 del total, mientras que la segunda regresa 1/12
# del total. Al saber que ambas son admisibles podemos concluir que h2 se acerca
# más al costo real. También, viendo los resultados, se nota la diferencia en
# cuanto a nodos explorados. 

def _desarmar_rubik(problema, movimientos=5):
    """
    Desarma el cubo aplicando una secuencia aleatoria de movimientos
    """
    estado_actual = problema.meta
    acciones_posibles = problema.acciones(estado_actual)
    
    secuencia = [choice(acciones_posibles) for _ in range(movimientos)]
    print(f"Secuencia de desarme: {secuencia}")
    
    for accion in secuencia:
        estado_actual, _ = problema.sucesor(estado_actual, accion)
        
    return estado_actual

def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1, )
    solucion2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2, )
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n')

if __name__ == "__main__":

    # Camión Mágico
    pos_inicial = (1,)
    problema = PbCamionMagico(1000)
    compara_metodos(problema, pos_inicial, h_1_camion_magico_helper(problema.meta), h_2_camion_magico_helper(problema.meta))
    
    # Cubo Rubiks
    problema_rubiks = PbCuboRubik()
    pos_inicial_rubiks = _desarmar_rubik(problema_rubiks)
    compara_metodos(problema_rubiks, pos_inicial_rubiks, h_1_problema_1_helper(problema_rubiks.meta), h_2_problema_1)