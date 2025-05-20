#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas



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
    
    """
    def __init__(self, n):
        self.n = n

    def acciones_legales(self, estado):
        acciones = []

        if estado < self.n:
            acciones.append("caminar")
        
        if estado * 2 <= self.n:
            acciones.append("camion")

        return acciones

    def sucesor(self, estado, accion):
        if accion == "caminar":
            return estado + 1
        elif accion == "camion":
            return estado * 2

    def costo_local(self, estado, accion):
        if accion == "caminar":
            return 1
        elif accion == "camion":
            return 2

    @staticmethod
    def bonito(self, estado):
        """
        El prettyprint de un estado dado

        """
        linea = ["-"] * self.n

        if 1<= estado <= self.n:
            linea[estado - 1] = "X"
        
        outpout = ""
        output += "Posicion: " + str(estado) + "\n"
        output += "Camino: "

        for i in range(self.n):
            if (i+1) % 5 == 0 or i == 0 or i == self.n - 1:
                output += str(i + 1)
            else:
                output += linea[i]
        
        output += "\n     "
        for i in range(self.n):
            if (i + 1) % 5 == 0 or i == 0 or i == self.n - 1:
                output += str(i + 1)
            else:
                output += " "

        
        return output
        
 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, n):
        modelo = CamionMagico(n)
        estado_inicial = 1
        meta = lambda x: x == n
        super().__init__(estado_inicial, meta, modelo)        
    

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def heuristica_camion(n):
    def h_1_camion_magico(nodo):
        """
        La heuristica mas simple posible, el problema siempre se puede resolver
        caminando, se busca el minimo de pasos caminando, que es la diferencia entre
        la posicion actual y la posicion meta.
        """
        estado = nodo.estado
        if estado >= n:
            return 0
        pasos_caminar = n - estado
        return pasos_caminar
    return h_1_camion_magico

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def heuristica_camion_2(n):
    def h_2_camion_magico(nodo):
        """
        Esta heurística estima el número de pasos necesarios para llegar a la meta
        considerando el uso del camión mágico. La idea es multiplicar la posición
        actual por 2 hasta que se alcance o supere la posición meta. Luego, se
        calcula el número de pasos caminando desde la posición actual hasta la meta.
        Esta heurística es admisible porque nunca sobreestima el costo real para
        llegar a la meta. En el peor de los casos, se camina desde la posición
        actual hasta la meta, lo que es igual al costo real. En el mejor de los
        casos, se utiliza el camión mágico para llegar a la meta en menos pasos.
        La heurística es dominante respecto a la heurística anterior porque
        considera el uso del camión mágico, que puede ser más eficiente que
        caminar. En situaciones donde el camión mágico es útil, esta heurística
        proporcionará un costo estimado menor que la heurística anterior.

        """
        estado = nodo.estado
        if estado >= n:
            return 0
        # Estima el costo de llegar a la meta usando el camión mágico
        pasos_caminar = n - estado
        pasos_bus = 0
        while estado < n:
            estado *= 2
            pasos_bus += 1
        return min(pasos_caminar, pasos_bus)
    return h_2_camion_magico

def heuristica_camion_3(n):
    def h_3_camion_magico(nodo):
        """
        Probando con una tercera heurística como la segunda pero sin
        considerar el costo de caminar. Esta heurística estima el número de pasos
        necesarios para llegar a la meta considerando solo el uso del camión mágico.

        """
        estado = nodo.estado
        if estado >= n:
            return 0
    
        # Numero de pasos para llegar a la meta usando el camión mágico
        # multiplicando la posición actual por 2 hasta que se alcance o supere la meta
        pasos_bus = 0
        temp_estado = estado
        while temp_estado < n:
            temp_estado *= 2
            pasos_bus += 1
        return pasos_bus
    return h_3_camion_magico

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        raise NotImplementedError('Hay que hacerlo de tarea')
 
 # ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')
 

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
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

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
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(20) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')


if __name__ == "__main__":


    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PblCamionMágico(10)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    
    h_1 = heuristica_camion(10)
    h_2 = heuristica_camion_3(10)
    compara_metodos(problema, h_1, h_2)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    #problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    #compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    