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
    def __init__(self, meta):
        self.x0 = 0
        self.meta = meta

    def acciones(self, estado):
        """
        @param estado: posicion actual
        @return: lista de acciones ["caminar", "camion"]
        """
        acciones= []
        if estado + 1 <= self.meta:
            acciones.append('caminar')
            
        if estado * 2 <= self.meta:
            acciones.append('camion')
        
        return acciones

    def sucesor(self, estado, accion):  
        if accion == 'caminar':
            return estado + 1, 1
        if accion == 'camion':
            return estado * 2, 2
        
        raise ValueError("Acción no válida")

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return print(f"posicion: {estado}")
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo, problema):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    Esta heuristica calcula el costo suponiendo que siempre se va usar el camion y que va a crecer de su posicion actual hasta la meta
    
    Esta heuristica es admisible porque nunca va a sobrestimar el costo real porque es muy optimista y asume que cada accion reduce la distancia exponencialmente y el costo real siempre sera mayor porque incluye los pasos adicionales
     
    """
    estado = nodo.estado
    meta = problema.meta
    
    if estado >= meta:
        return 0
    
    if estado == 0:
        return meta
    
    factor = meta / estado
    duplicaciones = math.ceil(math.log2(factor))
    
    return duplicaciones * 2


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo, problema):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Esta heuristica calcula el costo si usamos el camion todas las veces posibles sin pasarnos de la meta y luego caminamos el resto del camino caminando
    
    Es admisible porque solo usa el camion cuando no se pase de la meta, toma en cuenta el camino ideal en el que todo el trayecto se puede hacer en camion
    
    Esta heuristica es dominante a h_1 porque considera no solo usar el camion si no tambien el caminar por lo que esta mas cerca del costo real
    """
    estado = nodo.estado
    meta = problema.meta
    
    if estado >= meta:
        return 0
    
    n = 0
    pos = estado
    while pos * 2 <= meta:
        pos *= 2
        n += 1
    mejor_costo = n * 2 + (meta - pos)
    return mejor_costo

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    estado: 6 caras 
    Up
    Down
    Front
    Back
    Left
    Right
    cada cara tiene 9 stickers 
    tupla de 54 elementos 6 caras x 9 stickers
    
    """
    def __init__(self, estado_inicial=None):
        self.meta = (
            'W','W','W','W','W','W','W','W','W',
            'Y','Y','Y','Y','Y','Y','Y','Y','Y',
            'R','R','R','R','R','R','R','R','R',
            'O','O','O','O','O','O','O','O','O',
            'G','G','G','G','G','G','G','G','G',
            'B','B','B','B','B','B','B','B','B'
        )
        if estado_inicial is None:
            self.x0 = self.meta
        else:
            self.x0 = estado_inicial

    def acciones(self, estado):
        return ['U', "U'", 'D', "D'", 'F', "F'", 
                'B', "B'", 'L', "L'", 'R', "R'"]

    def sucesor(self, estado, accion):
        nuevo = list(estado)
        
        inverso = accion.endswith("'")
        cara = accion[0]
        
        veces = 3 if inverso else 1
        
        for _ in range(veces):
            nuevo = self._rotar_cara(nuevo, cara)
        
        return tuple(nuevo), 1
    def _rotar_cara(self, estado, cara):
        """
        Rota una cara 90° horario
        
        Cada rotación hace DOS cosas:
        1. Rotar los 9 stickers de la cara en sí misma
        2. Mover stickers entre las caras adyacentes
        """
        nuevo = estado[:]
        
        if cara == 'U':
            nuevo[0], nuevo[1], nuevo[2] = estado[6], estado[3], estado[0]
            nuevo[3], nuevo[5] = estado[7], estado[1]
            nuevo[6], nuevo[7], nuevo[8] = estado[8], estado[5], estado[2]
            
            nuevo[18], nuevo[19], nuevo[20] = estado[36], estado[37], estado[38]  # L → F
            nuevo[45], nuevo[46], nuevo[47] = estado[18], estado[19], estado[20]  # F → R
            nuevo[27], nuevo[28], nuevo[29] = estado[45], estado[46], estado[47]  # R → B
            nuevo[36], nuevo[37], nuevo[38] = estado[27], estado[28], estado[29]  # B → L
        
        elif cara == 'D':
            nuevo[9], nuevo[10], nuevo[11] = estado[15], estado[12], estado[9]
            nuevo[12], nuevo[14] = estado[16], estado[10]
            nuevo[15], nuevo[16], nuevo[17] = estado[17], estado[14], estado[11]
            
            nuevo[24], nuevo[25], nuevo[26] = estado[51], estado[52], estado[53]  # R → F
            nuevo[42], nuevo[43], nuevo[44] = estado[24], estado[25], estado[26]  # F → L
            nuevo[33], nuevo[34], nuevo[35] = estado[42], estado[43], estado[44]  # L → B
            nuevo[51], nuevo[52], nuevo[53] = estado[33], estado[34], estado[35]  # B → R
        
        elif cara == 'F':
            nuevo[18], nuevo[19], nuevo[20] = estado[24], estado[21], estado[18]
            nuevo[21], nuevo[23] = estado[25], estado[19]
            nuevo[24], nuevo[25], nuevo[26] = estado[26], estado[23], estado[20]
            
            # Rotar stickers 
            nuevo[6], nuevo[7], nuevo[8] = estado[44], estado[41], estado[38]      # L → U
            nuevo[45], nuevo[48], nuevo[51] = estado[6], estado[7], estado[8]      # U → R
            nuevo[11], nuevo[10], nuevo[9] = estado[45], estado[48], estado[51]    # R → D
            nuevo[38], nuevo[41], nuevo[44] = estado[9], estado[10], estado[11]    # D → L
        
        elif cara == 'B':
            nuevo[27], nuevo[28], nuevo[29] = estado[33], estado[30], estado[27]
            nuevo[30], nuevo[32] = estado[34], estado[28]
            nuevo[33], nuevo[34], nuevo[35] = estado[35], estado[32], estado[29]
            
            # Rotar stickers
            nuevo[2], nuevo[1], nuevo[0] = estado[47], estado[50], estado[53]      # R → U
            nuevo[36], nuevo[39], nuevo[42] = estado[2], estado[1], estado[0]      # U → L
            nuevo[15], nuevo[16], nuevo[17] = estado[36], estado[39], estado[42]   # L → D
            nuevo[53], nuevo[50], nuevo[47] = estado[17], estado[16], estado[15]   # D → R
        
        elif cara == 'L':
            nuevo[36], nuevo[37], nuevo[38] = estado[42], estado[39], estado[36]
            nuevo[39], nuevo[41] = estado[43], estado[37]
            nuevo[42], nuevo[43], nuevo[44] = estado[44], estado[41], estado[38]
            
            # Rotar stickers
            nuevo[0], nuevo[3], nuevo[6] = estado[35], estado[32], estado[29]      # B → U
            nuevo[18], nuevo[21], nuevo[24] = estado[0], estado[3], estado[6]      # U → F
            nuevo[9], nuevo[12], nuevo[15] = estado[18], estado[21], estado[24]    # F → D
            nuevo[29], nuevo[32], nuevo[35] = estado[15], estado[12], estado[9]    # D → B
        
        elif cara == 'R':
            nuevo[45], nuevo[46], nuevo[47] = estado[51], estado[48], estado[45]
            nuevo[48], nuevo[50] = estado[52], estado[46]
            nuevo[51], nuevo[52], nuevo[53] = estado[53], estado[50], estado[47]
            
            # Rotar stickers 
            nuevo[2], nuevo[5], nuevo[8] = estado[20], estado[23], estado[26]      # F → U
            nuevo[27], nuevo[30], nuevo[33] = estado[2], estado[5], estado[8]      # U → B
            nuevo[11], nuevo[14], nuevo[17] = estado[27], estado[30], estado[33]   # B → D
            nuevo[20], nuevo[23], nuevo[26] = estado[17], estado[14], estado[11]   # D → F
        
        return nuevo

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo, problema):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE
    
    Esta heurisitca cuenta cuantos stickers estan mal colocados y los divide entre 8, por lo que asume que cada movimiento puede corregir 8 stickers a la vez por lo que siempre es menor o igual que el costo total por lo que es admisible

    """
    estado = nodo.estado
    meta = problema.meta
    
    mal_colocados = sum(1 for i in range(54) if estado[i] != meta[i])
    
    return mal_colocados // 8


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo, problema):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Esta heuristica cuenta el numero de caras correctas con sus 9 stickers tienen el color correcto, esta es admisible porque asume que en el mejor de los casos arregla una cara de un solo movimientos y resolver una cara puede entorpecer a otras por lo que siempre es menor igual que el costo real
    
    Esta domina a h1 porque explora muchos menos nodos y esta mas cerca del costo real
    """
    estado = nodo.estado
    meta = problema.meta
    
    caras_mal = 0
    
    for inicio in [0, 9, 18, 27, 36, 45]:  # Inicio de cada cara
        # Verificar si algún sticker de esta cara está mal
        if any(estado[i] != meta[i] for i in range(inicio, inicio+9)):
            caras_mal += 1
    
    return caras_mal



def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    if pos_inicial is not None:
        problema.x0 = pos_inicial 
    
    h1 = lambda nodo: heuristica_1(nodo, problema)
    h2 = lambda nodo: heuristica_2(nodo, problema)
    
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, h1)
    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, h2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(19) 
          + str(nodos1).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(nodos2).center(17))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(50)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    
    estado, _ = PbCuboRubik().sucesor(PbCuboRubik().x0, 'U')
    estado, _ = PbCuboRubik().sucesor(estado, 'R')
    estado, _ = PbCuboRubik().sucesor(estado, 'F')
    

    pos_inicial = None   # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCuboRubik(estado)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, None, h_1_problema_1, h_2_problema_1)