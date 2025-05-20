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
    def __init__(self, n):
        assert n >=1, "El número de pasajeros debe ser mayor o igual que 1"
        self.n = n

    def acciones_legales(self, estado):
        a = []
        if estado < self.n:
            a.append('camina')
        if 2 * estado <= self.n:
            a.append('pasa')
        return a
    
    def sucesor(self, estado, accion):
        if accion == 'camina':
            return estado + 1
        if accion == 'pasa':
            return 2 * estado
        raise ValueError('Acción no válida')

    def costo_local(self, estado, accion):
        if accion == 'camina':
            return 1
        if accion == 'pasa':
            return 2
        raise ValueError('Acción no válida')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Estado actual :  {estado} pasajeros"
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, n):
        assert n >=1, "El número de pasajeros debe ser mayor o igual que 1"
        self.estado_inicial = 1
        self.n = n
        self.modelo = CamionMagico(n)

    def es_meta(self, estado):
        """Verifca si el estado actual es meta"""
    
        return estado == self.n
    
    def acciones_legales(self, estado):
        """Devuelve las acciones legales"""
        return self.modelo.acciones_legales(estado)
    
    def sucesor(self, estado, accion):
        """Devuelve el estado sucesor"""
        return self.modelo.sucesor(estado, accion)
    
    def costo_local(self, estado, accion):
        """Devuelve el costo local"""
        return self.modelo.costo_local(estado, accion)
    

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """

    """Esta primera heuristica es la que se nos viene a la mente a todos
    cuando iniciamos a resolver el problema del camión mágico.
    Comenzamos por analizar el estado actual y duplicamos mientras
    que el estado sea menor o igual a n, si no llegamos exactamente, 
    caminamos los pasos restantes."""

    estado = nodo.estado
    n = nodo.problema.n
    pasos = 0

    while estado * 2 <= n:
        estado *= 2
        pasos += 1
    pasos += (n - estado)
    return pasos


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
    
    """
    Mejora sobre h_1: Permite caminar algunos pasos antes de empezar a duplicar,
    reduciendo el número total de movimientos en ciertos casos.
    Antes de empezar a duplicar, verificamos si avanzar algunos pasos iniciales
    puede reducir el número total de movimientos. Esto es útil cuando N no es
    una potencia de 2, porque caminar primero puede permitir alcanzar N en menos pasos.
    """
    estado = nodo.estado
    n = nodo.problema.n
    pasos = 0
    
    # Opcionalmente caminar algunos pasos antes de duplicar
    while (estado % 2 != 0) and (estado < n):
        estado += 1
        pasos += 1
    
    # Ahora, realizar las duplicaciones
    while estado * 2 <= n:
        estado *= 2
        pasos += 1
    
    # Pasos restantes para llegar exactamente a N
    pasos += (n - estado)
    return pasos

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    Estado = tuple de 54 caracteres ('U','L','F','R','B','D') en orden Singmaster.

    Índices de referencia (fila x columna):
                0  1  2
                3  4  5
                6  7  8        ← U

      9 10 11   18 19 20   27 28 29   36 37 38
     12 13 14   21 22 23   30 31 32   39 40 41  ← L F R B
     15 16 17   24 25 26   33 34 35   42 43 44

               45 46 47
               48 49 50
               51 52 53        ← D
    """


    CARAS = ('U', 'L', 'F', 'R', 'B', 'D')

    def __init__(self, estado_inicial=None):
        # Cubo resuelto si no se indica lo contrario
        if estado_inicial is None:
            self.estado_inicial = tuple(
                cara for cara in self.CARAS for _ in range(9)
            )
        else:
            if len(estado_inicial) != 54:
                raise ValueError("El estado debe tener 54 stickers.")
            self.estado_inicial = tuple(estado_inicial)

    def acciones_legales(self, estado):
        acciones = (
        "U", "U'",
        "D", "D'",
        "L", "L'",
        "R", "R'",
        "F", "F'",
        "B", "B'",
    )
        
        return list(acciones)

    def sucesor(self, estado, accion):
        cara = accion[0]
        antihorario = len(accion) > 1 and accion[1] == "'"
        nuevo = list(estado)

        if cara == "U":
            nuevo = self._rotar_cara(nuevo, self._U_FACE, antihorario)
            nuevo = self._ciclo4(nuevo, self._U_GRUPOS, antihorario)

        elif cara == "D":
            nuevo = self._rotar_cara(nuevo, self._D_FACE, antihorario)
            nuevo = self._ciclo4(nuevo, self._D_GRUPOS, not antihorario)

        elif cara == "L":
            nuevo = self._rotar_cara(nuevo, self._L_FACE, antihorario)
            nuevo = self._ciclo4(nuevo, self._L_GRUPOS, antihorario)
        
        elif cara == "R":
            nuevo = self._rotar_cara(nuevo, self._R_FACE, antihorario)
            nuevo = self._ciclo4(nuevo, self._R_GRUPOS, antihorario)

        elif cara == "F":
            nuevo = self._rotar_cara(nuevo, self._F_FACE, antihorario)
            nuevo = self._ciclo4(nuevo, self._F_GRUPOS, antihorario)

        elif cara == "B":
            nuevo = self._rotar_cara(nuevo, self._B_FACE, antihorario)
            nuevo = self._ciclo4(nuevo, self._B_GRUPOS, antihorario)

        return tuple(nuevo)


    @staticmethod
    def _rotar_cara(stickers, idxs, antihorario=False):
        """Rota una cara (8 stickers externos, horario por defecto)."""
        s = list(stickers)
        paso = -2 if antihorario else 2
        for i in range(0, 8, 2):
            s[idxs[i]] = stickers[idxs[(i+paso) % 8]]
            s[idxs[i+1]] = stickers[idxs[(i+paso+1) % 8]]
        return tuple(s)

    @staticmethod
    def _ciclo4(stickers, grupos, antihorario=False):
        """Cicla los 4 grupos de stickers al rededor de una cara."""
        s = list(stickers)
        if antihorario:
            temp = [stickers[i] for i in grupos[0]]
            for i in range(3):
                for j in range(len(grupos[i])):
                    s[grupos[i][j]] = stickers[grupos[i+1][j]]
            for j in range(len(grupos[3])):
                s[grupos[3][j]] = temp[j]
        else:
            temp = [stickers[i] for i in grupos[3]]
            for i in range(3, 0, -1):
                for j in range(len(grupos[i])):
                    s[grupos[i][j]] = stickers[grupos[i-1][j]]
            for j in range(len(grupos[0])):
                s[grupos[0][j]] = temp[j]
        return tuple(s)

    # Índices para el movimiento U
    _U_FACE = [0, 1, 2, 5, 8, 7, 6, 3]
    _U_GRUPOS = [
        [9, 10, 11],    # L
        [18, 19, 20],   # F
        [27, 28, 29],   # R
        [36, 37, 38],   # B
    ]

    # índices para el movimiento D
    _D_FACE = [45, 46, 47, 50, 53, 52, 51, 48]
    _D_GRUPOS = [
        [24, 25, 26],   # F (fila inferior)
        [33, 34, 35],   # R
        [42, 43, 44],   # B
        [15, 16, 17],   # L
    ]

    #índices para el movimiento L
    _L_FACE = [9, 10, 11, 14, 17, 16, 15, 12]
    _L_GRUPOS = [
        [0, 3, 6],     # U (columna izquierda)
        [18, 21, 24],  # F
        [45, 48, 51],  # D
        [44, 41, 38],  # B (columna derecha, en orden inverso)
    ]


    # índices para el movimiento R
    _R_FACE = [27, 28, 29, 32, 35, 34, 33, 30]
    _R_GRUPOS = [
        [2, 5, 8],      # U (columna derecha)
        [20, 23, 26],   # F
        [47, 50, 53],   # D
        [42, 39, 36],   # B (columna izquierda, orden invertido)
    ]

        # ────────────── índices para el movimiento F
    _F_FACE = [18, 19, 20, 23, 26, 25, 24, 21]
    _F_GRUPOS = [
        [6, 7, 8],      # U (fila inferior)
        [27, 30, 33],   # R (columna izquierda)
        [45, 46, 47],   # D (fila superior, en orden)
        [17, 14, 11],   # L (columna derecha, en orden inverso)
    ]

    # ────────────── índices para el movimiento B
    _B_FACE = [36, 37, 38, 41, 44, 43, 42, 39]
    _B_GRUPOS = [
        [0, 1, 2],      # U (fila superior)
        [9, 12, 15],    # L (columna izquierda)
        [51, 52, 53],   # D (fila inferior, en orden)
        [35, 32, 29],   # R (columna derecha, en orden inverso)
    ]


    def costo_local(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

        # ───────────────────────────── helpers internos
    @staticmethod
    def _rotar_cara(stickers, idxs, antihorario=False):
        """
        Rota una cara 90° (horario por defecto) intercambiando los 8
        stickers que rodean el centro, cuyos índices vienen en `idxs`
        (ordenados en sentido horario).
        """
        s = list(stickers)
        paso = -2 if antihorario else 2   # mover 2 posiciones en el ciclo
        for i in range(0, 8, 2):
            s[idxs[i]] = stickers[idxs[(i+paso) % 8]]
            s[idxs[i+1]] = stickers[idxs[(i+paso+1) % 8]]
        return tuple(s)

    @staticmethod
    def _ciclo4(stickers, grupos, antihorario=False):
        """
        Cicla los 4 grupos (listas de índices) que corresponden a los bordes
        de la cara que se gira.  Copia completa (no solo referencias).
        """
        s = list(stickers)
        g = grupos[::-1] if antihorario else grupos
        for i in range(4):
            origen = grupos[(i - 1) % 4] if antihorario else grupos[(i + 1) % 4]
            for dst, src in zip(grupos[i], origen):
                s[dst] = stickers[src]
        return tuple(s)


    @staticmethod
    def bonito(estado):
        if len(estado) != 54:
            raise ValueError("Estado inválido (se esperaban 54 stickers)")

        def fila(idxs):
            return " ".join(estado[i] for i in idxs)

        # Cara U
        print("      " + fila([0, 1, 2]))
        print("      " + fila([3, 4, 5]))
        print("      " + fila([6, 7, 8]))

        # Cinturón L‑F‑R‑B
        filas_cinturon = [
            [ 9,10,11,  18,19,20,  27,28,29,  36,37,38],
            [12,13,14,  21,22,23,  30,31,32,  39,40,41],
            [15,16,17,  24,25,26,  33,34,35,  42,43,44],
        ]
        for r in filas_cinturon:
            print(
                fila(r[0:3]) + "  " + fila(r[3:6]) + "  "
                + fila(r[6:9]) + "  " + fila(r[9:12])
            )

        # Cara D
        print("      " + fila([45,46,47]))
        print("      " + fila([48,49,50]))
        print("      " + fila([51,52,53]))
 
 # ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

def test():
    cubo = CuboRubik()
    print(cubo.acciones_legales(cubo.estado_inicial))
    CuboRubik.bonito(cubo.estado_inicial)

    nuevo_estado = cubo.sucesor(cubo.estado_inicial, "U")
    print("\nDespués de U:")
    CuboRubik.bonito(nuevo_estado)

    nuevo_estado2 = cubo.sucesor(nuevo_estado, "U'")
    print("\nDespués de U seguido de U':")
    CuboRubik.bonito(nuevo_estado2)

    d1 = cubo.sucesor(cubo.estado_inicial, "D")
    print("\nDespués de D:")
    CuboRubik.bonito(d1)

    regreso = cubo.sucesor(d1, "D'")
    print("\nDespués de D seguido de D':")
    CuboRubik.bonito(regreso)

        # ------------------- prueba L y L'
    l1 = cubo.sucesor(cubo.estado_inicial, "L")
    print("\nDespués de L:")
    CuboRubik.bonito(l1)

    regreso_l = cubo.sucesor(l1, "L'")
    print("\nDespués de L seguido de L':")
    CuboRubik.bonito(regreso_l)

        # ------------------- prueba R y R'
    r1 = cubo.sucesor(cubo.estado_inicial, "R")
    print("\nDespués de R:")
    CuboRubik.bonito(r1)

    regreso_r = cubo.sucesor(r1, "R'")
    print("\nDespués de R seguido de R':")
    CuboRubik.bonito(regreso_r)


        # ------------------- prueba F y F'
    f1 = cubo.sucesor(cubo.estado_inicial, "F")
    print("\nDespués de F:")
    CuboRubik.bonito(f1)

    regreso_f = cubo.sucesor(f1, "F'")
    print("\nDespués de F seguido de F':")
    CuboRubik.bonito(regreso_f)

    # ------------------- prueba B y B'
    b1 = cubo.sucesor(cubo.estado_inicial, "B")
    print("\nDespués de B:")
    CuboRubik.bonito(b1)

    regreso_b = cubo.sucesor(b1, "B'")
    print("\nDespués de B seguido de B':")
    CuboRubik.bonito(regreso_b)



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


    # # Compara los métodos de búsqueda para el problema del camión mágico
    # # con las heurísticas que desarrollaste
    # n = 20
    # problema = PblCamionMágico(20)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # # # Compara los métodos de búsqueda para el problema del cubo de rubik
    # # # con las heurísticas que desarrollaste
    # # problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    # # compara_metodos(problema, h_1_problema_1, h_2_problema_1)

    test()
    