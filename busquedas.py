#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
busquedas.py
------------

Clases y algoritmos necesarios para desarrollar agentes de
búsquedas en entornos determinísticos conocidos discretos
completamente observables

"""

__author__ = 'juliowaissman'

from collections import deque
import heapq


class ModeloBusqueda:
    """
    Clase genérica de un modelo de búsqueda.

    Todo modelo de búsqueda debe de tener:
        1) Un método que obtenga las acciones legales en cada estado
        2) Un método que calcule cual es es siguiente estado
        3) Una función de costo local

    """
    def acciones_legales(self, estado):
        """
        Lista de acciones legales en un estado dado.

        @param estado: Una tupla con un estado válido.

        @return: Una lista de acciones legales.

        """
        raise NotImplementedError("No implementado todavía.")

    def sucesor(self, estado, accion):
        """
        Estado sucesor

        @param estado: Una tupla con un estado válido.
        @param accion: Una acción legal en el estado.

        @return: Una tupla con el estado sucesor de estado cuando
                 se aplica la acción.

        """
        raise NotImplementedError("No implementado todavía.")

    def costo_local(self, estado, accion):
        """
        Calcula el costo de realizar una acción en un estado.

        @param estado: Una tupla con un estado válido.
        @param acción: Una acción legal en estado.

        @return: Un número positivo con el costo de realizar
                 la acción en el estado.

        """
        return 1


class ProblemaBusqueda:
    """
    Clase genérica de un problema de búsqueda.

    Todo problema de búsqueda debe de tener:
        a) Un estado inicial
        b) Una función que diga si un estado es una meta o no
        c) Un modelo para la búsqueda

    """
    def __init__(self, x0, meta, modelo):
        """
        Inicializa el problema de búsqueda

        @param x0: Una tupla con un estado válido del
                   problema (estado inicial).
        @param meta: Una función meta(s) --> bool,
                     donde meta(s) devuelve True solo
                     si el estado s es un estado objetivo.
        @param modelo: Un objeto de la clase ModeloBusqueda

        """
        def es_meta(estado):
            self.num_nodos += 1
            return meta(estado)
        self.es_meta = es_meta

        self.x0 = x0
        self.modelo = modelo
        self.num_nodos = 0  # Solo para efectos medición


class Nodo:
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
        self.nodos_visitados = 0

    def expande(self, modelo):
        """
        Expande un nodo en todos sus nodos hijos de acuerdo al problema pb

        @param modelo: Un objeto de una clase heredada de ModeloBusqueda

        @return: Una lista de posibles nodos sucesores

        """
        return (
            Nodo(
                modelo.sucesor(self.estado, a),
                a,
                self,
                modelo.costo_local(self.estado, a))
            for a in modelo.acciones_legales(self.estado))

    def genera_plan(self):
        """
        Genera el plan (parcial o completo) que representa el nodo.

        @return: Una lista [(x0, c0), a1, (x1, c1), a2, (x2, c2), ..., aT, (xT, cT)], donde los x0, x1, ..., xT son tuplas con los estados a cada paso del plan, c0, c1, ..., cT es el costo total hasta ese momento del plan, a1, a2, ..., aT son las acciónes que hay que implementar para llegar desde el estado inicial x0 hasta el testado final xT

        """
        return ([(self.estado, self.costo)] if not self.padre else
                (self.padre.genera_plan() 
                 + [self.accion, (self.estado, self.costo)]))

    def __str__(self):
        """
        Muestra el nodo como lo que es en realidad, un plan.

        """
        plan = self.genera_plan()
        return (f"Costo: {self.costo}\n" +
                f"Profundidad: {self.profundidad}\n" +
                f"Trayectoria:\n" +
                "".join([f"en {x[0]} hace {a} y va a {xp[0]} con costo {xp[1]},\n"
                         for (x, a, xp)
                         in zip(plan[:-1:2], plan[1::2], plan[2::2])]))

    # Este método de sobrecarga del operador < es necesario
    # para poder utilizar los nodos en la heapq
    def __lt__(self, other):
        return self.profundidad < other.profundidad


def busqueda_ancho(problema):
    """
    Búsqueda a lo ancho para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con un plan completo

    """
    if problema.es_meta(problema.x0):
        return Nodo(problema.x0)

    frontera = deque([Nodo(problema.x0)])
    visitados = {problema.x0}

    while frontera:
        nodo = frontera.popleft()
        for hijo in nodo.expande(problema.modelo):
            if hijo.estado in visitados:
                continue
            if problema.es_meta(hijo.estado):
                hijo.nodos_visitados = problema.num_nodos
                return hijo
            frontera.append(hijo)
            visitados.add(hijo.estado)
    return None


def busqueda_profundo(problema, max_profundidad=None):
    """
    Búsqueda a lo profundo para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    frontera = deque([Nodo(problema.x0)])
    visitados = {problema.x0: 0}

    while frontera:
        nodo = frontera.pop()
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        if max_profundidad is not None and max_profundidad == nodo.profundidad:
            continue
        for hijo in nodo.expande(problema.modelo):
            # or visitados[hijo.estado] > hijo.profundidad:
            if (hijo.estado not in visitados or
                visitados[hijo.estado] > hijo.profundidad):
                frontera.append(hijo)
                visitados[hijo.estado] = hijo.profundidad
    return None


def busqueda_profundidad_iterativa(problema, max_profundidad=20):
    """
    Búsqueda por profundidad iterativa dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    for profundidad in range(max_profundidad):
        resultado = busqueda_profundo(problema, profundidad)
        if resultado is not None:
            return resultado
    return None


def busqueda_costo_uniforme(problema):
    """
    Búsqueda por costo uniforme

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    frontera = []
    heapq.heappush(frontera, (0, Nodo(problema.x0)))
    visitados = {problema.x0: 0}

    while frontera:
        (_, nodo) = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema.modelo):
            if (hijo.estado not in visitados or
                visitados[hijo.estado] > hijo.costo):
                heapq.heappush(frontera, (hijo.costo, hijo))
                visitados[hijo.estado] = hijo.costo
    return None

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
    #raise NotImplementedError('Hay que hacerlo de tarea \
    #                          (problema 2 en el archivo busquedas.py)')
