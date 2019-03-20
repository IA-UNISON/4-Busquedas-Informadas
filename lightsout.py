#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Jose Pimienta'


import busquedas


class LightsOut(busquedas.ModeloBusqueda):
    # --------------------------------------------------------
    # Completa la clase
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
        #inicializamos el tablero encendido
       self.x = tuple(1 for x in range(25))

    def acciones_legales(self, estado):
        #siempre es permitido presionar cualquier casilla del tablero
        return range(25)

    def sucesor(self, estado, accion):
        lista_estado = list(estado)
        lista_estado[accion]= 0 if lista_estado[accion] == 1 else 1
        #ahora ponemos las acciones por los tres tipos de posibles
        #cambios en el tablero
        
        #Si se presiona algun boton del primer renglon
        if accion < 5: #se presiono una casilla en el primer renglon [0,1,2,3,4]
            if accion == 0: #si es la esquina superio izquirda solo afecta dos casillas
                lista_estado[accion+1] = 0 if lista_estado[accion+1] == 1 else 1
                lista_estado[accion+5] = 0 if lista_estado[accion+5] == 1 else 1
                
            elif accion == 4: #es la esquina superior derecha
                lista_estado[accion-1] = 0 if lista_estado[accion-1] == 1 else 1
                lista_estado[accion+5] = 0 if lista_estado[accion+5] == 1 else 1
                
            else: #es cualquier que no este en esquina
                lista_estado[accion+1] = 0 if lista_estado[accion+1] == 1 else 1
                lista_estado[accion-1] = 0 if lista_estado[accion-1] == 1 else 1
                lista_estado[accion+5] = 0 if lista_estado[accion+5] == 1 else 1
                
        #ahora checamos si se presiono el ultimop renglon        
        elif accion > 19:#se presiono una casilla en el primer renglon [20,21,22,23,24]
            if accion == 20: #si es la esquina inferior izquirda solo afecta dos casillas
                lista_estado[accion+1] = 0 if lista_estado[accion+1] == 1 else 1
                lista_estado[accion-5] = 0 if lista_estado[accion-5] == 1 else 1
                
            elif accion == 24: #es la esquina inferior derecha
                lista_estado[accion-1] = 0 if lista_estado[accion-1] == 1 else 1
                lista_estado[accion-5] = 0 if lista_estado[accion-5] == 1 else 1
                
            else: #es cualquier que no este en esquina
                lista_estado[accion+1] = 0 if lista_estado[accion+1] == 1 else 1
                lista_estado[accion-1] = 0 if lista_estado[accion-1] == 1 else 1
                lista_estado[accion-5] = 0 if lista_estado[accion-5] == 1 else 1
                
        #ahora checamos en caso que se presione una casilla que no este
        #ni en el primero ni en el ultimo renglon
        else:
            if accion % 5 == 0 : #esta en la columna de hasta la izquierda
                lista_estado[accion+1] = 0 if lista_estado[accion+1] == 1 else 1
                lista_estado[accion+5] = 0 if lista_estado[accion+5] == 1 else 1
                lista_estado[accion-5] = 0 if lista_estado[accion-5] == 1 else 1
                
            elif accion % 5 == 4: #esta en la columna de hasta la derecha
                lista_estado[accion-1] = 0 if lista_estado[accion-1] == 1 else 1
                lista_estado[accion+5] = 0 if lista_estado[accion+5] == 1 else 1
                lista_estado[accion-5] = 0 if lista_estado[accion-5] == 1 else 1
                
            else: #es cualquier que no este en esquina
                lista_estado[accion+1] = 0 if lista_estado[accion+1] == 1 else 1
                lista_estado[accion-1] = 0 if lista_estado[accion-1] == 1 else 1
                lista_estado[accion+5] = 0 if lista_estado[accion+5] == 1 else 1
                lista_estado[accion-5] = 0 if lista_estado[accion-5] == 1 else 1
                
        
        return tuple(lista_estado)
                
            
    def costo_local(self, estado, accion):
        #el costo por cualquier accion es igual a 1 (igual en todas)
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
#  Completa el problema de LightsOut
# ------------------------------------------------------------
class ProblemaLightsOut(busquedas.ProblemaBusqueda):
    def __init__(self, pos_ini):
        """
        Utiliza la superclase para hacer el problema

        """
        # Completa el código
        x0 = tuple(pos_ini)
        def meta(x):
            return all(casilla == 0 for casilla in x)

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    esta heuristica devuelve la cantidad de casillas encendiadas, 
    es decir que ocupan ser apagadas

    """
    return sum(1 for x in list(nodo.estado) if x == 1)


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    en esta heuristica regresamos la suma de el numero de cruces prendidas, 
    es decir sumamos si tenemos la siguiente situacion
    _______
    |_|X|_|
    |X|X|X|
    |_|X|_|
    

    """
    x = 0
    '''
    for i in range(25):
        if nodo.estado == 1:
            if i < 5: #se presiono una casilla en el primer renglon [0,1,2,3,4]
                if i == 0: #si es la esquina superio izquirda solo afecta dos casillas
                    if nodo.estado[i+1] == 1 and nodo.estado[i+5] == 1: x+=1
                    
                elif i == 4: #es la esquina superior derecha
                    if nodo.estado[i-1] == 1 and nodo.estado[i+5] == 1: x+=1
                    
                else: #es cualquier que no este en esquina
                    if (nodo.estado[i+1] == 1 and nodo.estado[i-1] == 1 
                    and nodo.estado[i+5] == 1) : x+=1
                    
            #ahora checamos si se presiono el ultimop renglon        
            elif i > 19:#se presiono una casilla en el primer renglon [20,21,22,23,24]
                if i == 20: #si es la esquina inferior izquirda solo afecta dos casillas
                    if nodo.estado[i+1] == 1 and nodo.estado[i-5] == 1: x+=1
                    
                elif i == 24: #es la esquina inferior derecha
                    if nodo.estado[i-1] == 1 and nodo.estado[i-5] == 1: x+=1
                    
                else: #es cualquier que no este en esquina
                    if (nodo.estado[i+1] == 1 and nodo.estado[i-1] == 1 
                    and nodo.estado[i-5] == 1): x+=1
                    
            #ahora checamos en caso que se presione una casilla que no este
            #ni en el primero ni en el ultimo renglon
            else:
                if i % 5 == 0 : #esta en la columna de hasta la izquierda
                    if (nodo.estado[i+1] == 1 and nodo.estado[i+5] == 1 
                    and nodo.estado[i-5] == 1): x+=1
                    
                elif i % 5 == 4: #esta en la columna de hasta la derecha
                    if (nodo.estado[i-1] == 1 and nodo.estado[i+5] == 1 
                    and nodo.estado[i-5] == 1): x+=1
                    
                else: #es cualquier que no este en esquina
                    if (nodo.estado[i+1] == 1 and nodo.estado[i-1] == 1 
                    and nodo.estado[i+5] == 1 and nodo.estado[i-5]):
                        x+=1
    '''
    return sum(1 for x in list(nodo.estado) if x == 0)
    return x


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
