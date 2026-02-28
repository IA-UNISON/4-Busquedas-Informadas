#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo importante es crear nuevas heurísticas
y compararlas usando A*.
"""

import busquedas
import math


# ------------------------------------------------------------
#  MODELO DEL CAMIÓN MÁGICO
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):

    def __init__(self, N):
        self.N = N
        PbCamionMagico.N_GLOBAL = N

    def acciones(self, estado):
        acciones = []
        if estado + 1 <= self.N:
            acciones.append("caminar")
        if estado * 2 <= self.N:
            acciones.append("camion")
        return acciones

    def sucesor(self, estado, accion):
        if accion == "caminar":
            return (estado + 1, 1)
        elif accion == "camion":
            return (estado * 2, 2)

    def terminal(self, estado):
        return estado == self.N

    @staticmethod
    def bonito(estado):
        return f"Posición: {estado}"


# ------------------------------------------------------------
#  HEURÍSTICAS CAMIÓN
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    estado = nodo.estado
    N = PbCamionMagico.N_GLOBAL
    return N - estado


def h_2_camion_magico(nodo):
    estado = nodo.estado
    N = PbCamionMagico.N_GLOBAL

    if estado >= N:
        return 0

    return (N - estado) // 2


# ------------------------------------------------------------
#  MODELO DEL CUBO RUBIK SIMPLIFICADO
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    Modelo simplificado de Cubo Rubik 3x3.
    El estado es una tupla de 9 números (grid 3x3).
    """

    def __init__(self, meta=(1,2,3,4,5,6,7,8,9)):
        self.meta = meta

        self.movimientos = {
            "R": [(2,5),(5,8)],
            "L": [(0,3),(3,6)],
            "U": [(0,1),(1,2)],
            "D": [(6,7),(7,8)]
        }

    def acciones(self, estado):
        return list(self.movimientos.keys())

    def sucesor(self, estado, accion):
        nuevo = list(estado)

        for i, j in self.movimientos[accion]:
            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]

        return tuple(nuevo), 1

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        return (
            f"{estado[0]} {estado[1]} {estado[2]}\n"
            f"{estado[3]} {estado[4]} {estado[5]}\n"
            f"{estado[6]} {estado[7]} {estado[8]}"
        )


# ------------------------------------------------------------
#  HEURÍSTICAS CUBO
# ------------------------------------------------------------

def h_1_problema_1(nodo):
    """
    Heurística 1:
    Número de piezas fuera de lugar.

    Es admisible porque cada pieza mal colocada
    requiere al menos un movimiento.
    """
    meta = (1,2,3,4,5,6,7,8,9)
    return sum(1 for i in range(9) if nodo.estado[i] != meta[i])


def h_2_problema_1(nodo):
    """
    Heurística 2:
    Distancia Manhattan total en el grid 3x3.

    Es admisible porque cada movimiento mueve
    una pieza como máximo una posición.
    """

    estado = nodo.estado

    meta_pos = {
        1:(0,0),2:(0,1),3:(0,2),
        4:(1,0),5:(1,1),6:(1,2),
        7:(2,0),8:(2,1),9:(2,2)
    }

    total = 0

    for idx, valor in enumerate(estado):
        fila_actual = idx // 3
        col_actual = idx % 3

        fila_meta, col_meta = meta_pos[valor]

        total += abs(fila_actual - fila_meta) + abs(col_actual - col_meta)

    return total


# ------------------------------------------------------------
#  COMPARADOR
# ------------------------------------------------------------

def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):

    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)

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


# ------------------------------------------------------------
#  MAIN
# ------------------------------------------------------------
if __name__ == "__main__":

    # ==============================
    # CAMIÓN MÁGICO
    # ==============================
    print("\n===== CAMIÓN MÁGICO =====")

    pos_inicial = 1
    problema = PbCamionMagico(100)

    compara_metodos(
        problema,
        pos_inicial,
        h_1_camion_magico,
        h_2_camion_magico
    )

    # ==============================
    # CUBO RUBIK SIMPLIFICADO
    # ==============================
    print("\n===== CUBO RUBIK SIMPLIFICADO =====")

    problema = PbCuboRubik()

    # Generamos un estado alcanzable aplicando movimientos válidos
    estado1, _ = problema.sucesor(problema.meta, "U")
    estado2, _ = problema.sucesor(estado1, "R")
    estado_inicial, _ = problema.sucesor(estado2, "L")

    compara_metodos(
        problema,
        estado_inicial,
        h_1_problema_1,
        h_2_problema_1
    )