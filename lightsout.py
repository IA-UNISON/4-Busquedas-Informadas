#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Raul Perez'

import busquedas
from time import time

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
        """
        Se crean las acciones posibles
        """
        self.acciones = range(25)

    def acciones_legales(self, estado):
        """
        Devuelve todas las acciones una tupla del 0 - 24
        """
        return self.acciones

    def sucesor(self, estado, accion):
        """
        Cambia el estado de las luces
        """
        s = list(estado)
        # obtenemos la fila y la columna donde fue presionado
        fila = accion//5
        columna = accion%5 
        # cambia la luz donde se pulso
        s[accion] = 0 if s[accion] is 1 else 1
        # cambio las luces adyacentes si se puede
        # luz de arriba
        if fila is not 0:
            s[accion-5] = 0 if s[accion-5] is 1 else 1
        # luz de abajo
        if fila is not 4:
            s[accion+5] = 0 if s[accion+5] is 1 else 1
        # luz de la izquierda
        if columna is not 0:
            s[accion-1] = 0 if s[accion-1] is 1 else 1
        # luz de la derecha
        if columna is not 4:
            s[accion+1] = 0 if s[accion+1] is 1 else 1

        return tuple(s)

    def costo_local(self, estado, accion):
        """
        Para cada accion el costo es 1
        """
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
            """
            Revisa la todas las luces del tablero
            si todas las luces estan apagadas, entonces 
            el estado es meta
            """
            return True if sum((p for p in x)) is 0 else False

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    La maxima cantidad de luces que se pueden apagar al pulsar es 
    de 5, por lo tanto, la sumatoria de todas las luces prendidas
    dividido entre 5, seria la minima cantidad de pasos para apagar 
    las luces. Por lo tanto seria admisible.
    """
    s = nodo.estado
    prendidos = sum((p for p in s))
    return (prendidos//5 + 1)
    

# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    La idea consisten en sumarle 'pasos' a la heuristica cuando se 
    encuentre a una luz prendida, en caso de encontrarse con una luz
    centro (al pulsar tal luz se apagen todas la adyacentes), enconces se
    restan las dos sumados por esas luces y se suma un paso.
    Realmente no estoy seguro si es admisible o no, pero da muy buenos resultados.
    El mejor valor de 'pasos' fue 2

    Esta Heuristica es dominantes sobre la primera por mucho, ya que la primera solo
    da el minimo posible, en cambio la segunda da un costo mucho mas cercano al real
    """
    s = nodo.estado
    # Se pudiera cambiar, son los pasos de una luz que no esta en el centro
    pasos = 2 
    prendidos = []
    heuristica = 0
    # guardo las posiciones donde esta prendido
    for posicion in range(len(s)):
        if s[posicion] is 1:
            prendidos.append(posicion)
            heuristica += pasos
    # verifico si hay luces que son centros
    checados = [] # si la luz es centro se guardan las luces vecinas
    for pos_prendido in prendidos:
        fila, columna = pos_prendido//5, pos_prendido%5 
        contador = 0
        # checa las luces vecinas
        if ((fila is not 0) and (pos_prendido-5 in prendidos) and 
            (pos_prendido-5 not in checados)):
                contador += 1
        if ((fila is not 4) and (pos_prendido+5 in prendidos) and 
            (pos_prendido+5 not in checados)):
                contador += 1
        if ((columna is not 0) and (pos_prendido-1 in prendidos) and 
            (pos_prendido-1 not in checados)):
                contador += 1
        if ((columna is not 4) and (pos_prendido+1 in prendidos) and 
            (pos_prendido+1 not in checados)):
                contador += 1
        # dependiendo de la fila y la columna checa
        # si al pulsar puede apagar todas las luces
        # caso 1: en la esquina
        if ( (fila in [0,4] and columna in [0,4])) and (contador is 2):
            heuristica += (1-pasos*(contador+1)) # quita las sumas anteriores y le suma 1 paso
            # dependiendo de la esquina guardo los checados
            checados.append(pos_prendido)
            if pos_prendido is 0:
                checados.append(1)
                checados.append(5)
            elif pos_prendido is 4:
                checados.append(3)
                checados.append(9)
            elif pos_prendido is 20:
                checados.append(15)
                checados.append(21)
            else:
                checados.append(19)
                checados.append(23)
        # caso 2: en los bordes de izquierda y derecha
        elif (columna in [0,4] and fila in [1,2,3]) and contador is 3: 
            heuristica += (1-pasos*(contador+1)) # quita las sumas anteriores y le suma 1 paso
            checados.append(pos_prendido)
            checados.append(pos_prendido+1)
            checados.append(pos_prendido+5)
            checados.append(pos_prendido-5)
        # caso 3: en los bordes de arriba y abajo
        elif (fila in [0,4] and columna in [1,2,3]) and contador is 3: 
            heuristica += (1-pasos*(contador+1)) # quita las sumas anteriores y le suma 1 paso
            checados.append(pos_prendido)
            checados.append(pos_prendido-1)
            checados.append(pos_prendido+5)
            checados.append(pos_prendido-5)
        # caso 4: en el centro
        elif (fila in [1,2,3] and columna in [1,2,3]) and contador is 4:
            heuristica += (1-pasos*(contador+1)) # quita las sumas anteriores y le suma 1 paso
            checados.append(pos_prendido)
            checados.append(pos_prendido+1)
            checados.append(pos_prendido-1)
            checados.append(pos_prendido+5)
            checados.append(pos_prendido-5)
        
    return heuristica

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
    t_inicial_h1 = time()
    solucion1 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_1)
    t_final_h1 = time()
    t_inicial_h2 = time()
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_2)
    t_final_h2 = time()
    print('-' * 80)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados'.center(20) + 'Tiempo'.center(20))
    print('-' * 80 + '\n')
    print('A* con h1'.center(10) + str(solucion1.costo).center(20) +
          str(solucion1.nodos_visitados).center(20) + str(t_final_h1-t_inicial_h1).center(20))
    print('A* con h2'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados).center(20) + str(t_final_h2-t_inicial_h2).center(20))
    print('-' * 80 + '\n')


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
    

"""
Resultados

Para el problema en diagonal

--------------------------------------------------------------------------------
  Método         Costo          Nodos visitados          Tiempo
--------------------------------------------------------------------------------

A* con h1          5                  5262               3.83 seg
A* con h2          5                   24                0.05 seg
--------------------------------------------------------------------------------

Para el problema simétrico

--------------------------------------------------------------------------------
  Método         Costo          Nodos visitados          Tiempo
--------------------------------------------------------------------------------

A* con h1          6                 16859              12.93 seg
A* con h2          6                   18               0.05  seg
--------------------------------------------------------------------------------

Para el problema Bonito


--------------------------------------------------------------------------------
  Método         Costo          Nodos visitados          Tiempo
--------------------------------------------------------------------------------

A* con h1          9                 728052             561.24 seg ~ 9.34 min 
A* con h2          9                  542               1.38   seg
--------------------------------------------------------------------------------

"""