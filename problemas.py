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
    def __init__(self, pos_inicial=1, meta=50):
        inicio_seguro = int(pos_inicial)
        meta_segura = int(meta)

        if inicio_seguro >= meta_segura:
            raise ValueError("Error: La meta debe ser mayor a la posición inicial.")

        if inicio_seguro < 1:
            raise ValueError("Error: La posición inicial debe ser al menos 1.")

        self.estado_inicial = (inicio_seguro, meta_segura)
        self.meta = meta_segura

    def acciones(self, estado):
        posicion_actual, meta = estado
        acciones = []

        if posicion_actual < meta:
            acciones.append("A pie")

        if (posicion_actual * 2) <= meta:
            acciones.append("Camion magico")

        return acciones

    def sucesor(self, estado, accion):
        posicion_actual, meta = estado

        if accion == 'A pie':
            return (posicion_actual + 1, meta), 1

        if accion == 'Camion magico':
            return (posicion_actual * 2, meta), 2

        raise ValueError(f"Accion no válida: {accion}")

    def terminal(self, estado):
        posicion_actual, meta = estado
        return posicion_actual == meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        posicion_actual, meta = estado
        return f"Posicion actual: {posicion_actual} | Meta: {meta}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    x, meta = nodo.estado

    h_caminar = meta - x

    x_temp = x
    costo = 0

    while x_temp * 2 <= meta:
        x_temp *= 2
        costo += 2

    costo += (meta - x_temp)

    return min(h_caminar, costo)

    """
    Justificación:
    La heurística estima el costo restante considerando dos escenarios: caminar toda la distancia hasta la meta o seguir 
    un plan en el que se usa el camión mágico mientras sea posible y luego se camina lo que falta, entonces, al tomar 
    el menor de ambos valores, se obtiene una estimación del tiempo mínimo bajo condiciones ideales.
    
    ¿Por qué es admisible?
    La política de las heurísticas se basa en que no sobreestime el costo real mínimo, y en ambas estimaciones son cotas
    inferiores al costo real: caminar nunca sobreestima y el plan con camión asume decisiones perfectas, por ende, como
    se toma el mínimo entre ellas, el valor resultante nunca supera el costo óptimo, por lo que no sobreestima.
    """


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

    x, meta = nodo.estado
    return (meta - x) // max(1, x)

    """
        Justificación:
        En esta heurística se piensa que mientras mas grande es x menos acciones faltan, es decir, estima cuántos 
        avances grandes, faltan para llegar a la meta, ya que, cuando la posicion es grande el camión hace que
        avance mas rápido, por lo tanto, los pasos disminuyen. La división calcula una aproximación
        del número mínimo de acciones necesarias.
        

        ¿Por qué es admisible?
        Porque solo toma en cuenta una proporción de la distancia restante e ignora dar pasos innecesarios entonces
        nunca sobreestima el tiempo para llegar a la meta haciendo que el valor calculado sea menor o igual al costo 
        real en todos los casos
        """

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
        self.meta = (0,)*9 + (1,)*9 + (2,)*9 + (3,)*9 + (4,)*9 + (5,)*9
        self.estado_inicial = estado_inicial if estado_inicial else self.meta

        caras = ['Arriba', 'Abajo', 'Izq', 'Der', 'Frente', 'Atras']
        self.accioneslegales = [c + d for c in caras for d in ('', '_Inv')]

        base = list(range(54))

        self.permutaciones = {}

        #SI ES HACIA ARRIBA
        p_arr = base.copy()
        p_arr[0], p_arr[1], p_arr[2], p_arr[5], p_arr[8], p_arr[7], p_arr[6], p_arr[3] = 6, 3, 0, 1, 2, 5, 8, 7
        p_arr[9:12], p_arr[36:39], p_arr[27:30], p_arr[18:21] = base[18:21], base[9:12], base[36:39], base[27:30]

        #SI ES HACIA ABAJO
        p_aba = base.copy()
        p_aba[45], p_aba[46], p_aba[47], p_aba[50], p_aba[53], p_aba[52], p_aba[51], p_aba[48] = 51, 48, 45, 46, 47, 50, 53, 52
        p_aba[15:18], p_aba[24:27], p_aba[33:36], p_aba[42:45] = base[42:45], base[15:18], base[24:27], base[33:36]

        #SI ES HACIA EL FRENTE
        p_fre = base.copy()
        p_fre[18], p_fre[19], p_fre[20], p_fre[23], p_fre[26], p_fre[25], p_fre[24], p_fre[21] = 24, 21, 18, 19, 20, 23, 26, 25
        p_fre[6], p_fre[7], p_fre[8], p_fre[27], p_fre[30], p_fre[33], p_fre[47], p_fre[46], p_fre[45], p_fre[17], p_fre[14], p_fre[11] = \
            17, 14, 11, 6, 7, 8, 27, 30, 33, 47, 46, 45

        #SI ES HACIA LA IZQUIERDA
        p_izq = base.copy()
        p_izq[9], p_izq[10], p_izq[11], p_izq[14], p_izq[17], p_izq[16], p_izq[15], p_izq[12] = 15, 12, 9, 10, 11, 14, 17, 16
        p_izq[0], p_izq[3], p_izq[6], p_izq[18], p_izq[21], p_izq[24], p_izq[45], p_izq[48], p_izq[51], p_izq[44], p_izq[41], p_izq[38] = \
            44, 41, 38, 0, 3, 6, 18, 21, 24, 45, 48, 51

        #SI ES HACIA LA DERECHA
        p_der = base.copy()
        p_der[27], p_der[28], p_der[29], p_der[32], p_der[35], p_der[34], p_der[33], p_der[30] = 33, 30, 27, 28, 29, 32, 35, 34
        p_der[2], p_der[5], p_der[8], p_der[42], p_der[39], p_der[36], p_der[47], p_der[50], p_der[53], p_der[20], p_der[23], p_der[26] = \
            20, 23, 26, 2, 5, 8, 42, 39, 36, 47, 50, 53

        #SI ES HACIA ATRAS
        p_atr = base.copy()
        p_atr[36], p_atr[37], p_atr[38], p_atr[41], p_atr[44], p_atr[43], p_atr[42], p_atr[39] = 42, 39, 36, 37, 38, 41, 44, 43
        p_atr[2], p_atr[1], p_atr[0], p_atr[9], p_atr[12], p_atr[15], p_atr[51], p_atr[52], p_atr[53], p_atr[35], p_atr[32], p_atr[29] = \
            35, 32, 29, 2, 1, 0, 9, 12, 15, 51, 52, 53

        giros = {
            'Arriba': tuple(p_arr),
            'Abajo': tuple(p_aba),
            'Frente': tuple(p_fre),
            'Izq': tuple(p_izq),
            'Der': tuple(p_der),
            'Atras': tuple(p_atr)
        }

        for accion, perm in giros.items():
            self.permutaciones[accion] = perm
            p2 = tuple(perm[i] for i in perm)
            p3 = tuple(p2[i] for i in perm)
            self.permutaciones[accion + '_Inv'] = p3

    def acciones(self, estado):
        return self.accioneslegales

    def sucesor(self, estado, accion):
        permutacion = self.permutaciones[accion]
        nuevo_estado = tuple(estado[i] for i in permutacion)
        return nuevo_estado, 1

    def terminal(self, estado):
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        e = estado
        return (
            f"          {e[0]} {e[1]} {e[2]}\n"
            f"          {e[3]} {e[4]} {e[5]}\n"
            f"          {e[6]} {e[7]} {e[8]}\n"
            f"{e[9]} {e[10]} {e[11]}   {e[18]} {e[19]} {e[20]}   {e[27]} {e[28]} {e[29]}   {e[36]} {e[37]} {e[38]}\n"
            f"{e[12]} {e[13]} {e[14]}   {e[21]} {e[22]} {e[23]}   {e[30]} {e[31]} {e[32]}   {e[39]} {e[40]} {e[41]}\n"
            f"{e[15]} {e[16]} {e[17]}   {e[24]} {e[25]} {e[26]}   {e[33]} {e[34]} {e[35]}   {e[42]} {e[43]} {e[44]}\n"
            f"          {e[45]} {e[46]} {e[47]}\n"
            f"          {e[48]} {e[49]} {e[50]}\n"
            f"          {e[51]} {e[52]} {e[53]}\n"
        )
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE


    Justificación:
    Primero que nada, revisamos las 6 caras del cubo, después buscamos la cara que tenga la mayor cantidad
    de cuadritos fuera de su color. Y al girarlo 90 grados movería 8 de sus cuadritos ya que el centro se
    queda fijo

    ¿Por qué es admisible?
    Porque por ejemplo, si la cara que está más desordenada tiene 8 piezas en posiciones incorrectas, podemos
    asumir que al menos se requerirá 1 movimiento para acomodarla. Al tomar el mayor número de errores y dividirlo
    entre 8 nos aseguramos de que la estimación nunca exceda la cantidad real de giros necesarios para corregir esa
    cara, por ende, tampoco se estará sobreestimando el costo total para resolver el cubo.

    """
    estado = nodo.estado
    meta = (0,) * 9 + (1,) * 9 + (2,) * 9 + (3,) * 9 + (4,) * 9 + (5,) * 9

    max_error = 0

    for i in range(0, 54, 9):
        # Contamos cuántas estampas están mal solo en este bloque
        error_cara = sum(1 for j in range(i, i + 9) if estado[j] != meta[j])
        if error_cara > max_error:
            max_error = error_cara

    return (max_error + 7) // 8


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_problema_1(nodo):
    """

    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Justificación:
    Una cara resuelta debe tener exactamente 1 color. Si tiene más de uno, los demás colores no deberían de pertenecer
    ahí, entonces, esta heurística suma todos los colores extra que hay en las 6 caras, al girarlo 90 grados sabemos
    que podrá desplazar grupos de colores entre 4 caras adyacentes al mismo tiempo, por ende, podríamos asumir que con
    un solo giro perfecto podría eliminar hasta 4 colores no pertencientes a esa cara de golpe.

    ¿Por qué es admisible?
    Al contar los colores sobrantes totales y dividirlos entre 4 (el máximo de caras adyacentes que limpiamos en un
    turno ideal, redondeando hacia arriba), obtenemos un límite inferior estricto, por ende, la estimación jamás será
    mayor que los movimientos reales requeridos.

    Análisis de Dominancia:
    Esta heurística (h2) tiende a ser dominante sobre h1 en la mayoría de los estados, ya que, h1 solo evalúa la peor
    cara e ignora el resto del cubo, arrojando valores muy bajos, en cambio, h2 evalúa el desorden global de todas las
    caras, entonces al sumar los errores del cubo, h2 arroja valores heurísticos más altos y más cercanos al
    costo real, lo que permite al algoritmo A* podar más ramas del árbol y visitar menos nodos que h1.

    """
    estado = nodo.estado

    colores_sobrantes = 0

    for i in range(0, 54, 9):
        cara = estado[i:i + 9]
        colores_unicos = len(set(cara))
        if colores_unicos > 1:
            colores_sobrantes += (colores_unicos - 1)

    return (colores_sobrantes + 3) // 4


def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1, visitados1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2, visitados2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18)
          + str(visitados1).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(visitados2).center(20))
    print('-' * 50 + '\n')


def imprimirpasos(nodosol):
    if nodosol is None:
        print("No se encontró solución.")
        return

    pasos = []
    nodo_actual = nodosol

    while nodo_actual is not None:
        pasos.append(nodo_actual)
        nodo_actual = nodo_actual.padre

    pasos.reverse()
    print(f"\nCubo resuelto en {len(pasos) - 1} movimientos\n")

    for i, nodo in enumerate(pasos):
        if i == 0:
            print("--- ESTADO INICIAL (REVUELTO) ---")
        else:
            print(f"--- PASO {i}: Se aplicó el giro: {nodo.accion} ---")
        print(PbCuboRubik.bonito(nodo.estado))

if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    print("--------------- Camioncito mágico ----------------")
    pos_inicial = (1,50) # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico(pos_inicial=1, meta=50)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)

    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    print("\n" + "*" * 50)
    print("\n------------------ Cubo de Rubik -----------------")
    problemarubik = PbCuboRubik()
    movimientos_mezcla = ['Arriba', 'Der', 'Frente']
    estado_actual = problemarubik.meta

    for mov in movimientos_mezcla:
        estado_actual, _ = problemarubik.sucesor(estado_actual, mov)
    pos_inicial_rubik = estado_actual

    print(f"\nDesordenando el cubo con los siguientes movimientos: {movimientos_mezcla}")
    solucion, _ = busquedas.busqueda_A_estrella(problemarubik, h_1_problema_1, pos_inicial_rubik)
    imprimirpasos(solucion)

    print("\nCorrida:")
    compara_metodos(problemarubik, pos_inicial_rubik, h_1_problema_1, h_2_problema_1)
    