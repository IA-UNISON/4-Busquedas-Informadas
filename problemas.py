#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
import math



# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):
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
    
    """
    def __init__(self, N):
        if not isinstance(N, int):
            raise TypeError("N debe ser entero")
        if N < 1:
            raise ValueError("N debe ser >= 1")
        
        self.N = N
        self.s_0 = 1
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones(self, estado):
        acciones = []

        if estado + 1 <= self.N:
            acciones.append("caminar")
        
        if estado * 2 <= self.N:
            acciones.append("camión")
        
        return acciones
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        if accion == "caminar":
            return estado + 1, 1

        elif accion == "camión":
            return estado * 2, 2
        
        else: 
            raise ValueError("Acción inválida")
        #raise NotImplementedError('Hay que hacerlo de tarea')

    def terminal(self, estado):
        return estado == self.N
        #raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posición {estado}"
        #raise NotImplementedError('Hay que hacerlo de tarea')
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    Dado que no debemos sobreestimar el costo mínimo real restante y
    nuestra heurística debe ser 0 <= h(N) <= h*(N) para toda N
    Para cualquier estado N, el costo restante h*(N) >= 0 dado que 
    los costos de las acciones son positivos
    Esta heuristica en escencia no ayuda ya que solo vuelve 
    f(n) = g(n) + h(n)
    en 
    f(n) = g(n)
    lo cual se convierte en dijkstra, porque no establece
    una guia hacia el objetivo, pero no miente por exceso, por lo que
    nunca sobreestima

    """
    return 0
    


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Simplifiquemos el problema como si solo pudieramos duplicar la posición
    x en la que estamos
    x = estado actual
    N = meta
    x <= N
    Si solamente duplicaramos el estado actual podriamos aproximar sin pasarnos
    a la meta con esta fórmula: 2^k * x <= N
    donde k es el número de veces que duplicamos sin pasarnos
    entonces, para saber cuantas veces podemos duplicar despejamos a k
    2^k <= N/x => log2(2^k) <= log2(N/x) => k <= log2(N/x)
    Despues el valor de log2(N/x) lo redondeamos hacia abajo para no sobreestimar
    utilizamos el maximo entre 0 y lo que devuelva math.floor....., para asegurar
    que la heuristica no sea negativa

    """
    x = nodo.estado
    N = problema.N
    
    return 2 * max(0, math.floor(math.log2(N / x)))

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube

    Modelo de búsqueda para el cubo Runik

    https://www.iberorubik.com/tutoriales/3x3x3/nomenclatura/

    para lo cual se utiliza la siguiente nomenclatura para las caras:
    A: Cara superior    (0-8)
    F: Cara frontal     (9-17)
    D: Cara derecha     (18-26)
    T: Cara trasera     (27-35)
    I: Cara izquierda   (36-44)
    B: Cara inferior    (45-53)
    
    """
    def __init__(self, estado_inicial):
        # Cubo 3x3x3
        if len(estado_inicial) != 54:
            raise ValueError("El estado debe tener 54 elementos")
        
        self.estado_inicial = tuple(estado_inicial)

        #raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones(self, estado):
        """
        Tenemos los movimientos A y A' ya que se pueden realizar en sentido 
        horario y antihorario, derecha e izquierda para la misma cara

        """
        return [
            "A","A'",
            "F","F'",
            "D","D'",
            "T","T'",
            "I","I'",
            "B","B'"
        ]

        #raise NotImplementedError('Hay que hacerlo de tarea')

    """
    Rotaciones
    """
    def rotar_cara(self, e, i):
        e[i+0], e[i+1], e[i+2], e[i+5], e[i+8], e[i+7], e[i+6], e[i+3] = \
        e[i+6], e[i+3], e[i+0], e[i+1], e[i+2], e[i+5], e[i+8], e[i+7]

    def rotar_A(self, e):

        self.rotar_cara(e, 0)

        f = e[9:12]
        d = e[18:21]
        t = e[27:30]
        i = e[36:39]

        e[9:12] = i
        e[18:21] = f
        e[27:30] = d
        e[36:39] = t

    def rotar_B(self, e):

        self.rotar_cara(e, 45)

        f = e[15:18]
        d = e[24:27]
        t = e[33:36]
        i = e[42:45]

        e[15:18] = d
        e[24:27] = t
        e[33:36] = i
        e[42:45] = f

    def rotar_F(self, e):

        self.rotar_cara(e, 9)

        a = [e[6], e[7], e[8]]
        d = [e[18], e[21], e[24]]
        b = [e[45], e[46], e[47]]
        i = [e[38], e[41], e[44]]

        e[6], e[7], e[8] = i[::-1]
        e[18], e[21], e[24] = a
        e[45], e[46], e[47] = d[::-1]
        e[38], e[41], e[44] = b

    def rotar_T(self, e):

        self.rotar_cara(e, 27)

        a = [e[0], e[1], e[2]]
        d = [e[20], e[23], e[26]]
        b = [e[51], e[52], e[53]]
        i = [e[36], e[39], e[42]]

        e[0], e[1], e[2] = d
        e[20], e[23], e[26] = b[::-1]
        e[51], e[52], e[53] = i
        e[36], e[39], e[42] = a[::-1]

    def rotar_D(self, e):

        self.rotar_cara(e, 18)

        a = [e[2], e[5], e[8]]
        f = [e[11], e[14], e[17]]
        b = [e[47], e[50], e[53]]
        t = [e[27], e[30], e[33]]

        e[2], e[5], e[8] = f
        e[11], e[14], e[17] = b
        e[47], e[50], e[53] = t[::-1]
        e[27], e[30], e[33] = a[::-1]

    def rotar_I(self, e):

        self.rotar_cara(e, 36)

        a = [e[0], e[3], e[6]]
        f = [e[9], e[12], e[15]]
        b = [e[45], e[48], e[51]]
        t = [e[29], e[32], e[35]]

        e[0], e[3], e[6] = t[::-1]
        e[9], e[12], e[15] = a
        e[45], e[48], e[51] = f
        e[29], e[32], e[35] = b[::-1]

    

    def sucesor(self, estado, accion):
        """
        Aplicamos la rotación y devolvemos el nuevo estado, para no duplicar el
        número de funciones, para la inversa aplicamos el mismo movimiento 3 veces

        """
        estado = list(estado)

        if accion == "A":
            self.rotar_A(estado)
        
        elif accion == "A'":
            for _ in range(3):
                self.rotar_A(estado)
        
        elif accion == "F":
            self.rotar_F(estado)
        
        elif accion == "F'":
            for _ in range(3):
                self.rotar_F(estado)
        
        elif accion == "D":
            self.rotar_D(estado)
        
        elif accion == "D'":
            for _ in range(3):
                self.rotar_D(estado)
        
        elif accion == "T":
            self.rotar_T(estado)
        
        elif accion == "T'":
            for _ in range(3):
                self.rotar_T(estado)

        elif accion == "I":
            self.rotar_I(estado)
        
        elif accion == "I'":
            for _ in range(3):
                self.rotar_I(estado)

        elif accion == "B":
            self.rotar_B(estado)
        
        elif accion == "B'":
            for _ in range(3):
                self.rotar_B(estado)
        
        else:
            raise ValueError("Acción inválida")
        
        return tuple(estado), 1


        #raise NotImplementedError('Hay que hacerlo de tarea')

    def terminal(self, estado):
        for i in range(0, 54, 9):
            cara = estado[i:i+9]
            if len(set(cara)) != 1:
                return False
        return True

        #raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        def cara(i):
            return estado[i:i+9]

        A = cara(0)
        F = cara(9)
        D = cara(18)
        T = cara(27)
        I = cara(36)
        B = cara(45)

        print("      {} {} {}".format(*A[0:3]))
        print("      {} {} {}".format(*A[3:6]))
        print("      {} {} {}".format(*A[6:9]))
        print()

        for i in range(3):
            print(
                "{} {} {}   {} {} {}   {} {} {}   {} {} {}".format(
                    *I[i*3:(i+1)*3],
                    *F[i*3:(i+1)*3],
                    *D[i*3:(i+1)*3],
                    *T[i*3:(i+1)*3]
                )
            )

        print()

        print("      {} {} {}".format(*B[0:3]))
        print("      {} {} {}".format(*B[3:6]))
        print("      {} {} {}".format(*B[6:9]))

        #raise NotImplementedError('Hay que hacerlo de tarea')
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    De manera muy simplista, la heurística es admisible al simplemente 
    ser el algoritmo de busqueda A*, y siempre la heuristica es
    h(x) = 0 <= h*(x) 
    siempre la heurística sera menor o igual que la solución optima

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

    Si el cubo esta resuelto la heuristica es 0, si el cubo no esta resuelto al menos
    un movimiento es necesario para resolverlo, lo cual no sobreestima
    """

    estado = nodo.estado

    for cara in range(6):

        estado = nodo.estado

    for cara in range(6):
        inicio = cara * 9
        color = estado[inicio]

        for i in range(inicio, inicio + 9):
            if estado[i] != color:
                return 1

        """inicio = cara * 9
        color = estado[inicio]

        for i in range(inicio, inicio + 9):
            if estado[i] != color:
                return 1"""

    return 0
"""
La heurística h_1 = 0 es adimsible porque nunca sobreestima el costo real.
Sin embargo, no aporta información sobre la distancia al objetivo, por lo que
A* se comporta como búsqueda de costo uniforme.
La heurística h_2 devuelve 0 si el cubo esta resuelto y 1 en caso contrario.
Esta heurística es admisible porque cualquier estado no resuelto requiere
al menos un movimiento para alcanzar el objetivo, por lo que
h_2 = 1 <= h*
h_2 domina a h_1 ya que para todo estado n, h_2 >= h_1 y existen estados
donde h_2 > h_1. Por lo tanto, h_2 es una heurística más informativa y
permite que A* explore menos nodos
"""


def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):

    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(nodos1))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(nodos2))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(100)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    

    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    pos_inicial = (
        0,0,0,0,0,0,0,0,0,
        4,4,4,1,1,1,1,1,1,
        1,1,1,2,2,2,2,2,2,
        2,2,2,3,3,3,3,3,3,
        3,3,3,4,4,4,4,4,4,
        5,5,5,5,5,5,5,5,5
    )  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    """
    No se limitan bien los estados fisicamente inmposibles, lo cual causa que se quede
    colgado con mas movimientos
    """

    """0,0,0,0,0,0,4,4,4,
        1,1,1,1,1,1,2,2,2,
        2,2,2,2,2,2,3,3,3,
        3,3,3,3,3,3,1,1,1,
        4,4,4,4,4,4,5,5,5,
        5,5,5,5,5,5,0,0,0
        
        0,0,0,0,0,0,4,4,4,
        1,1,1,1,1,1,0,0,0,
        2,2,2,2,2,2,1,1,1,
        3,3,3,3,3,3,2,2,2,
        4,4,4,4,4,4,5,5,5,
        5,5,5,5,5,5,3,3,3
    """

    problema = PbCuboRubik( pos_inicial )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_problema_1, h_2_problema_1)
    #compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    