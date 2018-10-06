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
from queue import PriorityQueue

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
        return (Nodo(modelo.sucesor(self.estado, a),
                     a,
                     self,
                     modelo.costo_local(self.estado, a))
                for a in modelo.acciones_legales(self.estado))

    def genera_plan(self):
        """
        Genera el plan (parcial o completo) que representa el nodo.

        @return: Una lista [x0, a1, x1, a2, x2, ..., aT, xT], donde
                 los x0, x1, ..., xT son tuplas con los estados a
                 cada paso del plan, mientras que los a1, a2, ..., aT
                 son las acciónes que hay que implementar para llegar desde
                 el estado inicial x0 hasta el testado final xT

        """
        return ([self.estado] if not self.padre else
                self.padre.genera_plan() + [self.accion, self.estado])

    def __str__(self):
        """
        Muestra el nodo como lo que es en realidad, un plan.

        """
        plan = self.genera_plan()
        return ("Costo: {}\n".format(self.costo) +
                "Profundidad: {}\n".format(self.profundidad) +
                "Trayectoria:\n" +
                "".join(["en {} hace {} y va a {},\n".format(x, a, xp)
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
# Referencia: https://github.com/DumbBrain/AI_modern_approach/blob/master/search.py
#
# ---------------------------------------------------------------------
def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
return None


# Metodo memoize - https://www.python-course.eu/python3_memoization.php
def memoize(fun):
	fun.cache = {}
	def _fun(x):
		if x in fun.cache:
			return fun.cache[x]
		y = fun(x)
		fun.cache[x] = y
		return y
	return _fun


def busqueda_primero_mejor(problema, f):
    """
        Busca los nodos con la mejor heuristica, la menor
        Se especifica la funcion que se quiere minimizar (f).

        Si f es una heuristica estamada a la meta, tenemos
            busqueda primero el mejor greedy
        Si f es la profundidad del nodo, tenemos
            busqueda primero a lo ancho

        memoize significa que los valores seran guardados en un cache, como son computados. Entonces despues de hacer busqueda podemos recuperar el camino.
    """
    f = memoize(f)
    nodo = Nodo(problema.x0)
    # Hacemos que la frontera ordene los nodos, partiendo del min, de la funcion f - https://dbader.org/blog/priority-queues-in-python
    frontera = PriorityQueue(f)
    frontera.put(nodo)
    explorados = set()

    while frontera:
        nodo = frontera.get()
        if problema.es_meta(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        for hijo in nodo.expande(problema):
            if hijo.estado not in explorados and hijo not in frontera:
                frontera.put(hijo)
            # dos caminos para un mismo nodo
            elif hijo in frontera:
                # nodo ya encontrado con el mismo hijo.estado
                aux = frontera[hijo]
                # comparamos heurista -
                if f(hijo) < f(aux):
                    # borramos al aux si tiene peor heuristica https://stackoverflow.com/questions/11520492/difference-between-del-remove-and-pop-on-lists/11520540
                    del frontera[aux]
                    frontera.put(hijo)
    # No salimos hasta que hay solucion,,,,
return None


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
    frontera = []

    raise NotImplementedError('Hay que hacerlo de tarea \
                              (problema 2 en el archivo busquedas.py)')
