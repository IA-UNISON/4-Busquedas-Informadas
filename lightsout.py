#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Juan Manuel Cruz Luque'


from busquedas import *


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
    de 5 X 5, cuyo estado puede ser apagado 0 o prendido 1. Por ejemplo el estado

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

    Las acciones posibles son de elegir cambiar una luz y sus casillas adjacentes, por lo que la accion es
    un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self, pos_inicial):
        # ¡El formato y lo que lleva la inicialización de
        # la super hay que cambiarlo al problema!
        #super(Lights_out, self).__init__(s0, meta)
        s_meta = tuple(map(lambda s: 0, pos_inicial))
        super(Lights_out, self).__init__(pos_inicial, lambda s: s == s_meta)
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        return range(25)
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        def obtener_indice(renglon, columna):
            return columna + renglon * 5

        s = list(estado)
        renglon = accion // 5
        columna = accion % 5

        if s[accion] == 1:
            s[accion] = 0
        else:
            s[accion] = 1

        if renglon > 0:

            indice = obtener_indice(renglon - 1, columna)

            if s[indice] == 0:
                s[indice] = 1
            else:
                s[indice] = 0

        if renglon < 4:

            indice = obtener_indice(renglon + 1, columna)

            if s[indice] == 0:
                s[indice] = 1
            else:
                s[indice] = 0

        if columna > 0:

            indice = obtener_indice(renglon, columna - 1)

            if s[indice] == 0:
                s[indice] = 1
            else:
                s[indice] = 0

        if columna < 4:

            indice = obtener_indice(renglon, columna + 1)

            if s[indice] == 0:
                s[indice] = 1
            else:
                s[indice] = 0

        return tuple(s)
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        return 1
        #raise NotImplementedError('Hay que hacerlo de tarea')

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

