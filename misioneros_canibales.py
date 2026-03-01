#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
misioneros_canibales.py
-----------------------

Daniel Eduardo Alvarez Terrazas

Problema clásico de los misioneros y caníbales

Hay 3 misioneros y 3 caníbales en la orilla izquierda de un río.
Tienen un bote que carga máximo 2 personas. El objetivo es pasar
a todos a la orilla derecha, pero en ningún momento los caníbales
pueden ser más que los misioneros en alguna orilla (si no, se los comen).

"""

import busquedas


class PbMisioneros(busquedas.ProblemaBusqueda):
    """
    Problema de los Misioneros y Caníbales.

    El estado es una tupla (m_izq, c_izq, bote) donde:
        - m_izq: misioneros en la orilla izquierda (0 a 3).
        - c_izq: caníbales en la orilla izquierda (0 a 3).
        - bote:  0 si el bote está en la izquierda, 1 si está en la derecha.

    La meta es (0, 0, 1): todos cruzaron y el bote está en la derecha.

    """
    def __init__(self):
        """
        Inicializa el problema. No necesita parámetros porque siempre
        son 3 misioneros y 3 caníbales.
        """
        self.total_m = 3
        self.total_c = 3

    def _es_valido(self, m_izq, c_izq):
        """
        Revisa que en ninguna orilla los caníbales superen a los misioneros.

        @param m_izq: int, misioneros en la orilla izquierda.
        @param c_izq: int, caníbales en la orilla izquierda.
        @return: bool, True si el estado es válido.

        """
        m_der = self.total_m - m_izq
        c_der = self.total_c - c_izq

        if m_izq < 0 or c_izq < 0 or m_der < 0 or c_der < 0:
            return False
        if m_izq > 0 and c_izq > m_izq:
            return False
        if m_der > 0 and c_der > m_der:
            return False
        return True

    def acciones(self, estado):
        """
        Devuelve las acciones legales desde el estado actual.

        Una acción es (m, c): cuántos misioneros y caníbales suben al bote.
        El bote lleva entre 1 y 2 personas. Solo se generan acciones que
        dejan ambas orillas en un estado válido.

        @param estado: tuple (m_izq, c_izq, bote).
        @return: list de tuplas (m, c) con las combinaciones válidas.

        """
        m_izq, c_izq, bote = estado
        posibles = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        legales = []

        for m, c in posibles:
            if bote == 0:
                nuevo_m = m_izq - m
                nuevo_c = c_izq - c
            else:
                nuevo_m = m_izq + m
                nuevo_c = c_izq + c

            if self._es_valido(nuevo_m, nuevo_c):
                legales.append((m, c))

        return legales

    def sucesor(self, estado, accion):
        """
        Aplica la acción y devuelve el nuevo estado con costo 1.

        Si el bote está en la izquierda, resta personas de esa orilla.
        Si está en la derecha, suma personas a la izquierda.

        @param estado: tuple (m_izq, c_izq, bote).
        @param accion: tuple (m, c), personas que cruzan.
        @return: tuple (nuevo_estado, costo_local).

        """
        m_izq, c_izq, bote = estado
        m, c = accion

        if bote == 0:
            nuevo = (m_izq - m, c_izq - c, 1)
        else:
            nuevo = (m_izq + m, c_izq + c, 0)

        return nuevo, 1

    def terminal(self, estado):
        """
        Revisa si todos cruzaron al lado derecho.

        @param estado: tuple (m_izq, c_izq, bote).
        @return: bool, True si m_izq == 0, c_izq == 0 y bote == 1.

        """
        return estado == (0, 0, 1)

    @staticmethod
    def bonito(estado):
        """
        Muestra el estado de forma visual.

        @param estado: tuple (m_izq, c_izq, bote).
        @return: str, representación del estado.

        """
        m_izq, c_izq, bote = estado
        m_der = 3 - m_izq
        c_der = 3 - c_izq
        lado_bote = "<--bote" if bote == 0 else "bote-->"
        return (f"Izq: {m_izq}M {c_izq}C  |  {lado_bote}  |  "
                f"Der: {m_der}M {c_der}C")


if __name__ == "__main__":

    problema = PbMisioneros()
    s0 = (3, 3, 0)

    print("=" * 55)
    print("  MISIONEROS Y CANÍBALES")
    print("=" * 55)
    print(f"\nEstado inicial: {PbMisioneros.bonito(s0)}")
    print(f"Meta: pasar a todos a la derecha\n")

    # --- BFS ---
    print("---------- BFS ----------")
    plan, nodos = busquedas.busqueda_ancho(problema, s0)
    if plan:
        print(f"Costo: {plan.costo}")
        print(f"Nodos visitados: {nodos}")
        print("Trayectoria:")
        for (estado, accion, costo) in plan.genera_plan():
            if accion is not None:
                m, c = accion
                print(f"  {PbMisioneros.bonito(estado)}  ->  cruzan {m}M {c}C")
            else:
                print(f"  {PbMisioneros.bonito(estado)}  (estado final)")
    print()

    # --- DFS ---
    print("---------- DFS (max prof. 20) ----------")
    plan, nodos = busquedas.busqueda_profundo(problema, s0, 20)
    if plan:
        print(f"Costo: {plan.costo}, Nodos visitados: {nodos}")
    print()

    # --- IDS ---
    print("---------- IDS ----------")
    plan, nodos = busquedas.busqueda_profundidad_iterativa(problema, s0, 20)
    if plan:
        print(f"Costo: {plan.costo}, Nodos visitados: {nodos}")
    print()

    # --- UCS ---
    print("---------- UCS ----------")
    plan, nodos = busquedas.busqueda_costo_uniforme(problema, s0)
    if plan:
        print(f"Costo: {plan.costo}, Nodos visitados: {nodos}")
    print()

    # --- A* con heurística simple ---
    def h_misioneros(nodo):
        """Personas que faltan por cruzar, divididas entre 2 (capacidad del bote)."""
        m, c, b = nodo.estado
        return (m + c) / 2

    print("---------- A* ----------")
    plan, nodos = busquedas.busqueda_A_estrella(problema, s0, h_misioneros)
    if plan:
        print(f"Costo: {plan.costo}, Nodos visitados: {nodos}")
    print()
