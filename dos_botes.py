#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dos_botes.py
------------

Una pequeña aplicación de las búsquedas

"""
__author__ = 'joaquinsotelo'


import busquedas


class PbDosBotes(busquedas.ProblemaBusqueda):
    """
    Problema de los dos botes, donde x = (x0, x1) es el estado con la cantidad de agua en el cubo 0 y 1.

    Acciones = {('vaciar', 0), ('vaciar', 1),
                ('llenar', 0), ('llenar', 1),
                ('pasar', 0), ('pasar', 1)}

    se entiende que ('pasar', 0) es pasar agua del primer cubo al segundo cubo.
    
    Se guarda el valor de x0_max y x1_max)

    """
    def __init__(self, x0_max, x1_max, meta=0):
        self.maximos = (x0_max, x1_max)
        self.meta = meta

    def acciones(self, estado):
        return [
            (op, cubo) for op in ['vaciar', 'llenar', 'pasar'] for cubo in [0, 1]
            if ( (op == 'vaciar' and estado[cubo] > 0) 
                  or (op == 'llenar' and estado[cubo] < self.maximos[cubo]) 
                  or (op == 'pasar' and estado[cubo] > 0 and estado[1 - cubo] < self.maximos[1 - cubo])
            )
        ]

    def sucesor(self, estado, accion):
        costo_local = self.calculo_costo_local(estado, accion)
        x = list(estado[:])
        verbo, cubo = accion
        if verbo == 'vaciar':
            x[cubo] = 0
        elif verbo == 'llenar':
            x[cubo] = self.maximos[cubo]
        else:
            delta = min(x[cubo], self.maximos[1 - cubo] - x[1 - cubo])
            x[cubo] -= delta
            x[1 - cubo] += delta
        return tuple(x), costo_local
    
    def calculo_costo_local(self, estado, accion):
        return 1
    
    def terminal(self, estado):
        return self.meta in estado


class PbDosBotesCostoAgua(PbDosBotes):
    def calculo_costo_local(self, estado, accion):
        a, i = accion
        costo = 0.01
        if a == 'llenar':
            costo += self.maximos[i] - estado[i]
        return costo


def el_problema_mas_largo(max_cubo):
    def costo_solucion(x):
        plan, _ = busquedas.busqueda_ancho(PbDosBotes(x[0], x[1], x[2]), (0, 0))
        return 0 if plan is None else plan.costo

    return max(((i, j, x) for i in range(2, max_cubo + 1)
                for j in range(1, i) for x in range(1, i)),
               key=costo_solucion)


def el_problema_mas_antiecologico(max_cubo):
    def costo_solucion(x):
        plan, _ = busquedas.busqueda_costo_uniforme(PbDosBotesCostoAgua(x[0], x[1], x[2]), (0, 0))
        return 0 if plan is None else plan.costo

    return max(((i, j, x) for i in range(2, max_cubo + 1)
                for j in range(1, i) for x in range(1, i)),
               key=costo_solucion)


if __name__ == "__main__":

    print("Vamos a ver como se resuleve el problema")
    print("de un bote de 7, otro de 5, si queremos tener 3 litros al final")
    plan, nodos_visitados = busquedas.busqueda_ancho(PbDosBotes(7, 5, 4), (0, 0))
    print(f"Plan: {plan}")
    print(f"Nodos visitados: {nodos_visitados}")

    a, b, x = el_problema_mas_largo(15)
    print("\n\nEl problema que más pasos tiene uno que hacer")
    print("si el cubo mayor puede tener hasta 15 litros es de")
    print(f"un cubo de {a} litros, otro de {b} litros, y tener {x} en alguno de los cubos al final")

    a, b, x = el_problema_mas_antiecologico(15)
    print("\n\nEl problema que más agua gasta")
    print("si el cubo mayor puede tener hasta 15 litros es de")
    print(f"un cubo de {a} litros, otro de {b} litros, y tener al final {x} en alguno de los cubos")
