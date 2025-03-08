#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas

# ------------------------------------------------------------
#  Problema Misioneros-Canibales
# ------------------------------------------------------------

class MisionerosCanibales(busquedas.ModeloBusqueda):
    """
    Problema de los misioneros y caníbales.
    Estado representado como (M_izq, C_izq, bote, M_der, C_der),
    donde:
        - M_izq y C_izq son el número de misioneros y caníbales en la orilla izquierda.
        - M_der y C_der son el número de misioneros y caníbales en la orilla derecha.
        - bote = 1 si está en la izquierda, 0 si está en la derecha.
    """
    def __init__(self):
        self.capacidad_bote = 2
        self.movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

    def acciones_legales(self, estado):
        M_izq, C_izq, bote, M_der, C_der = estado
        acciones = []
        for m, c in self.movimientos:
            if bote == 1:  # Bote en la izquierda
                nuevo_estado = (M_izq - m, C_izq - c, 0, M_der + m, C_der + c)
            else:  # Bote en la derecha
                nuevo_estado = (M_izq + m, C_izq + c, 1, M_der - m, C_der - c)
            if self.es_estado_valido(nuevo_estado):
                acciones.append((m, c))
        return acciones

    def sucesor(self, estado, accion):
        M_izq, C_izq, bote, M_der, C_der = estado
        m, c = accion
        if bote == 1:
            return (M_izq - m, C_izq - c, 0, M_der + m, C_der + c)
        else:
            return (M_izq + m, C_izq + c, 1, M_der - m, C_der - c)
    
    def costo_local(self, estado, accion):
        return 1

    def es_estado_valido(self, estado):
        M_izq, C_izq, _, M_der, C_der = estado
        if min(M_izq, C_izq, M_der, C_der) < 0:
            return False
        if (M_izq > 0 and M_izq < C_izq) or (M_der > 0 and M_der < C_der):
            return False
        return True

    @staticmethod
    def bonito(estado):
        return f"Izq: ({estado[0]}M, {estado[1]}C) | Bote: {'Izq' if estado[2] else 'Der'} | Der: ({estado[3]}M, {estado[4]}C)"

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
        if estado + 1 <= self.n:
            acciones.append("caminar")
        if estado * 2 <= self.n:
            acciones.append("camion_magico")
        return acciones

    def sucesor(self, estado, accion):
        if accion == "caminar":
            return estado + 1
        elif accion == "camion_magico":
            return estado * 2

    def costo_local(self, estado, accion):
        return 1 if accion == "caminar" else 2

    @staticmethod
    def bonito(estado):
        return f"Posición actual: {estado}"

 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMagico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, n):
        estado_inicial = 1
        meta = lambda estado: estado == n
        modelo = CamionMagico(n)
        super().__init__(estado_inicial, meta, modelo)
    

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
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

def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube

    El cubo estara compuesto de 6 listas de valores enumeradas de 0 a 5,
    donde la lista 0 sera la cara frontal de este y 4 y 5 seran las
    caras inferior y superior respectivamente. Los caracteres de las 6 
    listas representan un color:

    A = Azul
    R = Rojo
    V = Verde
    N = Naranja
    B = Blanco
    C = Cafe

    
    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        aux = A

    def sucesor(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        normal = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        giro = {12, 13}
        if accion in normal:
            return 1
        if accion in giro:
            return 3
 
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
#  Diseñadas para el problema MisionerosCanibales
# ------------------------------------------------------------
def h_1_MisionerosCanibales(nodo):
    """
    Heurística que cuenta cuántos misioneros y caníbales quedan en la orilla izquierda.

    Como va contando los pasajeros que van de un lado a otro y van de dos en dos, 
    el valor final sera inferior al costo
    """
    M_izq, C_izq, bote, M_der, C_der = nodo.estado
    return (M_izq + C_izq) // 2  # Cada cruce mueve hasta 2 personas


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política:
# ------------------------------------------------------------
def h_2_MisionerosCanibales(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    En esta heuristica, se prioriza el movimiento de Misioneros
    sobre Canibales, siguiendo la formula:
    h2 = M_izq + C_izq/2

    En este caso, al priorizar el movimiento de Misioneros, se
    minimiza la perdida causada por los Canibales a los Misioneros,
    Haciendo que el valor final sea menor al costo.
    """
    M_izq, C_izq, bote, M_der, C_der = nodo.estado
    return M_izq + (C_izq / 2)  # Prioriza mover misioneros



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
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')


if __name__ == "__main__":
    print("---------- 1 - Problema Implementado -------------")
    estado_inicial = (3, 3, 1, 0, 0)
    meta = lambda estado: estado == (0, 0, 0, 3, 3)
    problema = busquedas.ProblemaBusqueda(estado_inicial, meta, MisionerosCanibales())

    solucion = busquedas.busqueda_ancho(problema)
    if solucion:
        print("Solución encontrada:")
        print(solucion)
    else:
        print("No se encontró solución.")
    
    
    # 2 - Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    print("---------- 2 - Camion Magico con A* -------------")
    problema = PblCamionMagico(20)
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico) # <--- PONLE LOS PARÁMETROS QUE NECESITES
    
    # 4 - Heuristicas Desarrolladas
    print("---------- 4 y 5 - Heuristicas Propias -------------")
    problema = busquedas.ProblemaBusqueda((3, 3, 1, 0, 0), lambda estado: estado == (0, 0, 0, 3, 3), MisionerosCanibales())
    compara_metodos(problema, h_1_MisionerosCanibales, h_2_MisionerosCanibales)

    '''
    Los resultados muestran que h1 y h2 tienen un costo igual de 11, pero h1 visita 15 nodos
    mientras que h2 visita 29, lo que muestra que h1 es mas eficiente que h2 y por lo tanto es dominante.
    '''

    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
   # problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
   # compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    