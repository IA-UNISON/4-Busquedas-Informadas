#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dos_botes.py
------------

Una pequeña aplicación de las búsquedas

"""
__author__ = 'nombre del estudiante'


import busquedas


class ModeloDosBotes(busquedas.ModeloBusqueda):
    """
    Problema de los dos botes, donde x=(A, B)
    es el estado con la cantidad de agua en A y B.

    Acciones = {('vaciar', 0), ('vaciar', 1),
                ('llenar', 0), ('llenar', 1),
                ('pasar', 0), ('pasar', 1)}

    se entiende que ('pasar', 0) es pasar agua del
    primer cubo al segundo cubo.

    y además se guarda el valor de A_max y B_max)

    """
    def __init__(self, A_max, B_max):
        """

        """
        self.maximos = (A_max, B_max)

    def acciones_legales(self, estado):
        return ([('vaciar', i) for i in [0, 1]
                 if estado[i] > 0] +
                [('llenar', i) for i in [0, 1]
                 if estado[i] < self.maximos[i]] +
                [('pasar', i) for i in [0, 1]
                 if estado[i] > 0 and estado[1 - i] < self.maximos(1 - i)])

    def sucesor(estado, acción)
