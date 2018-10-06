#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Gilberto Espinoza'


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
        # Para evitar numeros magicos en medio de las implementaciones
        # los valores que se definan aqui son las caracteristicas del juego
        # definimo un self.estado = (0..0) ???
        self.dim = 5 # dimension del tablero
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        return range(0, len(estado)) # siempre es valido dar click a algun cuadrito
        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        # los socesores de cada accion son los estados opuestos
        # la cruz cuya casilla es accion
        # dado que el tablero es de 5 x 5 se utiliza
        nuevo_estado = list(estado)

        def switch(foco): # Apagador
            if foco == 0:
                return 1
            else:
                return 0

        # accion es la casilla que queremos cambiar
        # centro de cuadricula
        vecinos = []
        vecinos.append(0) # de ley se apaga o se prendre la casilla de accion
        # vericamos si esta en un borde, para definir la vecindad
        if accion // 5 is not 4: vecinos.append(self.dim)    #NUMERO_MAGICO
        if accion // 5 is not 0: vecinos.append(-self.dim)   #NUMERO_MAGICO
        if accion % 5 is not 4: vecinos.append(+1)    #NUMERO_MAGICO
        if accion % 5 is not 0: vecinos.append(-1)    #NUMERO_MAGICO

        #if accion is 15:
        #    print(vecinos)
        #    print(self.bonito(estado))

        for i in range(0, len(vecinos)):
            # cambios los vecinos afectados
            nuevo_estado[accion + vecinos[i]] = switch(nuevo_estado[accion + vecinos[i]]) # 0 o 1

        #if accion is 15:
            #print(self.bonito(tuple(nuevo_estado)))

        return tuple(nuevo_estado)

        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        return 1 # asignamos un costo uniforme para ir empezando
        raise NotImplementedError('Hay que hacerlo de tarea')

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
            if 1 not in x:
                print(x)
            return 1 not in x # si hay un solo 1 sigue sin ser meta
            raise NotImplementedError("Hay que hacer de tarea")

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    La heuristica no es admisible pues si tuvieramos una cruz aislada,
    la heuristica regresa 5, pero el costo real a la solucion es 1
    Aun asi esta heuristica encuentra solucion
    """
    return sum(nodo.estado)
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

    CRUZ AISLADA
    Estas cruces solo pueden aparecer en las casillas del centro de la cuadricula,
    no en bordes ni esquinas, debe ser una cruz completa.
    En la casilla 6, apreciamos una cruz aislada, notese que las casillas
    vecinas alrededor estan apagadas, especificamente, para ser aislada debe
    tener apagadas [-2*dim, -2, 2, 2*dim] segun correponda.
    Cada que veamos una de estas nuestra heuristica sumara 1
    Esta heuristca regresa maximo 2, es decir, existen cruces aisladas en [6,18] o [8, 16],
    por lo cual nunca sobreestima, pues si solo estan encendidas estas cruces, bastan
    dos movimientos (los centros de las cruces) para apagar todas estas.

    ---------------------
    |   | X |   |   |   |
    ---------------------
    | X | X | X |   | X |
    ---------------------
    |   | X |   | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------
    """
    def cruz_aislada(nodo):
        """
            estado: tupla con el estado de la cuadricula
            accion: casilla a verificar si es una cruz aisladas
        """

        # centro de la cuadricula 5x5
        if nodo.accion not in [6,7,8, 11,12,13, 16,17,18]: #NUMERO_MAGICO
            return 0 # False # si no es una de estas no puede ser cruz aislada

        # verificamos que la cruz exista
        dim = 5 #NUMERO_MAGICO
        vecinos = [-dim, -1, 0, 1, dim] # vecinos que hacen la cruz

        for i in range(0,len(vecinos)):
            if nodo.estado[nodo.accion + vecinos[i]] == 0: #Si algun vecino es 0, no hay cruz
                return 0 #False


        # agregamos los vecinos para verificar si esta aislada
        vecinos = []
        #revisamos de que extremo del cuatro central estan, agregamos vecino
        if nodo.accion // 5 is not 3: vecinos.append(2*dim)    #NUMERO_MAGICO
        if nodo.accion // 5 is not 1: vecinos.append(-2*dim)   #NUMERO_MAGICO
        if nodo.accion % 5 is not 3: vecinos.append(+2)           #NUMERO_MAGICO
        if nodo.accion % 5 is not 1: vecinos.append(-2)           #NUMERO_MAGICO

        for i in range(0,len(vecinos)):
            if nodo.estado[nodo.accion + vecinos[i]] == 1: #Si algun 2-vecino es 1, no esta aislada
                return 0 #False

        return 1 # True # Existe una cruz aislada

    h_2 = 0

    h_2 += cruz_aislada(nodo)

    return h_2

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
