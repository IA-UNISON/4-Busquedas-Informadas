#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'nombre del estudiante'


from busquedas import *
import numpy as np

class Lights_out(ProblemaBusqueda):
#----------------------------------------------------------------------------
# Problema 2 (25 puntos): Completa la clase para el problema de lights out
#
#----------------------------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas adjacentes cambian
    (si estan prendidas se apagan y viceversa). El juego consiste en una matriz
    de 5 X 5, cuyo estado puede ser apagado 0 o 
    prendido 1. Por ejemplo el estado

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
    adjacentes, por lo que la accion es
    un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self, pos_inicial):
        # ¡El formato y lo que lleva la inicialización de 
        # la super hay que cambiarlo al problema!
        #super(Lights_out, self).__init__(s0, meta)
        s_meta = tuple([0 for i in xrange(25)])
        super(Lights_out, self).__init__(pos_inicial, lambda s: s == s_meta)
        # raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        return range(25)
        # raise NotImplementedError('Hay que hacerlo de tarea')

    

    def sucesor(self, estado, accion):
        estado_nuevo = list(estado)
        estado_nuevo[accion] = (estado_nuevo[accion] + 1)%2
        vecinos = obtener_ady(accion)
        for i in vecinos:
            estado_nuevo[i] = (estado_nuevo[i] + 1)%2
        return tuple(estado_nuevo)
        # raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        return 1
        # raise NotImplementedError('Hay que hacerlo de tarea')

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

def obtener_ady(accion):
    a = []
    if accion + 5 <= 24:
        a.append(accion + 5)
    if accion - 5 >= 0:
        a.append(accion - 5)
    if accion%5 != 4:
        a.append(accion + 1)
    if accion%5 != 0:
        a.append(accion - 1)
    return a

#-------------------------------------------------------------------------------------------------
# Problema 3 (25 puntos): Desarrolla una política admisible. 
#-------------------------------------------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
    LA HEURÍSTICA ES ADMISIBLE

    La idea de la heuristica es que mientras mas luces esten prendidas (1) en
    las casillas adyacentes, de cada casilla, es mejor, por que asi hay mas
    posibilidad de llegar al estado meta con menos cantidad de movimientos.
    Por lo tanto, penaliza si no hay luces prendidas en las casillas
    adyacentes a cada una.
    Creo que la heuristica es admisible porque en el estado meta, h1 da 0
    """

    acc = 0
    costo = 0
    est = np.array([list(nodo.estado)])
    unos = np.where(est == 1)[1]
    for i in unos:
        if nodo.estado[i] == 1:
            acc += 1
        for j in obtener_ady(i):
            if nodo.estado[j] == 1:
                acc += 1
        costo += 1/(acc+.1)
        acc = 0
    return costo

#-------------------------l------------------------------------------------------------------------
# Problema 4 (25 puntos): Desarrolla otra política admisible. 
# Analiza y di porque piensas que es (o no es) dominante una respecto otra política
#-------------------------------------------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
    LA HEURÍSTICA ES ADMISIBLE

    Hice 3 intentos de heuristica, los 2 primeros no los pude comprobar porque me comian
    la memoria del ordenador :(.. pero el que mas me convencio (creo que es correcto)
    es el que no esta comentado.
    Es bastante sencillo, consiste en contar las casillas que tienen una
    casilla a la derecha adyacente a ella y al final el numero de casillas
    que cumplieron con esta condicion (mas su respectiva casilla a la derecha) 
    dividirlo entre 2.
    Porque ?.. Me base en la idea de un problema relajado para el juego, en vez
    de que al presionar una casilla, se cambien de valor las 5 adyacentes a esta,
    solo se cambia la misma y la de la derecha. Por ejemplo:
    ---------------------
    | X | X |   | X | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    |   |   |   | X | X |
    ---------------------
    |   | X |   |   |   |
    ---------------------
    |   |   |   | X | X |
    ---------------------
    En esa configuracion, si contamos las casillas que tienen un 1,
    y a su derecha otro 1, nos da un total 10, al dividir 10/2 nos da 5.
    Esto es el minimo numero de movimientos que podemos hacer para llegar
    a una solución, cabe resaltar que son movimientos "minimos", dado que
    en la mayoria de las veces hay casillas solas (separadas) y este hace
    que se requieran mas movimientos.
    Es por esa misma razon que la heuristica se basa en una configuracion
    casi ideal (como la del ejemplo), la cual no es tan probalble que ocurra.
    La heuristica es admisible porque si tenemos en el tablero solo dos
    luces prendidas (juntas con orientacion horizontal), hace falta solo un 
    movimiento para llegar a la solucion, en cambio en el problema no
    relajado, esto no sucede asi, harian falta mas movimientos dado que se 
    prenderian las casillas de arriba, abajo y a la izquierda, lo cual
    genera mas costo para llegar a la solucion final.

    """

    """

    PRIMER INTENTO

    estado = np.asarray(nodo.estado).reshape((5,5))
    acc = 5
    for i in estado:
        if not 1 in i:
            acc -= 1
            break
    return acc
    """

    """
    SEGUNDO INTENTO
    estado = np.asarray(nodo.estado).reshape((5, 5))
    acc = 0
    for i in estado:
        if i[0] == i[-1] == 1:
            acc += 1
    return 1 / (acc + .1)
    """

    # TERCER INTENTO
    a = [i for i in xrange(25) if i%5 != 4]
    acc = 0
    for j in a:
        if nodo.estado[j] == nodo.estado[j + 1] == 1:
            acc += 2
    return acc / 2.0


