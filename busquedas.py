#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
busquedas.py
------------

Clases y algoritmos necesarios para desarrollar agentes de
búsquedas en entornos determinísticos conocidos discretos
completamente observables

"""
from collections import deque
import heapq


class ProblemaBusqueda:
    """
    Clase genérica de un modelo de búsqueda.

    Todo modelo de búsqueda debe de tener:
        1) Un método que obtenga las acciones legales en cada estado
        2) Un método que calcule cual es es siguiente estado
        3) Una función de costo local

    """
    def acciones(self, estado):
        """
        Lista de acciones legales en un estado dado.

        @param estado: Una tupla con un estado válido.
        @return: Una lista de acciones legales.

        """
        raise NotImplementedError("No implementado todavía el método acciones.")

    def sucesor(self, estado, accion):
        """
        Estado sucesor

        @param estado: Una tupla con un estado válido.
        @param accion: Una acción legal en el estado.
        @return: estado_sucesor, costo_local. 
                 Una tupla con el estado sucesor y 
                 un número con el costo local de realizar la acción en el estado.

        """
        raise NotImplementedError("No implementado todavía el método sucesor.")

    def terminal(self, estado):
        """
        Determina si un estado es terminal o no.

        @param estado: Una tupla con un estado válido.
        @return: True si el estado es terminal, False en caso contrario.

        """
        raise NotImplementedError("No implementado todavía el método terminal.")


class NodoBusqueda:
    """
    Clase para implementar un árbol como estructura de datos.

    """
    def __init__(self, estado, accion=None, padre=None, costo_local=0):
        """
        Inicializa un nodo como una estructura

        """
        self.estado = estado
        self.accion = accion
        self.padre = padre
        self.costo = 0 if not padre else padre.costo + costo_local
        self.profundidad = 0 if not padre else padre.profundidad + 1

    def expande(self, pb_busqueda):
        """
        Expande un nodo en todos sus nodos hijos de acuerdo al problema pb_busqueda

        @param pb_busqueda: Un objeto de una clase heredada de ProblemaBusqueda
        @return: Un generador de posibles nodos sucesores

        """
        for a in pb_busqueda.acciones(self.estado):
            estado_sucesor, costo_local = pb_busqueda.sucesor(self.estado, a)
            yield NodoBusqueda(
                estado_sucesor,
                a,
                self,
                costo_local)

    def genera_plan(self):
        """
        Genera el plan (parcial o completo) que representa el nodo.

        @return: Una lista [(x0, a0, c0), (x1, a1, c1), ..., (xT-1, aT-1, cT-1), (xT, None, None)],
                    donde xi es el estado i-ésimo, ai es la acción que se realizara el estado xi
                    para llegar al estado xi+1, y ci es el costo acumulado de realizar las acciones a0 a ai.
                    El último elemento de la lista representa el estado final del plan, por lo que no tiene
                    acción ni costo asociado. 

        """
        return (
            [(self.estado, None, None)] if self.padre is None else
             self.padre.genera_plan()[:-1] + [(self.padre.estado, self.accion, self.costo), 
                                              (self.estado, None, None)]
        )

    def __str__(self):
        """
        Muestra el nodo como lo que es en realidad, un plan.

        """
        plan = self.genera_plan()
        return (f"Costo: {self.costo}\n" +
                f"Profundidad: {self.profundidad}\n" +
                f"Trayectoria:\n" +
                "".join([f"en {x} hace {a} con costo acumulado {c},\n"
                         for (x, a, c) in plan[:-1]] + [f'{plan[-1][0]} es el estado final.']))

    
    def __lt__(self, other):
        "Ordena nodos por su profundidad sobrecargando <"
        return self.profundidad < other.profundidad


def busqueda_ancho(problema, s0):
    """
    Búsqueda a lo ancho para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con un plan completo

    """
    nodos_visitados = 1
    if problema.terminal(s0):
        return NodoBusqueda(s0)

    frontera = deque([NodoBusqueda(s0)])
    estados_visitados = {s0}

    while frontera:
        plan = frontera.popleft()
        for hijo in plan.expande(problema):
            if hijo.estado in estados_visitados:
                continue
            nodos_visitados += 1
            if problema.terminal(hijo.estado):
                return hijo, nodos_visitados
            frontera.append(hijo)
            estados_visitados.add(hijo.estado)
    return None, nodos_visitados


def busqueda_profundo(problema, s0, max_profundidad=None):
    """
    Búsqueda a lo profundo para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    frontera = deque([NodoBusqueda(s0)])
    visitados = {s0}
    nodos_visitados = 0

    while frontera:
        plan = frontera.pop()
        nodos_visitados += 1
        if problema.terminal(plan.estado):
            return plan, nodos_visitados
        if max_profundidad is not None and max_profundidad == plan.profundidad:
            continue
        for hijo in plan.expande(problema):
            # or visitados[hijo.estado] > hijo.profundidad:
            if (hijo.estado not in visitados):
                frontera.append(hijo)
                visitados.add(hijo.estado)
    return None, nodos_visitados


def busqueda_profundidad_iterativa(problema, s0, max_profundidad=20):
    """
    Búsqueda por profundidad iterativa dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda
    @return Un objeto tipo Nodo con la estructura completa

    """
    nodos_visitados = 0
    for profundidad in range(1, max_profundidad + 1):
        plan, nodos = busqueda_profundo(problema, s0, profundidad)
        nodos_visitados += nodos
        if plan is not None:
            return plan, nodos_visitados
    return None, nodos_visitados


def busqueda_costo_uniforme(problema, s0):
    """
    Búsqueda por costo uniforme

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    frontera = []
    heapq.heappush(frontera, (0, NodoBusqueda(s0)))
    visitados = {s0: 0}
    nodos_visitados = 0

    while frontera:
        _, plan = heapq.heappop(frontera)
        nodos_visitados += 1
        if problema.terminal(plan.estado):
            return plan, nodos_visitados
        for hijo in plan.expande(problema):
            if (hijo.estado not in visitados or visitados[hijo.estado] > hijo.costo):
                heapq.heappush(frontera, (hijo.costo, hijo))
                visitados[hijo.estado] = hijo.costo
    return None, nodos_visitados

# ---------------------------------------------------------------------
#
# Problema 1: Desarrolla el método de búsqueda de A* siguiendo las
# especificaciones de la función pruebalo con el 8 puzzle
# (ocho_puzzle.py) antes de hacerlo en el Lights_out que es mucho más
# dificl (en el archivo se incluyen las heurísticas del 8 puzzle y el
# resultado esperado)
#
# ---------------------------------------------------------------------


def busqueda_A_estrella(problema, heuristica):
    """
    Búsqueda A*

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param heuristica: Una funcion de heuristica, esto es, una función
                       heuristica(nodo), la cual devuelva un número mayor
                       o igual a cero con el costo esperado desde nodo hasta
                       un nodo cuyo estado final sea méta.

    @return Un objeto tipo Nodo con la estructura completa

    """
    raise NotImplementedError('Hay que hacerlo de tarea \
                              (problema 2 en el archivo busquedas.py)')