#-------------------------------------------------------------------------------------------------
# Problema 3 (25 puntos): Desarrolla una política admisible.
#-------------------------------------------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
    LA HEURÍSTICA ES ADMISIBLE

    Bueno esta heuristica funciona de la siguiente manera, cuando comence a agarrarle la onda de como
    ganar en el lights out, empece a seguir un orden. Al principio apagaba el primer renglon pulsando
    la columna debajo de cada casilla, despues hacia lo siguiente con el proximo renglon
    y asi hasta el ultimo. Cuando llegaba al ultimo y no habia ganado volvia encender una casilla del
    primer renglon y seguia el mismo procedimiento hasta que ganaba. Esta heuristica Es lo que hace,
    comienza en el segundo renglon y revisa el renglon de arriba si hay casillas encendidas penaliza
    y asi sucesivamente solo que aqui no volvemos a encender una primer casilla para seguir. Aqui
    muestro un ejemplo de como funciona, la X significa que esta encendido.


    ---------------------   ---------------------   ---------------------   ---------------------
    | X | X |   | X | X |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------
    | X | X | X | X | X |   | X | X | X | X | X |   |   |   |   |   | X |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------
    |   | X |   | X |   |   | X |   |   |   | X |   |   |   |   | X | X |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------
    | X | X | X | X | X |   | X | X | X | X | X |   |   |   |   |   | X |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------

    Bueno ahora porque creo que es admisible, para empezar que significa que una heuristica sea admisible?

    La definicion de la wikipedia dice lo siguiente

    En ciencias de la computación, específicamente en algoritmos relacionados con búsqueda de caminos, se dice
    que una heurística (informática) es admisible si nunca sobreestima el costo de alcanzar el objetivo, o sea,
    que en el punto actual la estimación del costo de alcanzar el objetivo nunca es mayor que el menor costo posible.

    Lo que entendi es que si evaluo mi heuristica con mi estado meta y me regresa un costo arriba de cero por decir un numero,
    mi heuristica no es admisible, al evaluar mi estado meta en mi heuristica obtuve el valor cero por lo que creo que mi
    heuristica es admisible.

    """
    costo = 0

    for i in xrange(5, 25):
        if nodo.estado[i - 5] != 0:
            costo += 1

    return costo
    #return 0

#-------------------------------------------------------------------------------------------------
# Problema 4 (25 puntos): Desarrolla otra política admisible.
# Analiza y di porque piensas que es (o no es) dominante una respecto otra política
#-------------------------------------------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
    LA HEURÍSTICA ES ADMISIBLE

    Bueno esta heuristica funciona con la misma idea de la primera heuristica, mi problema es que aprendi a jugar
    y es muy dificil inventarme otra forma asi que aprovecho la simetria del cuadrado aplicando la misma idea, pero
    ahora en vez de renglones por columnas, igualmente creo que mi heuristica es admisible porque al evaluar mi estado
    meta en mi heuritica obtengo costo cero. aqui muestro un ejemplo de como funciona, la X significa que esta encendido.


    ---------------------   ---------------------   ---------------------   ---------------------   ---------------------
    | X |   |   |   | X |   |   |   | X |   | X |   |   |   | X |   | X |   |   |   |   |   |   |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------   ---------------------
    | X | X |   |   | X |   |   |   | X |   | X |   |   |   | X |   | X |   |   |   |   |   |   |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------   ---------------------
    | X | X |   |   | X |   |   |   | X |   | X |   |   |   |   |   | X |   |   |   |   |   | X |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------   ---------------------
    | X |   | X |   | X |   |   | X |   |   | X |   |   |   | X | X | X |   |   |   |   | X |   |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------   ---------------------
    | X |   | X | X | X |   |   |   |   | X | X |   |   |   | X | X | X |   |   |   |   | X |   |   |   |   |   |   |   |
    ---------------------   ---------------------   ---------------------   ---------------------   ---------------------

    Diagonal
    --------------------------------------------------
      Método  Costo de la solucion  Nodos explorados
    --------------------------------------------------
    A* con h1          5          43
    A* con h2          5          57

    --------------------------------------------------

    Simetria
    --------------------------------------------------
      Método  Costo de la solucion  Nodos explorados
    --------------------------------------------------
    A* con h1          6          10
    A* con h2          6          8

    --------------------------------------------------

    Problemin
    --------------------------------------------------
      Método  Costo de la solucion  Nodos explorados
    --------------------------------------------------
    A* con h1          9          2735
    A* con h2          9          3801

    --------------------------------------------------

    En cuanto al costo, es el mismo el cambio se ve reflejado en los nodos explorados en diagonal y simetria, pues no
    se aprecia mucha diferencia, en diagonal tenemos de diferencia 14 nodos que para una computadora como que no pinta
    mucho. En simetria la diferencia es dos, lo que tampoco nos dice nada, pero en problemin pues podemos ver ya una
    gran diferencia de 1066 nodos, que ya marcan una buena diferencia pienso yo, la heuristica h1 pienso que fue mejor
    por el estado inicial del problema, ya que al evaluar el primer renglon se encontraba con dos penalizaciones pero
    en h2 al evaluar la primera columna se encontraba con cinco penalizaciones entonces entre los nodos que exploro h1
    se fue mas directamente a la solucion por la ventaja de tres casillas ya apagadas pienso que la cosa depende del
    estado inicial, de como se comportara una heuristica mejor que otra.

    """
    costo = 0

    for i in xrange(1,25,5):
        if nodo.estado[i - 1] != 0:
            costo += 1

    for i in xrange(2,25,5):
        if nodo.estado[i - 1] != 0:
            costo += 1

    for i in xrange(3,25,5):
        if nodo.estado[i - 1] != 0:
            costo += 1

    for i in xrange(4,25,5):
        if nodo.estado[i - 1] != 0:
            costo += 1

    return costo
    #return 0


def prueba_clase():
    """
    Prueba la clase Lights_out

    """

    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 =  (1, 0, 0, 1, 0,
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
    #n1 = prueba_busqueda(pos_inicial, busqueda_ancho)
    #n2 = prueba_busqueda(pos_inicial, busqueda_profundidad_iterativa)
    #n3 = prueba_busqueda(pos_inicial, busqueda_costo_uniforme)
    n4 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_1)
    n5 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_2)

    print '\n\n' + '-' * 50
    print u'Método'.center(10) + 'Costo de la solucion'.center(20) + 'Nodos explorados'.center(20)
    print '-' * 50
    #print 'BFS'.center(10) + str(n1.costo).center(20) + str(n1.nodos_visitados)
    #print 'IDS'.center(10) + str(n2.costo).center(20) + str(n2.nodos_visitados)
    #print 'UCS'.center(10) + str(n3.costo).center(20) + str(n3.nodos_visitados)
    print 'A* con h1'.center(10) + str(n4.costo).center(20) + str(n4.nodos_visitados)
    print 'A* con h2'.center(10) + str(n5.costo).center(20) + str(n5.nodos_visitados)
    print ''
    print '-' * 50 + '\n\n'

if __name__ == "__main__":

    print "Antes de hacer otra cosa vamos a verificar medianamente la clase Lights_out"
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

    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(diagonal)
    compara_metodos(diagonal, h_1, h_2)

    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(simetria)
    compara_metodos(simetria, h_1, h_2)

    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(problemin)
    compara_metodos(problemin, h_1, h_2)