def prueba_clase():
    """
    Prueba la clase Lights_out

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

    pos_a4 =  (1, 0, 0, 0, 1,
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


    entorno = Lights_out(pos_ini)

    assert entorno.acciones_legales(pos_ini) == range(25)
    assert entorno.sucesor(pos_ini, 0) == pos_a0
    assert entorno.sucesor(pos_a0, 4) == pos_a4
    assert entorno.sucesor(pos_a4, 24) == pos_a24
    assert entorno.sucesor(pos_a24, 15) == pos_a15
    assert entorno.sucesor(pos_a15, 12) == pos_a12
    print "Paso la prueba de la clase"
    

def prueba_busqueda(pos_inicial, metodo, heuristica=None, max_prof=None):
    """
    Prueba un método de búsqueda para el problema del ligths out.

    @param pos_inicial: Una tupla con una posicion inicial
    @param metodo: Un metodo de búsqueda a probar
    @param heuristica: Una función de heurística, por default None si el método de búsqueda no requiere heuristica
    @param max_prof: Máxima profundidad para los algoritmos de DFS y IDS.

    @return nodo: El nodo solución

    """
    if heuristica:
        return metodo(Lights_out(pos_inicial), heuristica)
    elif max_prof:
        return metodo(Lights_out(pos_inicial), max_prof)
    else:
        return metodo(Lights_out(pos_inicial))


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla de la función
    """
    # n1 = prueba_busqueda(pos_inicial, busqueda_ancho)
    # n2 = prueba_busqueda(pos_inicial, busqueda_profundidad_iterativa)
    # n3 = prueba_busqueda(pos_inicial, busqueda_costo_uniforme)
    # n4 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_1)
    n5 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_2)

    print '\n\n' + '-' * 50
    print 'Método'.center(10) + 'Costo de la solucion'.center(20) + 'Nodos explorados'.center(20)
    print '-' * 50
    # print 'BFS'.center(10) + str(n1.costo).center(20) + str(n1.nodos_visitados)
    # print 'IDS'.center(10) + str(n2.costo).center(20) + str(n2.nodos_visitados)
    # print 'UCS'.center(10) + str(n3.costo).center(20) + str(n3.nodos_visitados)
    # print 'A* con h1'.center(10) + str(n4.costo).center(20) + str(n4.nodos_visitados)
    print 'A* con h2'.center(10) + str(n5.costo).center(20) + str(n5.nodos_visitados)
    print ''
    print '-' * 50 + '\n\n'

if __name__ == "__main__":

    print "Antes de hacer otra cosa vamos a verificar <medianamente>    </medianamente> la clase Lights_out"
    prueba_clase()

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

    print "\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(diagonal)
    compara_metodos(diagonal, h_1, h_2)

    print "\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(simetria)
    compara_metodos(simetria, h_1, h_2)

    print "\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(problemin)
    compara_metodos(problemin, h_1, h_2)
