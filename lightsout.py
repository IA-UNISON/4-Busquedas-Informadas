#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'nombre del estudiante'


import busquedas


class LightsOut(busquedas.ModeloBusqueda):
    # --------------------------------------------------------
    # Problema 2:  Completa la clase
    # para el modelo de lights out
    # --------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas
    adjacentes cambian (si estan prendidas se apagan y viceversa).

    El juego consiste en una matriz de 5 X 5, cuyo estado puede
    ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------

    Las acciones posibles son de elegir cambiar una luz y sus casillas
    adjacentes, por lo que la accion es un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def acciones_legales(self, estado):
        return range(25)    #cualquiera de los lugares siempre es legal

    def sucesor(self, estado, accion):
        listado = list(estado)
        n = accion - 5
        o = accion + 1
        s = accion + 5
        e = accion - 1
        afectados = [accion, n, o , s , e]

        if accion < 5:          #si esta en el primer renglon
             afectados.remove(n)
        elif accion >= 20:      #si esta en el ultimo renglon
             afectados.remove(s)

        if accion % 5 == 0:     #si esta en la primer columna
            afectados.remove(e)
        elif accion % 5 == 4:   #si esta en la ultima columna
            afectados.remove(o)

        for afectado in afectados:
            listado[afectado] = 1 if listado[afectado] == 0 else 0

        return tuple(listado)

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        return cadena


# ------------------------------------------------------------
#  Problema 3: Completa el problema de LightsOut
# ------------------------------------------------------------
class ProblemaLightsOut(busquedas.ProblemaBusqueda):
    def __init__(self, pos_ini):
        """
        Utiliza la superclase para hacer el problema

        """
        # Completa el código
        x0 = tuple(pos_ini)
        def meta(x):
            return all(luz == 0 for luz in x)

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    """
    """
    Esta heuristica se basa en el numero de casillas faltantes,
    pero, por si mismo no es admisible (el caso de que falte una
    cruz: faltan 5 casillas pero con un solo movimiento se puede
    solucionar el juego). Para evitar esto se divide el numero de
    casillas faltantes entre 5 y asi este caso (el peor) no hace
    sobreestimacion y hace que la heuristica sea admisible.
    """
    return h_2(nodo) / 5

# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    """
    """
    Esta heuristica es el numero de casillas faltantes.
    No es admisible por las razones que justifique en h_1 pero
    si es rapida y en los juegos de prueba hace muy pocas
    busquedas.
    """
    """
    Algo curioso es que hice varias pruebas moviendo los valores
    del numero de casillas faltantes. Por ejemplo elevando el
    resultado al cuadrado, calculando 10^resultado y e^resultado,
    sacando raiz y logaritmo, y me di cuenta que la raiz y logaritmo
    son pesimos y hacen que se tengan que buscar muchos mas nodos.
    Por otro lado las potencias dieron resultados muy similares
    al mismo resultado sin potencia asi que decidi tomar la opcion
    que hace menos operaciones.
    """
    return sum([1 for casilla in list(nodo.estado) if casilla == 1])


def prueba_modelo():
    """
    Prueba la clase LightsOut

    """

    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 = (1, 0, 0, 1, 0,
              1, 0, 1, 1, 0,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a4 = (1, 0, 0, 0, 1,
              1, 0, 1, 1, 1,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)

    modelo = LightsOut()

    assert modelo.acciones_legales(pos_ini) == range(25)
    assert modelo.sucesor(pos_ini, 0) == pos_a0
    assert modelo.sucesor(pos_a0, 4) == pos_a4
    assert modelo.sucesor(pos_a4, 24) == pos_a24
    assert modelo.sucesor(pos_a24, 15) == pos_a15
    assert modelo.sucesor(pos_a15, 12) == pos_a12
    print("Paso la prueba de la clase LightsOut")


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_2)

    print('-' * 50)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados')
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(10) + str(solucion1.costo).center(20) +
          str(solucion1.nodos_visitados))
    print('A* con h2'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')


if __name__ == "__main__":

    #print("Antes de hacer otra cosa,")
    #print("vamos a verificar medianamente la clase LightsOut")
    #prueba_modelo()

    # Tres estados iniciales interesantes
    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)

    print("\n\nPara el problema en diagonal")
    print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_2)

    print("\n\nPara el problema simétrico")
    print("\n{}".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2)

    print("\n\nPara el problema Bonito")
    print("\n{}".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2)

