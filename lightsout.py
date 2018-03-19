#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Cesar Salazar'


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
        self.acciones=range(25)

    def acciones_legales(self, estado):
        #las 25 casillas que pueden ser presionadas
        return self.acciones

    def sucesor(self, estado, accion):
        sucesor = list(estado)
        fila=accion//5
        columna=accion%5
        sucesor[accion]=1-estado[accion]
        if(fila<4):
            sucesor[accion+5]=1-estado[accion+5]
        if(fila>0):
            sucesor[accion-5]=1-estado[accion-5]
        if(columna<4):
            sucesor[accion+1]=1-estado[accion+1]
        if(columna>0):
            sucesor[accion-1]=1-estado[accion-1]
        return tuple(sucesor)

    def costo_local(self, estado, accion):
        #1 por cada accion
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
            for casilla in x:
                if casilla == 1: 
                    return False 
            return True

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    -Como cada movimiento se apaga maximo cinco casillas, tome como heuristica la cantidad 
     de casillas todavía encendidas después de cada movimiento, dividido por 5.
    -Le sume 4 por si las luces encendidas es menos de 5, entonces sumandole 4 tomara el valor como 1
    -Si todas las luces estuvieran agrupadas de 5 en 5 en forma de cruz entonces el número total 
     de luces dividido entre 5 seria el mínimo de pasos
    -h(G) = 0 donde G es la solución
    """
    a = nodo.estado
    return (sum(a)+4)//5

# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    -Cuando estaba entendiendo el juego lo que hacia es ir dejando apagadas las casillas
     de arriba hacia abajo, al llegar a abajo, no sabia como apagar la linea de abajo, luego lo 
     que hacia era encender una al azar y volver a repetir apagando de arriba hacia abajo hasta que diera
     resultado.
    -Tome esto como ejemplo y decidi uponer esto como heuristica, si una casilla tenia la casilla de arriba
     encendida, aumento en 1 el costo.
    -Creo que no seria admisible porque una cruz en el centro, con esta heuristica seria 5, pero en un
     movimiento estaria solucionado, pero el resultado fue muy bueno
    -h(G) = 0 donde G es la solución

    Creo que h2 es dominante a h1 porque h1 puede ser maximo 5 y h2 puede ser hasta 20, 
    esto a mi parecer ocasiona que con h2 de mejores resultados para casos no tan sencillos, 
    porque esta mas cerca en esos casos del costo real

    """
    a = nodo.estado
    costo = 0
    #for i in range(0,5):
    #    costo+=1 if a[i+20]!=0 else 0
    for i in range(5,25):
        costo+=1 if a[i-5]!=0 else 0
    return costo


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
    t_inicial = time()
    solucion1 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_1)
    t_final = time()
    t_inicial2 = time()
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_2)
    t_final2 = time()

    print('-' * 70)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados' + 'Tiempo'.center(20))
    print('-' * 70 + '\n\n')
    print('A* con h1'.center(10) + str(solucion1.costo).center(20) +
          str(solucion1.nodos_visitados).center(20)+ str(t_final-t_inicial).center(20))
    print('A* con h2'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados).center(20)+ str(t_final2-t_inicial2).center(20))
    print('-' * 70 + '\n\n')


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
    #print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_2)

    print("\n\nPara el problema simétrico")
    #print("{}\n".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2)

    print("\n\nPara el problema Bonito")
    #print("{}\n".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2)


    """
    *al corregir el A* mejoraron los tiempos
    Para el problema en diagonal
    ----------------------------------------------------------------------
    Método         Costo        Nodos visitados       Tiempo
    ----------------------------------------------------------------------


    A* con h1          5                  1535         0.7568445205688477
    A* con h2          5                   47         0.02659440040588379
    ----------------------------------------------------------------------




    Para el problema simétrico
    ----------------------------------------------------------------------
    Método         Costo        Nodos visitados       Tiempo
    ----------------------------------------------------------------------


    A* con h1          6                  4162         1.9519867897033691
    A* con h2          6                   11         0.0057392120361328125
    ----------------------------------------------------------------------




    Para el problema Bonito
    ----------------------------------------------------------------------
    Método         Costo        Nodos visitados       Tiempo
    ----------------------------------------------------------------------


    A* con h1          9                 328870        139.14729261398315
    A* con h2          9                  3126         1.6946332454681396
    ----------------------------------------------------------------------
    """