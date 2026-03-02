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
    def __init__(self):
        pass

    def acciones(self, estado):
        posicion, meta = estado
        acciones = []
        if posicion <= meta:
            acciones.append("un paso")

        if posicion * 2 <= meta:
            acciones.append("camion magico")

        return acciones

    def sucesor(self, estado, accion):
        posicion, meta = estado
        if accion == 'un paso':
            estado_sucesor = (posicion + 1, meta)
            costo_local = 1
        elif accion == 'camion magico':
            estado_sucesor = (posicion * 2, meta)
            costo_local = 2

        return estado_sucesor, costo_local

    def terminal(self, estado):
        # Terminamos cuando nuestro estado sea exactamente igual a la meta
        posicion, meta = estado
        return posicion == meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        posicion, meta = estado
        return print(f"Posicion: {posicion} Meta: {meta}")
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Esta heuristica asume un escenario extremadamente optimista, lo que seria un
    problema relajado, simplemente calcula cuantas veces tendriamos que usar el camion magico
    para alcanzar o rebasar la meta, pero imaginando que el camión cuesta solo 1 minuto
    en lugar de 2. Es admisible porque al aplicar este descuento, garantizamos
    matematicamente que la estimacion siempre sera menor o igual al tiempo real
    que tomaria llegar. Es decir, nunca va a sobrestimar el costo.

    """
    estado_actual, meta = nodo.estado
    saltos = 0

    while estado_actual < meta:
        estado_actual *= 2
        saltos += 1

    return saltos

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Como esta heuristica trabaja desde la meta hasta el estado inicial y no
    al reves, no es cuestion de "atinarle" a que movimiento hacer, en cualquier
    momento sabe si usar camion magico (si divisible entre 2) o solo dar
    un paso (cuando no es divisible entre 2).

    """
    estado_actual, meta = nodo.estado
    actual = meta
    costo_estimado = 0

    while actual > estado_actual:
        if actual % 2 == 0 and (actual // 2) >= estado_actual:
            actual = actual // 2
            costo_estimado += 2
        else:
            actual -= 1
            costo_estimado += 1

    return costo_estimado

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    Modelo del Cubo de Rubik.
    Tenemos como estado una tupla de 54 enteros (0 al 5) representando los colores del cubo.
    El orden de las caras seria el siguiente:
    0:Arriba(U), 1:Izquierda(L), 2:Frente(F), 3:Derecha(R), 4:Atras(B), 5:Abajo(D)
    """

    def __init__(self):
        # Generamos dinámicamente la tupla meta, nueve ceroos, nueve unos, etc.
        # Esto crea la tupla de 54 elementos para el cubo resuelto.
        self.meta = tuple([i // 9 for i in range(54)])

        # Las 12 acciones del cubo:
        # Giros de 90 grados en sentido horario (U, D, L, R, F, B)
        # Giros de 90 grados en sentido antihorario (U', D', L', R', F', B')
        self.acciones_posibles = ['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'"]

    def acciones(self, estado):
        # Todas las acciones son legales siempre
        return self.acciones_posibles

    def sucesor(self, estado, accion):
        """
        Calcula el nuevo estado del cubo despues de aplicar un giro.

        Un giro horario de una cara implica dos cosas:
        Rotar los 8 colores de la cara (8 por que el centro no se mueve)
        misma y rotar los 12 cuadritos. son 12 por que tambien se cuentan
        los de los bordes de las 4 caras adyacentes.
        En lugar de programar la logica inversa para los giros antihorarios
        simplemente ejecutamos el giro horario 3 veces.
        """
        s = list(estado)
        costo_local = 1

        # Determina cuantas veces aplicar el giro base
        veces = 3 if "'" in accion else 1
        movimiento_base = accion[0]

        for _ in range(veces):
            if movimiento_base == 'U':
                # cara de arriba
                s[0], s[1], s[2], s[5], s[8], s[7], s[6], s[3] = s[6], s[3], s[0], s[1], s[2], s[5], s[8], s[7]
                # Bordes: F -> L -> B -> R -> F
                s[9:12], s[36:39], s[27:30], s[18:21] = s[18:21], s[9:12], s[36:39], s[27:30]

            elif movimiento_base == 'D':
                # cara de abajo
                s[45], s[46], s[47], s[50], s[53], s[52], s[51], s[48] = s[51], s[48], s[45], s[46], s[47], s[50], s[
                    53], s[52]
                # Bordes: F -> R -> B -> L -> F
                s[15:18], s[24:27], s[33:36], s[42:45] = s[42:45], s[15:18], s[24:27], s[33:36]

            elif movimiento_base == 'F':
                # cara de en frente
                s[18], s[19], s[20], s[23], s[26], s[25], s[24], s[21] = s[24], s[21], s[18], s[19], s[20], s[23], s[
                    26], s[25]
                # Bordes (cruzan filas y columnas): U -> R -> D -> L -> U
                s[6], s[7], s[8], s[27], s[30], s[33], s[47], s[46], s[45], s[17], s[14], s[11] = \
                    s[17], s[14], s[11], s[6], s[7], s[8], s[27], s[30], s[33], s[47], s[46], s[45]

            elif movimiento_base == 'L':
                # cara de la izquierda
                s[9], s[10], s[11], s[14], s[17], s[16], s[15], s[12] = s[15], s[12], s[9], s[10], s[11], s[14], s[17], \
                s[16]
                # Bordes: U -> F -> D -> B -> U
                s[0], s[3], s[6], s[18], s[21], s[24], s[45], s[48], s[51], s[44], s[41], s[38] = \
                    s[44], s[41], s[38], s[0], s[3], s[6], s[18], s[21], s[24], s[45], s[48], s[51]

            elif movimiento_base == 'R':
                # cara de la derecha
                s[27], s[28], s[29], s[32], s[35], s[34], s[33], s[30] = s[33], s[30], s[27], s[28], s[29], s[32], s[
                    35], s[34]
                # Bordes: U -> B -> D -> F -> U
                s[2], s[5], s[8], s[42], s[39], s[36], s[47], s[50], s[53], s[20], s[23], s[26] = \
                    s[20], s[23], s[26], s[2], s[5], s[8], s[42], s[39], s[36], s[47], s[50], s[53]

            elif movimiento_base == 'B':
                # cara trasera
                s[36], s[37], s[38], s[41], s[44], s[43], s[42], s[39] = s[42], s[39], s[36], s[37], s[38], s[41], s[
                    44], s[43]
                # Bordes: U -> L -> D -> R -> U
                s[2], s[1], s[0], s[9], s[12], s[15], s[51], s[52], s[53], s[35], s[32], s[29] = \
                    s[35], s[32], s[29], s[2], s[1], s[0], s[9], s[12], s[15], s[51], s[52], s[53]

        # Convertimos de regreso a tupla
        return tuple(s), costo_local

    def terminal(self, estado):
        # Terminamos cuando nuestro estado sea exactamente igual al cubo resuelto
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        Imprime el cubo "desplegado" en forma de cruz para visualizarlo en la consola.
        """
        s = estado
        res = f"      {s[0]}{s[1]}{s[2]}\n"
        res += f"      {s[3]}{s[4]}{s[5]}\n"
        res += f"      {s[6]}{s[7]}{s[8]}\n"
        res += f"{s[9]}{s[10]}{s[11]} {s[18]}{s[19]}{s[20]} {s[27]}{s[28]}{s[29]} {s[36]}{s[37]}{s[38]}\n"
        res += f"{s[12]}{s[13]}{s[14]} {s[21]}{s[22]}{s[23]} {s[30]}{s[31]}{s[32]} {s[39]}{s[40]}{s[41]}\n"
        res += f"{s[15]}{s[16]}{s[17]} {s[24]}{s[25]}{s[26]} {s[33]}{s[34]}{s[35]} {s[42]}{s[43]}{s[44]}\n"
        res += f"      {s[45]}{s[46]}{s[47]}\n"
        res += f"      {s[48]}{s[49]}{s[50]}\n"
        res += f"      {s[51]}{s[52]}{s[53]}\n"
        return res
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Esta heuristica cuenta cuantas estampas estan fuera de su lugar original.
    Asume un escenario ficticio muy optimista donde un solo giro del cubo 
    pudiera arreglar hasta 24 estampas de golpe. 
    Es admisible porque al asumir que arreglamos mas piezas por turno, 
    siempre subestimara la cantidad de movimientos reales necesarios.
    """
    # generamos la meta perfecta para comparar
    meta = tuple([i // 9 for i in range(54)])

    # contamos cuantos cuadros no coinciden con la meta
    cuadros_mal = sum(1 for i in range(54) if nodo.estado[i] != meta[i])

    # dividimos entre 24, el truco  de (cuadros_mal + 23) // 24 equivale a redondear hacia arriba
    return (cuadros_mal + 23) // 24


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Esta heuristica tambien cuenta las estampas desordenadas, pero usa el 
    limite fisico real del cubo, un giro mueve exactamente 20 cuadros.
    Es admisible porque asume que cada movimiento arreglara el maximo posible 
    de piezas (20), dandonos el costo minimo absoluto de movimientos reales.

    Como esta heuristica usa el limite fisico real (20) en lugar del ficticio (24), 
    su estimacion siempre estara mas cerca del costo verdadero. Por lo tanto, 
    h2 domina a h1, guiando a A* con mayor precision y explorando menos nodos.
    """
    meta = tuple([i // 9 for i in range(54)])
    cuadros_mal = sum(1 for i in range(54) if nodo.estado[i] != meta[i])

    # Dividimos entre 20 (el limite real). Redondeamos hacia arriba.
    return (cuadros_mal + 19) // 20



def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1, nodo1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    solucion2, nodo2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(nodo1))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(nodo2))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    print("\n" + "=" * 50)
    print("=== RESOLVIENDO EL CAMION MAGICO ===")
    pos_inicial = (1, 50)  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico()  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    print("\n" + "=" * 50)
    print("=== RESOLVIENDO EL CUBO RUBIK ===")
    problema = PbCuboRubik()
    # en vez de escribir una tupla giro dos veces el cubo resuelto
    cubo_resuelto = problema.meta
    cubo_revuelto1, _ = problema.sucesor(cubo_resuelto, 'U')
    pos_inicial, _ = problema.sucesor(cubo_revuelto1, 'R')

    compara_metodos(problema, pos_inicial, h_1_problema_1, h_2_problema_1)
    