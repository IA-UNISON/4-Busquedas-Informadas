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
    def __init__(self):
        #es una lista de 24, inicializados en 0; costo 0
        self.x = tuple([0 for x in range(25)])
        self.costo = 0

    def acciones_legales(self, estado):
        return range(25)

    def sucesor(self, estado, accion):

        estado = list(estado)
        #Si puedo apagar/prender el de arriba
        if accion in range(5,25):
            estado[accion-5] = 1 - estado[accion-5]
        #si puedo apagar/prender el de abajo
        if accion in range(20):
            estado[accion+5] = 1-estado[accion+5]
        #si puedo apagar/prender el de izq
        if accion not in [0,5,10,15,20]: #5*x in range(5)
            estado[accion-1] = 1-estado[accion-1]
        if accion not in [4,9,14,19,24]:
            estado[accion+1] = 1-estado[accion+1]
        estado[accion] = 1 - estado[accion]
        return tuple(estado)


    def costo_local(self, estado, accion):
        # una accion tiene un costo local 1 + n donde n es el numero de focos
        # que apago (n va desde 0 hasta 5)
        costo_local = 0
        if accion in range(5,25) and estado[accion-5] == 1:
            costo_local+=1
        #si puedo apagar/prender el de abajo
        if accion in range(20) and estado[accion+5] == 1:
            costo_local+=1
        #si puedo apagar/prender el de izq
        if accion not in [0,5,10,15,20] and estado[accion-1] == 1:
            costo_local+=1
        if accion not in [4,9,14,19,24] and estado[accion+1] ==1:
            costo_local+=1

        return (costo_local + 1 if estado[accion] == 1 else
                costo_local)


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
            return all(encendido == 1 for encendido in x)

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def adyacentes(i,lista):
    return []
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    """
    La heuristica "ignorante":
    De los no-creadores de "distancias de Manhattan en un laberinto" llega
    "mira como ignoro las demas casillas, papá". La idea de la heuristica es
    muy simple: buscar el minimo de veces que hay que aplastar para encender
    todas las luces, ignorando aquellas que se vayan a prender.

    Sin embargo es una heuristica complicada, pues implica resolver otro
    problema, que es encontrar el minimo numero de cruces que hay que meter
    para dar con un tablero lleno, el cual es un problema de optimizacion.

    Vamos a resolverlo de esta manera:

    Por cada luz del tablero no-prendida:
        si luz tiene vecinos no-prendidos:
            cuantos enciendo?
            guardar el numero de encendidos
            para vecinos en luz.vecinos:
                cuantos enciendo?
                guardar arreglo de vecinos
            encender los adyacentes al vecino que mas enciende (puede ser
            incluso este.)
            sumar 1 al contador de la heuristica (recordemos que
            la heuristica es el numero de veces que enciendo estas madres)
        si no tiene vecinos, la enciendo
        sumar 1 al contador
    es una manera muy pobre de resolverlo, pero tampoco voy a
    matar moscas a cañonazos. Lo ideal seria usar algo de optimizacion
    para encontrar la heuristica, pero si no son cañonazos son balazos.
    """
    cont = 0
    lista = list(nodo.estado)
    marcas_vecinas = [0 for x in range(4)]
    marcas = [0 for x in range(25)]
    for i in range(len(lista)):
        if lista[i] == 0
            marcas[i] = sum(1 for x in adyacentes(i,lista) if x == 0)
            if marcas[i] == 0:
                lista[i] = 1
                cont+=1
                continue
            for j,a in enumerate(adyacentes(i,lista)):
                marcas_vecinas[j] = adyacentes(a,lista)
                arreglo = marcas_vecinas[:]
                arreglo = sort(arreglo)
                temp = arreglo[-1]
            if marcas[i] >= marcas_vecinas[-1]:
                marcar_adyacentes(i, lista)
            else:
                cont+=marcar_adyacentes()

    return 0


# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE


    Segunda heuristica: fichas consecutivas rodeadas de exito.

    ¿Alguna vez te has sentido excluido por el exito de los que estan a tu
    alrededor? Quizá este sea tu heuristica.

    esta heuristica trata de encontrar una cadena de espacios apagados
    es decir, que yo pueda llegar de uno apagado hacia otro apagado
    agarrando el maximo numero de espacios apagados. Por cada patron de
    no-éxito, sumo 1 a mi heuristica.
    """

    for x in nodo.estado:



    return 0


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

    print("Antes de hacer otra cosa,")
    print("vamos a verificar medianamente la clase LightsOut")
    prueba_modelo()

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
    print("\n".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2)

    print("\n\nPara el problema Bonito")
    print("\n".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2)
