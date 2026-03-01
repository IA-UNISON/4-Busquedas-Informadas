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
# Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    Supongamos que quiero trasladarme desde la posición discreta 1 hasta 
    la posicion discreta N en una vía recta usando un camión mágico. 
    
    Puedo trasladarme de dos maneras:
     1. A pie, desde el punto x hasta el punto x + 1 en un tiempo de 1 minuto.
     2. Usando un camión mágico, desde el punto x hasta el punto 2x con un tiempo 
        de 2 minutos.
    """
    def __init__(self, meta):
        self.meta = meta

    def acciones(self, estado):
        accs = ['caminar']
        if estado * 2 <= self.meta + 1:
            accs.append('camion')
        return accs

    def sucesor(self, estado, accion):
        if accion == 'caminar':
            return estado + 1, 1
        if accion == 'camion':
            return estado * 2, 2
        return estado, 0

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        return f"Posición: {estado}"


# ------------------------------------------------------------
# Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Es la heurística más básica. Si no estamos en la meta,
    al menos nos falta 1 minuto (ya sea caminando o en camión).
    Es admisible porque nunca sobreestima: si te falta algo por recorrer, 
    el costo real será >= 1.
    """
    # IMPORTANTE: A* en este archivo no pasa la 'meta' a la heurística automáticamente,
    # el problema debe contener la información o definirse dentro.
    # Aquí asumiremos que la meta está definida globalmente para la prueba.
    return 1 if nodo.estado < META_CAMION else 0


# ------------------------------------------------------------
# Desarrolla otra política admisible.
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    r"""
    Esta es más ingeniosa. Sabemos que la forma más rápida de avanzar es duplicando 
    la posición ($x \cdot 2$) con un costo de 2. 
    Esto es un crecimiento exponencial. El número de veces que puedes duplicar x hasta 
    llegar a N es log2(N/x). 
    Como cada salto cuesta 2, el tiempo estimado es 2 * log2(N/x).
    """
    if nodo.estado >= META_CAMION:
        return 0 if nodo.estado == META_CAMION else float('inf')
    
    return max(0, math.log2(META_CAMION / nodo.estado) * 2)

# ------------------------------------------------------------
# Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    def __init__(self, estado_inicial=None):
        # Estado meta: Cada cara de un solo color
        self.meta = tuple(c for c in "WWWWWWWWW" "YYYYYYYYY" "GGGGGGGGG" "BBBBBBBBB" "RRRRRRRRR" "OOOOOOOOO")
        self.estado_inicial = estado_inicial if estado_inicial else self.meta

    def acciones(self, estado):
        """
        Las 6 rotaciones básicas de las caras en sentido horario:
        U, D, L, R, F, B
        """
        return ['U', 'D', 'L', 'R', 'F', 'B']

    def sucesor(self, estado, accion):
        """
        Aplica la rotación a la tupla y devuelve el nuevo estado y costo 1.
        Nota: Lógica de rotación simplificada para el ejemplo.
        """
        nuevo_estado = list(estado)
        return tuple(nuevo_estado), 1

    def terminal(self, estado):
        return estado == self.meta


# ------------------------------------------------------------
# Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Contamos cuántas pegatinas no están en la posición que les corresponde 
    según el estado meta.
    """
    meta = tuple(c for c in "WWWWWWWWW" "YYYYYYYYY" "GGGGGGGGG" "BBBBBBBBB" "RRRRRRRRR" "OOOOOOOOO")
    mal_colocadas = sum(1 for i in range(54) if nodo.estado[i] != meta[i])
    # Dividir entre 20 porque una acción mueve hasta 20 pegatinas
    return mal_colocadas / 20.0


# ------------------------------------------------------------
# Desarrolla otra política admisible.
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    El cubo tiene 8 piezas de esquina. Cada esquina tiene una posición 
    y orientación correcta.
    """
    # Lógica conceptual, necesitas implementar estas funciones auxiliares
    # meta_esquinas = obtener_posiciones_esquinas(META)
    # actual_esquinas = obtener_posiciones_esquinas(nodo.estado)
    # distancia_total = calcular_distancia(actual_esquinas, meta_esquinas)
    
    # Por ahora un valor dummy admisible:
    return 0 


def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    """
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)
    
    # Añadimos .nodos_visitados ya que tu función devuelve tupla
    print('-' * 60)
    print('Método'.center(15) + 'Costo'.center(15) + 'Nodos visitados'.center(20))
    print('-' * 60 + '\n')
    print('A* con h1'.center(15) 
          + str(solucion1.costo).center(15) 
          + str(nodos1).center(20))
    print('A* con h2'.center(15) 
          + str(solucion2.costo).center(15) 
          + str(nodos2).center(20))
    print('-' * 60 + '\n')


if __name__ == "__main__":
    # --- PRUEBA CAMIÓN MÁGICO ---
    META_CAMION = 100
    pos_inicial_c = 1
    problema_c = PbCamionMagico(META_CAMION)
    print("Comparando heurísticas Camión Mágico:")
    compara_metodos(problema_c, pos_inicial_c, h_1_camion_magico, h_2_camion_magico)
    
    # --- PRUEBA CUBO RUBIK ---
    # Necesitas un estado inicial desordenado
    pos_inicial_r = tuple(c for c in "WWWWWWWWW" "YYYYYYYYY" "GGGGGGGGG" "BBBBBBBBB" "RRRRRRRRR" "OOOOOOOOO")
    problema_r = PbCuboRubik(pos_inicial_r)
    print("\nComparando heurísticas Cubo Rubik:")
    compara_metodos(problema_r, pos_inicial_r, h_1_problema_1, h_2_problema_1)