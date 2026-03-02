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
        if N < 1:
            raise ValueError("N debe ser mayor o igual a 1")
        self.N = N

    def acciones(self, estado):
        x = estado
        if x < self.N and 2 * x <= self.N:
            return['caminar', 'camion']
        elif x < self.N:
            return['caminar']
        elif 2 * x <= self.N:
            return['camion']
        else: return[]
    
    def sucesor(self, estado, accion):
        x = estado

        acciones = {'caminar': (x + 1, 1), 'camion': (2 * x, 2)}

        if accion in acciones:
            return acciones[accion]
        else:
            raise ValueError(f"Accion inválida: {accion}")
    
    def terminal(self, estado):
        return estado == self.N
    
    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posición: {estado}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    La heurística considera usar el camión varias veces y después caminar 
    lo necesario para llegar exactamente a la meta, tomando el menor costo 
    posible entre esas combinaciones, lo cual es admisible.
    Esta heurística domina a h_2 porque usa más infromación del problema
    """

    x = nodo.estado
    N = N_OBJETIVO

    if x >= N:
        return 0
    mejor = float("inf")
    pos = x
    k = 0
    while pos <= N:
        mejor = min(mejor, 2*k + (N - pos))
        pos *= 2
        k += 1
    return mejor

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    En esta heurística me enfoco en únicamente en el efecto del camión. La idea es contar
    cuántas veces tendría que duplicar la posición actual x para alcanzar o superar la meta N.
    Si después de k duplicaciones llego a x*2^k >= N, entonces estimo el costo restante como 2*k, 
    ya que cada uso del camión cuesta 2min.
    Es admisible porque supone un escenario ideal donde solo uso el camión. Caminar puede ser necesario, 
    pero eso aumentaría el costo real. Como esta estimación nunca sobreestima el costo mínimo, cumple
    la condición de admisibilidad.
    """

    x = nodo.estado
    N = N_OBJETIVO

    if x >= N:
        return 0
    potencia = 1
    k = 0

    while x * potencia < N:
        potencia *= 2
        k += 1
    return 2 * k

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
def __init__(self, estado_inicial=None):
        self.meta = tuple(
            [0]*9 + [1]*9 +      
            [2]*9 + [3]*9 +      
            [4]*9 + [5]*9        
        )
        self.inicial = self.meta if estado_inicial is None else estado_inicial

    def acciones(self, estado):
        return ['arriba', "arriba'", 'frente', "frente'", 'derecha', "derecha'"]

    def sucesor(self, estado, accion):
        if accion == 'arriba':
            return self._girar_arriba(estado), 1
        elif accion == "arriba'":
            return self._girar_arriba_inv(estado), 1

        elif accion == 'frente':
            return self._girar_frente(estado), 1
        elif accion == "frente'":
            return self._girar_frente_inv(estado), 1

        elif accion == 'derecha':
            return self._girar_derecha(estado), 1
        elif accion == "derecha'":
            return self._girar_derecha_inv(estado), 1

        else:
            raise ValueError("Acción no válida")

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        print("Arriba:", estado[0:9])
        print("Derecha:", estado[9:18])
        print("Frente:", estado[18:27])
        print("Abajo:", estado[27:36])
        print("Izquierda:", estado[36:45])
        print("Atras:", estado[45:54])

    def _rotar_cara_horario(self, cara):
        return [
            cara[6], cara[3], cara[0],
            cara[7], cara[4], cara[1],
            cara[8], cara[5], cara[2]
        ]

    def _rotar_cara_antihorario(self, cara):
        return [
            cara[2], cara[5], cara[8],
            cara[1], cara[4], cara[7],
            cara[0], cara[3], cara[6]
        ]

    def _girar_arriba(self, estado):
        s = list(estado)

        s[0:9] = self._rotar_cara_horario(s[0:9])

        frente = s[18:21]
        derecha = s[9:12]
        atras = s[45:48]
        izquierda = s[36:39]

        s[18:21] = izquierda
        s[9:12] = frente
        s[45:48] = derecha
        s[36:39] = atras

        return tuple(s)

    def _girar_arriba_inv(self, estado):
        s = list(estado)

        s[0:9] = self._rotar_cara_antihorario(s[0:9])

        frente = s[18:21]
        derecha = s[9:12]
        atras = s[45:48]
        izquierda = s[36:39]

        s[18:21] = derecha
        s[9:12] = atras
        s[45:48] = izquierda
        s[36:39] = frente

        return tuple(s)
    def _girar_frente(self, estado):
        s = list(estado)

        s[18:27] = self._rotar_cara_horario(s[18:27])

        arriba = [6, 7, 8]        
        derecha = [9, 12, 15]     
        abajo = [27, 28, 29]      
        izquierda = [38, 41, 44]  

        a = [s[i] for i in arriba]
        d = [s[i] for i in derecha]
        ab = [s[i] for i in abajo]
        iz = [s[i] for i in izquierda]

        for j in range(3):
            s[derecha[j]] = a[j]

        s[abajo[0]], s[abajo[1]], s[abajo[2]] = d[2], d[1], d[0]

        s[izquierda[0]], s[izquierda[1]], s[izquierda[2]] = ab[2], ab[1], ab[0]

        for j in range(3):
            s[arriba[j]] = iz[j]

        return tuple(s)


    def _girar_frente_inv(self, estado):
        s = estado
        for _ in range(3):
            s = self._girar_frente(s)
        return s
    
    def _girar_derecha(self, estado):
        s = list(estado)

        s[9:18] = self._rotar_cara_horario(s[9:18])

        arriba = [2, 5, 8]    
        frente = [20, 23, 26]   
        abajo = [29, 32, 35]    
        atras = [45, 48, 51]    

        a = [s[i] for i in arriba]
        f = [s[i] for i in frente]
        ab = [s[i] for i in abajo]
        at = [s[i] for i in atras]

        for j in range(3):
            s[frente[j]] = a[j]
            s[abajo[j]] = f[j]
            s[atras[j]] = ab[j]
            s[arriba[j]] = at[j]

        return tuple(s)

    def _girar_derecha_inv(self, estado):
        s = estado
        for _ in range(3):
         s = self._girar_derecha(s)
        return s
    
