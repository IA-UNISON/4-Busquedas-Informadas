#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
from random import choice
import busquedas
import math

# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class CamionMagico(busquedas.ModeloBusqueda):
    """
    ---------------------------------------------------------------------------------
     Supongamos que quiero trasladarme desde la posición discreta $1$ hasta 
     la posicion discreta $N$ en una vía recta usando un camión mágico. 
    
     Puedo trasladarme de dos maneras:
      1. A pie, desde el punto $x$ hasta el punto $x + 1$ en un tiempo de 1 minuto.
      2. Usando un camión mágico, desde el punto $x$ hasta el punto $2x$ con un tiempo 
         de 2 minutos.

     Desarrollar la clase del modelo del camión mágico
    ----------------------------------------------------------------------------------
    Los estados son una tupla con un número que representa la posición. 
    Las acciones legales son ['P', 'C'], 'P' es caminar a pie y 'C' es usar el camión.
    ----------------------------------------------------------------------------------
    """
    def acciones_legales(self, estado):
        return ['P','C']

    def sucesor(self, estado, accion):
        return (estado[0] + (1 if accion == 'P' else estado[0]),)

    def costo_local(self, estado, accion):
        return (1 if accion == 'P' else 2)

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        print("Posicion: " + str(estado[0]))
 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, N):
        def es_meta(estado):
            self.num_nodos += 1
            return (estado[0] == N)

        self.es_meta = es_meta
        self.x0 = (1,)
        self.modelo = CamionMagico()
        self.num_nodos = 0


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def heuristicas_camion_magico(N):
    def h1(nodo):
        """
        DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
        PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
        --------------------------------------------------------------
        La idea de esta heurística es que por por ejemplo si estoy en 
        la posición x y debo llegar a la posición 2x, a excepcion de 
        cuando x es 1, el costo va a ser 2 al usar el camión.

        Si estoy en 3 y quiero llegar a 12 debo duplicar dos veces, por
        eso hago math.log(N/nodo.estado[0],2), luego lo multiplico por 2 
        porque ese es el costo de tomar el camión.

        Hago la condición de que esto solo sea cuando arg >= 1 porque si no 
        salen números negativos, que sería cuando N < nodo.estado[0], 
        en ese caso ya no se debería poder llegar a la meta.

        abs(N - nodo.estado[0]) estaba pensando que era porque cuando
        estoy despues de la mitad del camino, por ejemplo estoy en 9 y 
        quiero llegar a 16 no puedo duplicar, y que cuando me pasó de N
        siga aumentando o algo así, pero esto lo devuelvo nomas cuando
        me pasé de N, así que en realidad no tengo justificación, pero
        al correrlo el número de nodos explorados con N de 1 hasta 1000
        siempre es menor que con la heurística 0, asi que voy a suponer
        que probablemente si funcione pero no lo aseguro y no entiendo
        porque.

        No tengo claro si esta heurística es admisible.
        """
        arg = N / nodo.estado[0]
        return (2*math.log(arg , 2) if arg > 1 else abs(N - nodo.estado[0]))
    # ------------------------------------------------------------
    #  Desarrolla otra política admisible.
    #  Analiza y di porque piensas que es (o no es) dominante una
    #  respecto otra política
    # ------------------------------------------------------------

    def h2(nodo):
        """
        DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
        PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
        ----------------------------------------------------------
        La idea de esta heurística es que para encontrar el camino
        mas corto de 1 hasta N es tomar el camino más corto de 1 
        hasta N/2, caminar un paso si N es impar y tomar el camión.
        
        Aunque si ya estoy después de N/2, por ejemplo si estoy en 
        9 y quiero llegar a 16, no puedo retroceder, asi que nomas
        me queda caminar.

        Si ya me pasé no puedo llegar, entonces pongo costo infinito.

        El costo que estoy calculando es el costo real, ignorando 
        cuando ya me pasé de la meta, por lo que se cumple que 
        para todo n, h2(n) <= h*(n).
        """
        
        estado = nodo.estado[0]
        
        if estado > N:
            return float('inf')

        costo = 0
        x, y = N // 2 , N

        # cada iteración agrega el coste para ir de `x a `y
        while estado <= x and x > 1:
             costo += 2 + y % 2
             y, x = x, x//2

        return costo + y - estado # agrego el costo de caminar de `estado a `y

    return (h1, h2)




# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    Los estados lo representaré como una tupla que la voy a pensar
    como una matriz de 6x8.

           +========+
           ║16 17 18║
           ║23    19║
           ║22 21 20║
   +=======+========+========+========+
   ║ 0 1 2 ║ 8  9 10║24 25 26║32 33 34║
   ║ 7   3 ║15    11║31    27║39    35║
   ║ 6 5 4 ║14 13 12║30 29 28║38 37 36║
   +=======+========+========+========+
           ║40 41 42║
           ║47    43║
           ║46 45 44║
           +========+


    Cada cara tiene un color número que indica que color va ahi, 
    por ejemplo la cara 1 tiene que tener todos las piezas de color 1.

    Las caras van a ser las siguientes:

           . = = = .
           |       |
           |   2   |
           |       |
   . = = = . = = = . = = = . = = = .
   |       |       |       |       |
   |   0   |   1   |   3   |   4   |
   |       |       |       |       |
   . = = = . = = = . = = = . = = = .
           |       |
           |   5   |
           |       |
           . = = = .

    Cada cara va a tener los índices de la siguiente manera para 
    representar las piezas:

           . = = = .
           | 0 1 2 |
           | 7   3 |
           | 6 5 4 |
           . = = = .

    El centro va a tener un color fijo.

    El estado va a ser entonces una tupla con 48 números, el
    número guardado va a representar el color que está en dicha
    posición, por ejemplo un cubo resuelto sería la siguiente tupla:
        (0,0,0,0,0,0,0,0,
         1,1,1,1,1,1,1,1,
         2,2,2,2,2,2,2,2,
         3,3,3,3,3,3,3,3,
         4,4,4,4,4,4,4,4,
         5,5,5,5,5,5,5,5)

    Las acciones son (F, B, R, U,  L, D, f, b, r, u, l, d)

    Estas letras corresponden a front, back, right, up, left y down,
    las mayúsculas significan que el movimiento se hace en sentido 
    del reloj y las minúsculas en sentido contrario.

    Esta notación es parecida a la de Singmaster pero uso
    minúsculas para indicar un movimiento invertdio en lugar 
    de poner el símbolo `.

    """
    # def __init__(self):
    #     raise NotImplementedError('Hay que hacerlo de tarea')
    def mezclar(self, estado, movimientos):
        estado = list(estado)
        acciones = self.acciones_legales(None)
        for i in range(movimientos):
            estado = self.sucesor(estado, choice(acciones))
        return tuple(estado)

    def acciones_legales(self, estado):
        return ('F', 'f', 'B', 'b', 'R', 'r', 'U', 'u', 'L', 'l', 'D', 'd')

    # con `direccion True se rota en dirección del reloj,
    # con False se rota en sentido inverso
    def rotar(self, cara, estado, direccion):
        x = cara*8
        if direccion:
            for i in range(2):
                temp = estado[x + i]
                estado[x + i] = estado[x + i + 6]
                estado[x + i + 6] = estado[x + i + 4]
                estado[x + i + 4] = estado[x + i + 2]
                estado[x + i + 2] = temp
        else:
            for i in range(2):
                temp = estado[x + i]
                estado[x + i] = estado[x + i + 2]
                estado[x + i + 2] = estado[x + i + 4]     
                estado[x + i + 4] = estado[x + i + 6]
                estado[x + i + 6] = temp

    def sucesor(self, estado, accion):
        estado = list(estado)
        if accion == 'F':
            for i in range(3):
                temp = estado[2+i]
                estado[2+i] = estado[40+i]
                estado[40+i] = estado[24+(6+i)%8]
                estado[24+(6+i)%8] = estado[20+i]
                estado[20+i] = temp
            self.rotar(1, estado, True)

        elif accion == 'f':
            for i in range(3):
                temp = estado[2+i]
                estado[2+i] = estado[20+i]
                estado[20+i] = estado[24+(6+i)%8]
                estado[24+(6+i)%8] = estado[40+i]
                estado[40+i] = temp
            self.rotar(1, estado, False)

        elif accion == 'B':
            for i in range(3):
                temp = estado[(6+i)%8]
                estado[(6+i)%8] = estado[16+i]
                estado[16+i] = estado[26+i]
                estado[26+i] = estado[44+i]
                estado[44+i] = temp
            self.rotar(4, estado, True)

        elif accion == 'b':
            for i in range(3):
                temp = estado[(6+i)%8]
                estado[(6+i)%8] = estado[44+i]
                estado[44+i] = estado[26+i]
                estado[26+i] = estado[16+i]
                estado[16+i] = temp
            self.rotar(4, estado, False)

        elif accion == 'R':
            for i in range(3):
                temp = estado[10+i]
                estado[10+i] = estado[42+i]
                estado[42+i] = estado[32+(6+i)%8]
                estado[32+(6+i)%8] = estado[18+i]
                estado[18+i] = temp
            self.rotar(3, estado, True)

        elif accion == 'r':
            for i in range(3):
                temp = estado[10+i]
                estado[10+i] = estado[18+i]
                estado[18+i] = estado[32+(6+i)%8]
                estado[32+(6+i)%8] = estado[42+i]
                estado[42+i] = temp
            self.rotar(3, estado, False)

        elif accion == 'U':
            for i in range(3):
                temp = estado[i]
                estado[i] = estado[8+i]
                estado[8+i] = estado[24+i]
                estado[24+i] = estado[32+i]
                estado[32+i] = temp
            self.rotar(2, estado, True)
        
        elif accion == 'u':
            for i in range(3):
                temp = estado[i]
                estado[i] = estado[32+i]
                estado[32+i] = estado[24+i]
                estado[24+i] = estado[8+i]
                estado[8+i] = temp
            self.rotar(2, estado, False)

        elif accion == 'L':
            for i in range(3):
                temp = estado[8+(6+i)%8]
                estado[8+(6+i)%8] = estado[16+(6+i)%8]
                estado[16+(6+i)%8] = estado[34+i]
                estado[34+i] = estado[40+(6+i)%8]
                estado[40+(6+i)%8] = temp
            self.rotar(0, estado, True)

        elif accion == 'l':
            for i in range(3):
                temp = estado[8+(6+i)%8]
                estado[8+(6+i)%8] = estado[40+(6+i)%8]
                estado[40+(6+i)%8] = estado[34+i]
                estado[34+i] = estado[16+(6+i)%8]
                estado[16+(6+i)%8] = temp
            self.rotar(0, estado, False)

        elif accion == 'D':
            for i in range(3):
                temp = estado[4+i]
                estado[4+i] = estado[36+i]
                estado[36+i] = estado[28+i]
                estado[28+i] = estado[12+i]
                estado[12+i] = temp
            self.rotar(5, estado, True)

        elif accion == 'd':
            for i in range(3):
                temp = estado[4+i]
                estado[4+i] = estado[12+i]
                estado[12+i] = estado[28+i]
                estado[28+i] = estado[36+i]
                estado[36+i] = temp
            self.rotar(5, estado, False)

        return tuple(estado)
    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        print(' '*8 + '+' + '='*7 + '+')
        
        print(' '*8 + '║', end=' ')
        for i in (16,17,18):
            print(estado[i], end=' ')
        print('║')

        print(' '*8 + '║', end=' ')
        print(str(estado[23]) + ' 2 ' + str(estado[19]) + ' ║')

        print(' '*8 + '║', end=' ')
        for i in (22,21,20):
            print(estado[i], end=' ')
        print('║')

        for i in range(4):
            print('+' + '='*7, end='')
        print('+')

        for i in (0,8,24,32):
            print('║', end=' ')
            for j in range(3):
                print(estado[i+j], end=' ')
        print('║')

        for i in (7,15,31,39):
            print('║', end=' ')
            print(estado[i], end=' ')
            print(i//8, end=' ')
            print(estado[i-4], end=' ')
        print('║')

        for i in (6,14,30,38):
            print('║', end=' ')
            for j in range(3):
                print(estado[i-j], end=' ')
        print('║')

        for i in range(4):
            print('+' + '='*7, end='')
        print('+')

        print(' '*8 + '║ ', end='')
        for i in (40,41,42):
            print(estado[i], end=' ')
        print('║')

        print(' '*8 + '║ ', end='')
        print(estado[47], end = ' ')
        print(5, end=' ')
        print(estado[43], end=' ')
        print('║')

        print(' '*8 + '║ ', end='')
        for i in (46,45,44):
            print(estado[i], end=' ')
        print('║')

        print(' '*8 + '+' + '='*7, end='+')

# ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """
    def __init__(self, x0= (0,0,0,0,0,0,0,0,
                            1,1,1,1,1,1,1,1,
                            2,2,2,2,2,2,2,2,
                            3,3,3,3,3,3,3,3,
                            4,4,4,4,4,4,4,4,
                            5,5,5,5,5,5,5,5)):


        def meta(estado):
            self.num_nodos += 1
            for i in range(6):
                cara = i*8
                for j in range(8):
                    if estado[cara + j] != i:
                        return False
            return True
        self.es_meta = meta
        self.x0 = x0
        self.modelo = CuboRubik()
        self.num_nodos = 0

    def mezclar(self, movimientos=20):
        self.x0 = self.modelo.mezclar(self.x0, movimientos)



 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0



def compara_metodos(problema, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo 
    de la solución de varios métodos de búsqueda,

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 )
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(18)
          + str(solucion2.nodos_visitados - solucion1.nodos_visitados).center(20))
    print('-' * 50 + '\n')



if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste

    # La meta a donde quiero llegar
    N = 10000
    problema = PblCamionMágico(N)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    h1_camion_magico, h2_camion_magico = heuristicas_camion_magico(N)
    # Al comparar los métodos h2 checa muchos menos nodos comparado con h1,
    # por lo que creo que h2 es dominante sobre h1
    compara_metodos(problema, h1_camion_magico, h2_camion_magico)

    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PblCuboRubik()  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    problema.mezclar(2) # número de movimientos para mezclar el cubo
    problema.modelo.bonito(problema.x0)
    print('\n')    
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    