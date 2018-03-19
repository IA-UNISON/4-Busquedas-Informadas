#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'nombre del estudiante'


import busquedas
import math

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
        self.acciones = range(25)

    def acciones_legales(self, estado):
        '''
        Realmente no hay restricciones en cuanto a las acciones
        '''
        return self.acciones

    def sucesor(self, estado, accion):
        '''
        Es facil ver que el problema puede ser tratado como una suma de matrices
        sobre el campo de Galois. o F2
        Fuente: http://codingthematrix.com/ de Philip N. Klein
        '''
        
        estado_nuevo=list(estado)
        
        r = accion % 5
        c = accion // 5
        
        
        estado_nuevo[accion]=1-estado_nuevo[accion]  
        if r < 4:
            estado_nuevo[accion+1]=1-estado_nuevo[accion+1]
        if r > 0:
            estado_nuevo[accion-1]=1-estado_nuevo[accion-1]
        if c >0:
            estado_nuevo[accion-5]=1-estado_nuevo[accion-5]
        if c < 4:
            estado_nuevo[accion+5]=1-estado_nuevo[accion+5]
        
        return tuple(estado_nuevo)

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
            """
            Todas apagadas
            """
            for luz in x:
                if luz == 1:
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
    
    Imitando al 8-puzzle, esta heuristica calcula la cantidad de luces que 
    necesitan apagar.
    
    En cuanto a admisibilidad es facil confundirse y decir que si lo es puesto 
    que la comparacion que hacemos con el 8-puzzle, pero en este caso no medimos
    distancia, y un movimiento afecta a varias luces, asi una heuristica admisible 
    tendia en consideracion la cantidad de luces que se deben presionar para llegar
    al estado meta, como se ve en la sig imagen
    
    https://goo.gl/yoXth7

    """
    return sum(luz for luz in nodo.estado)


# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    Cuando armamos un cubo de rubick, generalmente la clave o primer paso
    es acomodar la cara blanca, de manera analoga en el ligths out se apagan 
    las luces de todas las filas con exepcion de la ultima
    es decir
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,X,X,X,X,X)
    
    Es facil ver que es una variante de la heuristica 1, por lo que esta es dominada
    por ella.
    Despues de las pruebas podermos observar que el costo es el mismo pero la 
    cantidad de nodos visitados en mayor cuando de usa h_2
    
    En esta funcion podemos usar el mismo argumeto usada en la funcion h_1,
    estas son una observacion del estado/tablero actual mas que un indicador 
    de los pasos a seguir
    
    """
        
    return sum(nodo.estado[i] for i in range(20))

##EXTRA
    """
    PREMISA: Tratemos de encontrar una heuristica admisible mejor a la propuesta
    clasica de lugares erroneos.
    
    CONCLUSION: La no admisible provoca que se visiten menos nodos, aunque no 
    asegura encontrar una solucion optima, parece tener un desempeño mejor.
    """
def h_3(nodo):
    """
    Esta es la buena de belen.
    Cantidad de pasos optimista
    """
    return sum(luz for luz in nodo.estado)//5    

def h_4(nodo):
    '''
    Esta es la chila de ivan
    Cantidad de pasos optimista con distibucion de peso.
    '''
    return math.exp(sum(casilla for casilla in nodo.estado) / 5)

def h_5(nodo):
    """
    La chila de belen.
    Grupos de 5 en el tablero.
    """    
    vecindad ={}

    for i in range(25):
        flag = False
        if nodo.estado[i] == 1:
            for x in vecindad.keys():
                if len(vecindad[x])<5:
                    for xi in vecindad[x]:
                        if abs(xi-i)==5 or (xi%5==0 and i-xi==1) or (xi%5==4 and xi-i==1) or abs(xi-i)==1:
                            flag=True
                            vecindad[x].append(i)
                            break
                    if flag==True:
                        break
                
            if flag == False:
                vecindad[i] = [i]
    
    return len(vecindad)

def h_6(nodo):
    """   
    chila de la patty
    
    Busca en esquinas y sus cruces
    """ 
    #---------------------------------------------------------------------------------------------------
    costo = 0

    #CHECO MI ESQUINA INFERIOR IZQUIERDAY MI CRUZ 
    if nodo.estado[20] != 0 or nodo.estado[15] != 0 or nodo.estado[21] == 0:
      costo +=1 
    
    #se suman todas las casillas encencidas en la cruz
    aux1 = (nodo.estado[3] + nodo.estado[7] + nodo.estado[8] + nodo.estado[9] + nodo.estado[13])
    #se checa si solo se necesitaria un movimiento para resolver el numero de casillas encendidas
    #como es el caso en que todas esten encendidas(aux1=5) o que solo esten prendidas 1 o 2
    if aux1 == 1 or aux1 == 2 or aux1 == 5:
      costo+=1
    #se checa si se necesitarian hacer mas de un movimiento para resolver el numero de casillas encendias
    #como es el caso en que tres o cuatro casillas esten encendidas
    if aux1 == 3 or aux1 == 4: 
      costo+=2
   
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
    '''  
    solucion1= busquedas.busqueda_A_estrella(ProblemaLightsOut(diagonal),h_2)
    solucion2= busquedas.busqueda_A_estrella(ProblemaLightsOut(simetria),h_2)
    solucion3= busquedas.busqueda_A_estrella(ProblemaLightsOut(problemin),h_2)

    
    print("1: ",solucion1)
    print("2: ",solucion2)
    print("3: ",solucion3)
    '''
    print("\n\nPara el problema en diagonal")
    print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_6)

    print("\n\nPara el problema simétrico")
    print("\n".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_6)

    print("\n\nPara el problema Bonito")
    print("\n".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_6)
