#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
busquedas.py
------------

Clases y algoritmos necesarios para desarrollar agentes de búsquedas en entornos determinísticos
conocidos discretos completamente observables

"""

__author__ = 'juliowaissman'

from collections import deque
import heapq


class ProblemaBusqueda(object):

    """
    Clase genérica de un problema de búsqueda.

    Todo problema de búsqueda debe de tener:
        a) Un estado inicial
        b) Una función que diga si un estado es una meta o no
        c) Un método que obtenga las acciones legales en cada estado
        d) Un método que calcule cual es es siguiente estado
        e) Una función de costo local

    """

    def __init__(self, s0, meta):
        """
        Inicializa el problema de búsqueda

        @param s0: Una tupla con un estado válido del problema (estado inicial).
        @param meta: Una función meta(s) --> bool, donde meta(s) devuelve True solo
        si el estado s es un estado objetivo.

        """
        def es_meta(estado):
            self.num_nodos += 1
            return meta(estado)
        self.es_meta = es_meta

        self.s0 = s0
        self.num_nodos = 0  # Solo para efectos medición

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

        @return: Una tupla con el estado sucesor de estado cuando de aplica la acción accion.

        """
        raise NotImplementedError("No implementado todavía.")

    def costo_local(self, estado, accion):
        """
        Calcula el costo de realizar una acción en un estado.

        @param estado: Una tupla con un estado válido.
        @param accion: Una acción legal en estado.

        @return: Un número positivo con el costo de realizar la acción en el estado.
        """
        return 1


class Nodo(object):

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

    def expande(self, pb):
        """
        Expande un nodo en todos sus posibles nodos hijos de acuero al problema pb

        @param pb: Un objeto de una clase heredada de ProblemaBusqueda

        @return: Una lista de posibles nodos sucesores

        """
        return [Nodo(pb.sucesor(self.estado, a), a, self, pb.costo_local(self.estado, a))
                for a in pb.acciones_legales(self.estado)]

    def lista_acciones(self):
        """
        Lista de acciones desde la raiz a este nodo.

        @return: Una lista desde la primer acción hasta la última

        """
        return [] if not self.padre else self.padre.lista_acciones() + [self.accion]

    def lista_estados(self):
        """
        Lista de estados desde la raiz a este nodo.

        @return: Una lista desde el estado del nodo raiz hasta este nodo

        """
        return [self.estado] if not self.padre else self.padre.lista_estados() + [self.estado]

    def __str__(self):
        acciones = self.lista_acciones()
        estados = self.lista_estados()
        return ("Costo: " + str(self.costo) +
                "\nProfundidad: " + str(self.profundidad) +
                "\nTrayectoria:\n" +
                "".join(["en %s hace %s\n" % (str(e), str(a)) for (e, a) in zip(estados[:-1], acciones)]) +
                "para terminar en " + str(estados[-1]))


def busqueda_ancho(problema):
    """
    Búsqueda a lo ancho para un problema de búsquedas dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    if problema.es_meta(problema.s0):
        return Nodo(problema.s0)

    frontera = deque([Nodo(problema.s0)])
    visitados = {problema.s0}

    while frontera:
        nodo = frontera.popleft()
        for hijo in nodo.expande(problema):
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
    frontera = deque([Nodo(problema.s0)])
    visitados = {problema.s0: 0}

    while frontera:
        nodo = frontera.pop()
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        if max_profundidad is not None and max_profundidad == nodo.profundidad:
            continue
        for hijo in nodo.expande(problema):
            # or visitados[hijo.estado] > hijo.profundidad:
            if hijo.estado not in visitados:
                frontera.append(hijo)
                visitados[hijo.estado] = hijo.profundidad
    return None


def busqueda_profundidad_iterativa(problema, max_profundidad=10000):
    """
    Búsqueda por profundidad iterativa dado

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param max_profundidad: Máxima profundidad de búsqueda

    @return Un objeto tipo Nodo con la estructura completa

    """
    for profundidad in xrange(1, max_profundidad):
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
    heapq.heappush(frontera, (0, Nodo(problema.s0)))
    visitados = {problema.s0: 0}

    while frontera:
        (_, nodo) = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema):
            if hijo.estado not in visitados or visitados[hijo.estado] > hijo.costo:
                heapq.heappush(frontera, (hijo.costo, hijo))
                visitados[hijo.estado] = hijo.costo
    return None

#-------------------------------------------------------------------------------------------------
#
# Problema 2 (25 puntos): Desarrolla el método de búsqueda de A* siguiendo las especificaciones 
# de la función pruebalo con el 8 puzzle (ocho_puzzle.py) antes de hacerlo en el Lights_out que es 
# mucho más dificl (en el archivo se incluyen las heurísticas del 8 puzzle y el resultado esperado)
#
#-------------------------------------------------------------------------------------------------

def busqueda_A_estrella(problema, heuristica):
    """
    Búsqueda A*

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param heuristica: Una funcion de heuristica, esto es, una función heuristica(nodo), la cual devuelva
                       un número mayor o igual a cero con el costo esperado desde nodo hasta un nodo 
                       objetivo.

    @return Un objeto tipo Nodo con la estructura completa

    
    """
    raise NotImplementedError('Hay que hacerlo de tarea (problema 2 en el archivo busquedas.py)')


