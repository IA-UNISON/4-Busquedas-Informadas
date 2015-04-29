#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
misioneros_canibales.py
------------

Ejemplo del problema de misioneros y canibales resuelto con diferentes métodos de búsqueda


"""

__author__ = 'Juan Manuel Cruz Luque'


from busquedas import *


class misioneros_canibales(ProblemaBusqueda):

	def __init__(self, m, c, b):

		s_meta = (0,0,0)
		super(misioneros_canibales, self).__init__((m, c, b), lambda s: s == s_meta)

	def acciones_legales(self, estado):

		def es_valido(s):

			if s[0] < 0 or s[1] < 0 or s[0] > 3 or s[1] > 3 or (s[2] != 0 and s[2] != 1):
				return False

			if s[1] > s[0] and s[0] > 0:
				return False

			if s[1] < s[0] and s[0] < 3:
				return False

			return True

		asignacion = []

		if estado[2] == 1:
			sgn = -1
		else:
			sgn = 1

		for m in xrange(3):
			for c in xrange(3):
				s = (estado[0] + sgn * m, estado[1] + sgn * c, estado[2] + sgn * 1)
				if m + c >= 1 and m + c <= 2 and es_valido(s):
					asignacion.append(s)

		return asignacion

	def sucesor(self, estado, accion):

		return accion

def prueba_busqueda(m, c, b, metodo):

        return metodo(misioneros_canibales(m, c, b))

def muestra(m, c, b):

    n1 = prueba_busqueda(m, c, b, busqueda_ancho)
    print "\n\nCon busqueda a lo ancho\n", "-" * 30 + '\n', n1
    print "Explorando ", n1.nodos_visitados, " nodos"

    n2 = prueba_busqueda(m, c, b, busqueda_profundo)
    print "\n\nCon busqueda a lo profundo\n", "-" * 30 + '\n', n2
    print "Explorando ", n2.nodos_visitados, " nodos"

    n3 = prueba_busqueda(m, c, b, busqueda_profundidad_iterativa)
    print "\n\nCon busqueda a lo profundo iterativa\n", "-" * 30 + '\n', n3
    print "Explorando ", n3.nodos_visitados, " nodos"

    n4 = prueba_busqueda(m, c, b, busqueda_costo_uniforme)
    print "\n\nCon costo uniforme\n", "-" * 30 + '\n', n4
    print "Explorando ", n4.nodos_visitados, " nodos"

if __name__ == "__main__":

    print "Vamos a ver como funcionan las busquedas en el juego misioneros y canibales."
    muestra(3, 3, 1)

