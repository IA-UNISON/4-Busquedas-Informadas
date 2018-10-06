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
    Problema de los dos botes, donde x = (x0, x1)
    es el estado con la cantidad de agua en el cubo 0 y 1.

    Acciones = {('vaciar', 0), ('vaciar', 1),
                ('llenar', 0), ('llenar', 1),
                ('pasar', 0), ('pasar', 1)}

    se entiende que ('pasar', 0) es pasar agua del
    primer cubo al segundo cubo.

    y además se guarda el valor de x0_max y x1_max)

    """
    def __init__(self, x0_max, x1_max):
        self.maximos = (x0_max, x1_max)

    def acciones_legales(self, estado):

        return [(op, cubo)
                for op in ['vaciar', 'llenar', 'pasar'] for cubo in [0, 1]
                if (op is 'vaciar' and estado[cubo] > 0) or
                (op is 'llenar' and estado[cubo] < self.maximos[cubo]) or
                (op is 'pasar' and estado[cubo] > 0 and
                 estado[1 - cubo] < self.maximos[1 - cubo])]

    def sucesor(self, estado, accion):

        x = list(estado)
        verbo, cubo = accion
        if verbo is 'vaciar':
            x[cubo] = 0
        elif verbo is 'llenar':
            x[cubo] = self.maximos[cubo]
        else:
            delta = min(x[cubo], self.maximos[1 - cubo] - x[1 - cubo])
            x[cubo] -= delta
            x[1 - cubo] += delta
        return tuple(x)


class ModeloDosBotesAgua(ModeloDosBotes):
    def costo_local(self, estado, accion):
        a, i = accion
        costo = 0.01
        if a is 'llenar':
            costo += self.maximos[i] - estado[i]
        return costo


class PblDosBotes(busquedas.ProblemaBusqueda):
    def __init__(self, x0_max, x1_max, deseado):
        super().__init__((0, 0),
                         lambda x: deseado in x,
                         ModeloDosBotes(x0_max, x1_max))


class PblDosBotesAgua(busquedas.ProblemaBusqueda):
    def __init__(self, x0_max, x1_max, deseado):
        super().__init__((0, 0),
                         lambda x: deseado in x,
                         ModeloDosBotesAgua(x0_max, x1_max))


def el_problema_mas_largo(max_cubo):
    def costo_solucion(x):
        sol = busquedas.busqueda_ancho(PblDosBotes(x[0], x[1], x[2]))
        return 0 if sol is None else sol.costo

    return max(((i, j, x) for i in range(2, max_cubo + 1)
                for j in range(1, i) for x in range(1, i)),
               key=costo_solucion)


def el_problema_mas_antiecologico(max_cubo):
    def costo_solucion(x):
        sol = busquedas.busqueda_costo_uniforme(PblDosBotes(x[0], x[1], x[2]))
        return 0 if sol is None else sol.costo

    return max(((i, j, x) for i in range(2, max_cubo + 1)
                for j in range(1, i) for x in range(1, i)),
               key=costo_solucion)


#if __name__ is "__main__":

print("Vamos a ver como se resuleve el problema")
print("de un bote de 7, otro de 5, si queremos tener 3 litros al final")
print(busquedas.busqueda_ancho(PblDosBotes(7, 5, 3)))

a, b, x = el_problema_mas_largo(15)
print("\n\nEl problema que más pasos tiene uno que hacer")
print("si el bote mayor puede tener 15 litros es de")
print("un cubo de {}, otro de {}, y tener {} en uno".format(a, b, x))

a, b, x = el_problema_mas_antiecologico(15)
print("\n\nEl problema que más agua gasta")
print("si el bote mayor puede tener 15 litros es de")
print("un cubo de {}, otro de {}, y tener {} en uno".format(a, b, x))
