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
class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    Estado: (x, N)
    Meta: x == N
    """
    def __init__(self, N):
        self.N = int(N)
        if self.N < 1:
            raise ValueError("N debe ser >= 1")

    def acciones(self, estado):
        x, N = estado
        acc = []
        if x < N:
            acc.append('caminar')
        if 2 * x <= N:
            acc.append('camion')
        return acc

    def sucesor(self, estado, accion):
        x, N = estado
        if accion == 'caminar':
            return (x + 1, N), 1
        elif accion == 'camion':
            return (2 * x, N), 2
        else:
            raise ValueError(f"Accion desconocida: {accion}")

    def terminal(self, estado):
        x, N = estado
        return x == N

    @staticmethod
    def bonito(estado):
        x, N = estado
        return f"Posición: {x} / Meta: {N}"


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    h1(x,N) = N - x

    Admisible: caminar todo lo que falta siempre logra la meta con costo N-x,
    entonces el costo óptimo desde (x,N) nunca es mayor que N-x. No sobreestima.
    """
    x, N = nodo.estado
    return max(0, N - x)

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    h2(x,N) = ceil((N - x)/2)

    Admisible (cota inferior):
    Aunque imagináramos que puedes avanzar 2 posiciones por cada 1 de costo (optimista),
    todavía necesitarías al menos ceil((N-x)/2) de costo para cubrir la diferencia.
    Como es optimista, no sobreestima al costo real: admisible.

    Nota: Es más informada que 0, pero no necesariamente domina a h1.
    """
    x, N = nodo.estado
    d = max(0, N - x)
    return (d + 1) // 2

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    Modelo simplificado de "cubo de Rubik" (mini-rubik) para poder usar A*.

    Representamos el estado como una tupla de 8 piezas (0..7) en posiciones 0..7.
    - meta: (0,1,2,3,4,5,6,7)
    - acciones: cuatro "giros" que aplican ciclos (permutaciones) sobre 4 posiciones.

    Cada acción cuesta 1.

    Nota: Esto NO es el cubo 3x3 completo; es una abstracción tipo "puzzle de permutación"
    para poder diseñar heurísticas y comparar A* como pide la tarea.
    """
    def __init__(self, meta=(0, 1, 2, 3, 4, 5, 6, 7)):
        self.meta = tuple(meta)

        # Definimos 4 "movimientos" como ciclos sobre índices.
        # Cada movimiento reordena piezas en esas posiciones (ciclo de 4).
        # Ej: U gira (0,1,2,3): 0<-3,1<-0,2<-1,3<-2
        self.movs = {
            'U': (0, 1, 2, 3),
            'D': (4, 5, 6, 7),
            'L': (0, 3, 7, 4),
            'R': (1, 2, 6, 5),
        }

    def acciones(self, estado):
        # Siempre puedes aplicar cualquier giro
        return list(self.movs.keys())

    def sucesor(self, estado, accion):
        if accion not in self.movs:
            raise ValueError(f"Acción desconocida: {accion}")

        s = list(estado)
        a, b, c, d = self.movs[accion]

        # ciclo: a<-d, b<-a, c<-b, d<-c
        s[a], s[b], s[c], s[d] = s[d], s[a], s[b], s[c]
        return tuple(s), 1  # costo local 1

    def terminal(self, estado):
        return tuple(estado) == self.meta

    @staticmethod
    def bonito(estado):
        # Vista simple 2x4
        s = list(estado)
        return (
            f"{s[0]} {s[1]} {s[2]} {s[3]}\n"
            f"{s[4]} {s[5]} {s[6]} {s[7]}"
        )

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_problema_1(nodo):
    """
    h1 = ceil(mal_colocadas / 4)

    Admisible:
    Cada giro solo afecta 4 posiciones. En el mejor caso, un giro podría colocar correctamente
    hasta 4 piezas (optimista). Por lo tanto, si hay k piezas mal colocadas, se requieren al menos
    ceil(k/4) movimientos. Es una cota inferior => no sobreestima => admisible.
    """
    estado = nodo.estado
    # meta fija del mini-rubik
    meta = (0, 1, 2, 3, 4, 5, 6, 7)
    mal = sum(1 for i, v in enumerate(estado) if v != meta[i])
    return (mal + 3) // 4

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    h2 = ceil(min_swaps_para_ordenar / 3)

    Admisible:
    Para convertir una permutación en la identidad, el mínimo número de swaps necesarios es:
        min_swaps = n - (#ciclos)
    Un giro de 4 posiciones equivale, como máximo, a 3 swaps (un 4-ciclo = 3 transposiciones).
    Entonces se requieren al menos ceil(min_swaps/3) giros para resolver.
    Es una cota inferior => no sobreestima => admisible.

    Dominancia:
    No está garantizado que h2 domine a h1 para todos los estados, pero normalmente h2 suele ser
    más informada que contar mal colocadas (porque captura estructura de ciclos).
    """
    estado = nodo.estado
    n = len(estado)
    # meta identidad 0..7
    # Construimos perm p donde p[i] = pieza en posicion i (queremos p[i]=i)
    # Para ciclos, seguimos i -> p[i]
    visit = [False] * n
    ciclos = 0
    for i in range(n):
        if not visit[i]:
            ciclos += 1
            j = i
            while not visit[j]:
                visit[j] = True
                j = estado[j]  # siguiente
    min_swaps = n - ciclos
    return (min_swaps + 2) // 3



def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    plan1, nodos1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    plan2, nodos2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)

    print('-' * 60)
    print('Método'.ljust(15) + 'Costo'.ljust(15) + 'Nodos visitados')
    print('-' * 60)
    print('A* con h1'.ljust(15) + str(plan1.costo if plan1 else None).ljust(15) + str(nodos1))
    print('A* con h2'.ljust(15) + str(plan2.costo if plan2 else None).ljust(15) + str(nodos2))
    print('-' * 60 + '\n')

if __name__ == "__main__":
    # ---------------- Camión mágico ----------------
    N = 31
    problema = PbCamionMagico(N)
    pos_inicial = (1, N)
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)

    # ---------------- Mini-Rubik ----------------
    problema = PbCuboRubik()

    # “Revolver” aplicando 2 movimientos a la meta
    s0, _ = problema.sucesor(problema.meta, 'U')
    s0, _ = problema.sucesor(s0, 'L')

    print("\nMini-Rubik estado inicial:")
    print(PbCuboRubik.bonito(s0), "\n")

    compara_metodos(problema, s0, h_1_problema_1, h_2_problema_1)