def h_1_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    e = nodo.estado
    objetivos = [0,1,2,3,4,5]
    rangos = [(0,9),(9,18),(18,27),(27,36),(36,45),(45,54)]

    mal = 0
    for cara, (a,b) in enumerate(rangos):
        color = objetivos[cara]
        for i in range(a,b):
            if e[i] != color:
                mal += 1

    return mal // 8

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
    e = nodo.estado
    rangos = [(0,9),(9,18),(18,27),(27,36),(36,45),(45,54)]

    mezcla = 0
    for a,b in rangos:
        mezcla += (len(set(e[a:b])) - 1)  

    return mezcla
def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = 1  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(20)
    N_OBJETIVO = problema.N
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PbCuboRubik()  
    pos_inicial = problema._girar_arriba(problema.meta) 
    compara_metodos(problema, pos_inicial, h_1_problema_1, h_2_problema_1)

    N = 20
    problema = PbCamionMagico(N)
    s0 = 1

    print("BFS")
    plan, nodos = busquedas.busqueda_ancho(problema, s0)
    print(plan)
    print("Nodos visitados:", nodos)

    print("\nCosto Uniforme")
    plan, nodos = busquedas.busqueda_costo_uniforme(problema, s0)
    print(plan)
    print("Nodos visitados:", nodos)

    pb = PbCuboRubik()
    estado0 = pb.meta
    print("Cubo resuelto:")
    pb.bonito(estado0)

    estado1, _ = pb.sucesor(estado0, 'frente')

    print("\nDespués de mover frente:")
    pb.bonito(estado1)
