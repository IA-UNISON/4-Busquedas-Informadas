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
     def __init__(self, N):
        super().__init__()
        self.N = N
        self.estado = 1 #este es el estado inicial 
        

     def acciones_legales(self, estado):
        acciones = []
        if estado + 1 <= self.N:
            acciones.append("caminar") #caminar a x +1 que tiene menor costo
        if 2 * estado <= self.N:
            acciones.append("camion") #usar el camion magico
        return acciones

     def sucesor(self, estado, accion):
        #devuelve el estado del sucesor al usar la accion
        if accion == "caminar":
            return estado + 1
        elif accion == "camion":
            return 2*estado
        else:
          raise ValueError('Accion no valida')

     def costo_local(self, estado, accion):
        if accion == "caminar":
            return 1
        elif accion == "camion":
            return 2
        else:
          raise ValueError('Accion no valida')

     @staticmethod
     def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posicion: {estado}"
 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, N):
        x0 = 1 #estado inicial
        meta = lambda estado: estado == N
        modelo = CamionMagico(N)
        super().__init__(x0, meta, modelo)
        #raise NotImplementedError('Hay que hacerlo de tarea')
    

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico1(N):
    """
     estima el tiempo minimop necesario para llegar a N
     asuminedo que solo se camina    

    """
    def heuristica(nodo):
        return max(N - nodo.estado, 0)  # Asegura que no sea negativo
    return heuristica

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico2(N):
    """
    Distancia logaritmica para N,
    calcula el tiempo minimo para legar aN asumiendo que solo se usa el camion magico

    """
    def heuristica(nodo):
        tiempo = 0
        estado_actual = nodo.estado
        while estado_actual < N:
            estado_actual *= 2  # Usar el camión
            tiempo += 2  # Cada uso del camión toma 2 minutos
        return tiempo
    return heuristica
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
        super().__init__()
        self.acciones = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
        self.estado = []

    def acciones_legales(self, estado):
        return self.acciones #se puede mover el cubo de cualquier manera no existen restricciones
    
    def rotar_cara(self, estado, cara, sentido):
        """
        Rota una cara del cubo en sentido horario o antihorario.

        @param estado: Lista que representa el estado actual del cubo.
        @param cara: Lista de índices que representan la cara a rotar.
        @param sentido: Sentido de rotación ("horario" o "antihorario").
        @return: Nuevo estado con la cara rotada.
        """
        if sentido == "horario":
            estado[cara[0]], estado[cara[1]], estado[cara[2]], \
            estado[cara[3]], estado[cara[4]], estado[cara[5]], \
            estado[cara[6]], estado[cara[7]], estado[cara[8]] = \
                estado[cara[6]], estado[cara[3]], estado[cara[0]], \
                estado[cara[7]], estado[cara[4]], estado[cara[1]], \
                estado[cara[8]], estado[cara[5]], estado[cara[2]]
        elif sentido == "antihorario":
            estado[cara[0]], estado[cara[1]], estado[cara[2]], \
            estado[cara[3]], estado[cara[4]], estado[cara[5]], \
            estado[cara[6]], estado[cara[7]], estado[cara[8]] = \
                estado[cara[2]], estado[cara[5]], estado[cara[8]], \
                estado[cara[1]], estado[cara[4]], estado[cara[7]], \
                estado[cara[0]], estado[cara[3]], estado[cara[6]]
        return estado


    def rotar_piezas_adyacentes(self, estado, piezas, sentido):
        """
        Rota las piezas adyacentes a una cara.

        @param estado: Lista que representa el estado actual del cubo.
        @param piezas: Lista de índices que representan las piezas adyacentes.
        @param sentido: Sentido de rotación ("horario" o "antihorario").
        @return: Nuevo estado con las piezas adyacentes rotadas.
        """
        if sentido == "horario":
            estado[piezas[0]], estado[piezas[1]], estado[piezas[2]], \
            estado[piezas[3]], estado[piezas[4]], estado[piezas[5]], \
            estado[piezas[6]], estado[piezas[7]], estado[piezas[8]], \
            estado[piezas[9]], estado[piezas[10]], estado[piezas[11]] = \
                estado[piezas[9]], estado[piezas[10]], estado[piezas[11]], \
                estado[piezas[0]], estado[piezas[1]], estado[piezas[2]], \
                estado[piezas[3]], estado[piezas[4]], estado[piezas[5]], \
                estado[piezas[6]], estado[piezas[7]], estado[piezas[8]]
        elif sentido == "antihorario":
            estado[piezas[0]], estado[piezas[1]], estado[piezas[2]], \
            estado[piezas[3]], estado[piezas[4]], estado[piezas[5]], \
            estado[piezas[6]], estado[piezas[7]], estado[piezas[8]], \
            estado[piezas[9]], estado[piezas[10]], estado[piezas[11]] = \
                estado[piezas[3]], estado[piezas[4]], estado[piezas[5]], \
                estado[piezas[6]], estado[piezas[7]], estado[piezas[8]], \
                estado[piezas[9]], estado[piezas[10]], estado[piezas[11]], \
                estado[piezas[0]], estado[piezas[1]], estado[piezas[2]]
        return estado


    def sucesor(self, estado, accion):
        """
        Aplica una acción al estado actual y devuelve el nuevo estado.

        @param estado: Una tupla que representa el estado actual del cubo.
        @param accion: Una acción válida (por ejemplo, "U", "U'", "D", etc.).

        @return: Una tupla con el nuevo estado después de aplicar la acción.
        """
        nuevo_estado = list(estado)  # Copia del estado actual

        # Definimos los índices de las caras del cubo
        # Cara frontal (F): 0-8, Cara trasera (B): 9-17, Cara superior (U): 18-26,
        # Cara inferior (D): 27-35, Cara izquierda (L): 36-44, Cara derecha (R): 45-53
        caras = {
            "F": list(range(0, 9)),    # Frontal
            "B": list(range(9, 18)),   # Trasera
            "U": list(range(18, 27)),  # Superior
            "D": list(range(27, 36)),  # Inferior
            "L": list(range(36, 45)),  # Izquierda
            "R": list(range(45, 54))   # Derecha
        }
        piezas_adyacentes = {
            "U": [0, 3, 6, 45, 48, 51, 9, 12, 15, 36, 39, 42],
            "F": [6, 7, 8, 0, 3, 6, 0, 1, 2, 8, 5, 2],
            "B": [0, 1, 2, 8, 5, 2, 6, 7, 8, 0, 3, 6],
            "D": [6, 7, 8, 6, 7, 8, 6, 7, 8, 6, 7, 8],
            "L": [0, 3, 6, 0, 3, 6, 8, 5, 2, 0, 3, 6],
            "R": [2, 5, 8, 2, 5, 8, 6, 3, 0, 2, 5, 8]
        }
        # Lógica para cada acción
        if accion in ["U","U'"]:  # Giro de la cara superior en sentido horario
            sentido = "horario" if accion == "U" else "antihorario"
            nuevo_estado = self.rotar_cara(nuevo_estado[:], caras["U"], sentido)
            # Rotar las piezas adyacentes
            nuevo_estado = self.rotar_piezas_adyacentes(nuevo_estado[:], piezas_adyacentes["U"], sentido)

        elif accion in ["F","F'"]:  # Giro de la cara frontal en sentido horario
            sentido = "horario" if accion == "F" else "antihorario"
            # Rotar la cara frontal
            nuevo_estado = self.rotar_cara(nuevo_estado[:], caras["F"], sentido)
            # Rotar las piezas adyacentes
            
            nuevo_estado = self.rotar_piezas_adyacentes(nuevo_estado[:], piezas_adyacentes["F"], sentido)
        elif accion in ["B","B'"]:  # Giro de la cara trasera en sentido horario
            sentido = "horario" if accion == "B" else "antihorario"
            # Rotar la cara trasera
            nuevo_estado = self.rotar_cara(nuevo_estado[:], caras["B"], sentido)
            # Rotar las piezas adyacentes
            nuevo_estado = self.rotar_piezas_adyacentes(nuevo_estado[:], piezas_adyacentes["B"], sentido)

        elif accion in ["D","D'"]:  # Giro de la cara inferior en sentido horario
            sentido = "horario" if accion == "D" else "antihorario"
            # Rotar la cara inferior
            nuevo_estado = self.rotar_cara(nuevo_estado, caras["D"], sentido)
            # Rotar las piezas adyacentes
            nuevo_estado = self.rotar_piezas_adyacentes(nuevo_estado[:], piezas_adyacentes["D"], sentido)

        elif accion in ["L","L'"]:  # Giro de la cara izquierda en sentido horario
            sentido = "horario" if accion == "L" else "antihorario"
            # Rotar la cara 
            nuevo_estado = self.rotar_cara(nuevo_estado, caras["L"], sentido)
            # Rotar las piezas adyacentes
            nuevo_estado = self.rotar_piezas_adyacentes(nuevo_estado[:], piezas_adyacentes["L"], sentido)

        elif accion in ["R","R'"]:  # Giro de la cara derecha en sentido horario
            sentido = "horario" if accion == "R" else "antihorario"
            # Rotar la cara 
            nuevo_estado = self.rotar_cara(nuevo_estado, caras["R"], sentido)
            # Rotar las piezas adyacentes
            nuevo_estado = self.rotar_piezas_adyacentes(nuevo_estado[:], piezas_adyacentes["R"], sentido)
        return tuple(nuevo_estado)
    
    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Estado: {estado}"
 
 # ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """
    def __init__(self, estado_inicial):
        x0 = estado_inicial
        estado_resuelto = [
            'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',  # Cara frontal (rojo)
            'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',  # Cara trasera (azul)
            'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',  # Cara superior (blanco)
            'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v',  # Cara inferior (verde)
            'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',  # Cara izquierda (negro)
            'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'   # Cara derecha (morado)
        ]

        meta = lambda estado: estado == estado_resuelto #editado la parte de estado: estado
        modelo = CuboRubik()
        super().__init__(x0, meta, modelo)
       # raise NotImplementedError('Hay que hacerlo de tarea')
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Numero de estados fuera de lugar

    """
    estado_resuelto = [
        'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',  # Cara frontal (rojo)
        'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',  # Cara trasera (azul)
        'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',  # Cara superior (blanco)
        'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v',  # Cara inferior (verde)
        'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',  # Cara izquierda (negro)
        'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'   # Cara derecha (morado)
    ]
    return sum(1 for i, j in zip(nodo.estado, estado_resuelto) if i != j)

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Heurística 2: Distancia de Manhattan para cada pieza.
    Esta heurística es admisible porque nunca sobrestima el costo real.
    """
    estado_resuelto = [
        'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r',  # Cara frontal (rojo)
        'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',  # Cara trasera (azul)
        'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b',  # Cara superior (blanco)
        'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v',  # Cara inferior (verde)
        'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n',  # Cara izquierda (negro)
        'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'   # Cara derecha (morado)
    ]
    distancia = 0
    for i in range(len(nodo.estado)):
        if nodo.estado[i] != estado_resuelto[i]:
            # Calcula la distancia de Manhattan (simplificada)
            # Suponiendo que el cubo es 3x3x3
            x1, y1, z1 = i // 9, (i % 9) // 3, i % 3
            x2, y2, z2 = estado_resuelto.index(nodo.estado[i]) // 9, (estado_resuelto.index(nodo.estado[i]) % 9) // 3, estado_resuelto.index(nodo.estado[i]) % 3
            distancia += abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
    return distancia

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
    N = 100
    problema = PblCamionMágico(N)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_camion_magico1(N), h_2_camion_magico2(N))
    
    # Compara los métodos de búsqueda para el problema del cubo de rubikdi
    # con las heurísticas que desarrollaste
    cubo_random = (
    'b', 'r', 'r', 'b', 'r', 'r', 'b', 'r', 'r',  # Cara frontal
    'a', 'a', 'n', 'a', 'a', 'n', 'a', 'a', 'n',  # Cara trasera
    'b', 'b', 'm', 'b', 'b', 'm', 'b', 'b', 'm',  # Cara superior
    'v', 'v', 'r', 'v', 'v', 'r', 'v', 'v', 'r',  # Cara inferior
    'n', 'n', 'b', 'n', 'n', 'b', 'n', 'n', 'b',  # Cara izquierda
    'm', 'm', 'v', 'm', 'm', 'v', 'm', 'm', 'v'   # Cara derecha
    )
    problema = PblCuboRubik( cubo_random )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    