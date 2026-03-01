#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import math
import busquedas



# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    Problema del Camión Mágico.

    Nos queremos trasladar desde la posición discreta 1 hasta la posición
    discreta N en una vía recta. Tenemos dos formas de movernos:

      1. A pie: del punto x al punto x + 1, con costo de 1 minuto.
      2. En camión mágico: del punto x al punto 2x, con costo de 2 minutos.

    El estado es un entero x >= 1 que indica la posición actual.
    La meta es llegar a la posición N.

    """
    def __init__(self, meta=100):
        """
        Inicializa el problema del camión mágico.

        Aquí simplemente guardo la posición a la que quiero llegar.
        El estado es un entero (mi posición en la recta).

        @param meta: int, la posición objetivo N (por defecto 100).

        """
        self.meta = int(meta)

    def acciones(self, estado):
        """
        Devuelve las acciones legales desde la posición x.

        Desde la posición x tengo dos opciones:
        - 'A' (a pie): avanzar a x+1, siempre que no me haya pasado de la meta.
        - 'C' (camión): saltar a 2x, pero solo si 2x no se pasa de la meta.

        @param estado: int, la posición actual x.
        @return: list, lista de acciones legales ('A' y/o 'C').

        """
        x = estado
        acciones = []
        if x < self.meta:
            acciones.append('A')
        if 2 * x <= self.meta:
            acciones.append('C')
        return acciones

    def sucesor(self, estado, accion):
        """
        Calcula el estado sucesor y el costo de aplicar una acción.

        - Si camino ('A'), paso de x a x+1 y me tardo 1 minuto.
        - Si tomo el camión ('C'), paso de x a 2x y me tardo 2 minutos.

        @param estado: int, la posición actual x.
        @param accion: str, 'A' para caminar o 'C' para el camión.
        @return: tuple (estado_sucesor, costo_local).

        """
        x = estado
        if accion == 'A':
            return x + 1, 1
        if accion == 'C':
            return 2 * x, 2
        raise ValueError(f"Acción desconocida: {accion}")

    def terminal(self, estado):
        """
        Revisa si ya llegué a la posición meta.

        @param estado: int, la posición actual.
        @return: bool, True si estado == meta.

        """
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        Representación bonita del estado.

        @param estado: int, la posición actual.
        @return: str, cadena con la posición.

        """
        return f"Posición actual: {estado}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Primera heurística admisible para el problema del Camión Mágico.

    Mi idea es contar el mínimo de pasos que necesito para llegar de x a N,
    suponiendo que cada paso me duplica la posición (que es lo mejor que
    puedo hacer). Eso me da ceil(log2(N/x)).

    Creo que es admisible porque estoy asumiendo el mejor caso posible:
    que cada acción me duplica la posición y solo me cuesta 1. En la
    realidad el camión cuesta 2 y caminar solo suma 1, así que el costo
    real siempre va a ser mayor o igual a este valor. Nunca sobreestimo.

    @param nodo: NodoBusqueda, el nodo actual (nodo.estado es la posición x).
    @return: int, estimación del costo restante desde x hasta N.

    """
    x = nodo.estado
    N = 100
    if x >= N:
        return 0
    return math.ceil(math.log2(N / x))


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Segunda heurística admisible para el problema del Camión Mágico.

    Para esta heurística quise ser más preciso. La idea es la siguiente:
    si uso k viajes en camión y w pasos a pie, lo mejor que puedo hacer es
    caminar primero y luego tomar el camión (porque los pasos a pie se
    multiplican por las duplicaciones del camión). Así, lo máximo que
    alcanzo es (x + w) * 2^k. Para que eso llegue a N, necesito al menos
    w >= ceil(N / 2^k) - x pasos a pie. El costo total sería 2*k + w.
    Pruebo con distintos valores de k y me quedo con el mínimo.

    Es admisible porque estoy calculando el mínimo costo posible asumiendo
    que acomodo los pasos de la mejor manera (todos antes de subir al
    camión), lo cual es más favorable que la realidad. Nunca sobreestimo.

    Creo que domina a h_1 porque esta heurística sí toma en cuenta que el
    camión cuesta 2 minutos (no 1), entonces da valores más altos y más
    cercanos al costo real. En las pruebas se nota: h_2 explora menos nodos.

    @param nodo: NodoBusqueda, el nodo actual (nodo.estado es la posición x).
    @return: int, estimación del costo restante desde x hasta N.

    """
    x = nodo.estado
    N = 100
    if x >= N:
        return 0
    best = N - x
    max_k = int(math.log2(N)) + 1
    for k in range(1, max_k + 1):
        walks = max(0, math.ceil(N / (2 ** k)) - x)
        cost = 2 * k + walks
        if cost < best:
            best = cost
    return best

# ------------------------------------------------------------
#  Cubo de Rubik 3D (3x3x3)
# ------------------------------------------------------------

_MOVIMIENTOS = {
    # U (cara superior, horario visto desde arriba)
    'U': [
        (0, 6, 8, 2), (1, 3, 7, 5),
        (9, 45, 36, 18), (10, 48, 37, 19), (11, 51, 38, 20)
    ],
    # D (cara inferior, horario visto desde abajo)
    'D': [
        (27, 29, 35, 33), (28, 32, 34, 30),
        (18, 36, 45, 15), (19, 39, 46, 16), (20, 42, 47, 17)
    ],
    # F (cara frontal, horario visto desde el frente)
    'F': [
        (18, 24, 26, 20), (19, 21, 25, 23),
        (6, 9, 29, 44), (7, 12, 28, 41), (8, 15, 27, 38)
    ],
    # B (cara trasera, horario visto desde atrás)
    'B': [
        (45, 47, 53, 51), (46, 48, 52, 50),
        (2, 36, 33, 17), (1, 39, 34, 14), (0, 42, 35, 11)
    ],
    # R (cara derecha, horario visto desde la derecha)
    'R': [
        (9, 15, 17, 11), (10, 12, 16, 14),
        (2, 20, 29, 47), (5, 23, 32, 50), (8, 26, 35, 53)
    ],
    # L (cara izquierda, horario visto desde la izquierda)
    'L': [
        (36, 38, 44, 42), (37, 41, 43, 39),
        (0, 27, 45, 18), (3, 30, 48, 21), (6, 33, 51, 24)
    ],
}

# Aquí precalculo las permutaciones completas (arreglos de 54 posiciones)
# para cada movimiento y su inverso, así calcular el sucesor es rápido.

def _ciclos_a_permutacion(ciclos):
    """Convierte la lista de ciclos en una permutación de 54 elementos."""
    perm = list(range(54))
    for ciclo in ciclos:
        if len(ciclo) == 4:
            a, b, c, d = ciclo
            perm[a], perm[b], perm[c], perm[d] = d, a, b, c
    return tuple(perm)

def _inversa_permutacion(perm):
    inv = [0] * 54
    for i, p in enumerate(perm):
        inv[p] = i
    return tuple(inv)

def _aplicar_perm(estado, perm):
    return tuple(estado[perm[i]] for i in range(54))

# Construir tabla de permutaciones
_PERMS = {}
for _nombre, _ciclos in _MOVIMIENTOS.items():
    _p = _ciclos_a_permutacion(_ciclos)
    _PERMS[_nombre] = _p
    _PERMS[_nombre + "'"] = _inversa_permutacion(_p)

_ESTADO_RESUELTO = tuple(
    color for color in range(6) for _ in range(9)
)

_ACCIONES_RUBIK = list(_PERMS.keys())   # 12 movimientos: uno horario y uno antihorario por cada cara


class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    Problema del Cubo de Rubik 3x3x3.

    El estado es una tupla de 54 números (0 a 5), uno por cada cuadrito
    del cubo. Están ordenados por cara: Arriba(0-8), Derecha(9-17),
    Frente(18-26), Abajo(27-35), Izquierda(36-44), Atrás(45-53).
    El cubo está resuelto cuando todos los cuadritos de cada cara
    tienen el mismo color.

    Las acciones son los 12 movimientos posibles: girar cada una de las
    6 caras en sentido horario o antihorario (U, U', D, D', F, F',
    B, B', R, R', L, L'). Cada movimiento cuesta 1.

    """

    def __init__(self, meta=None):
        """
        Inicializa el problema del Cubo de Rubik.

        @param meta: tupla de 54 enteros o None (por defecto, cubo resuelto).
        """
        self.meta = tuple(meta) if meta is not None else _ESTADO_RESUELTO

    def acciones(self, estado):
        """
        Devuelve los 12 movimientos que se pueden hacer.

        @param estado: tupla de 54 enteros.
        @return: lista con las 12 acciones posibles.
        """
        return _ACCIONES_RUBIK

    def sucesor(self, estado, accion):
        """
        Aplica el movimiento al cubo y devuelve el nuevo estado con costo 1.

        @param estado: tupla de 54 enteros.
        @param accion: str, uno de los 12 movimientos.
        @return: (tupla, entero).
        """
        if accion not in _PERMS:
            raise ValueError(f"Acción desconocida: {accion}")
        return _aplicar_perm(estado, _PERMS[accion]), 1

    def terminal(self, estado):
        """
        Revisa si el cubo ya está resuelto.

        @param estado: tupla de 54 enteros.
        @return: bool, True si ya se armó el cubo.
        """
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        Muestra el cubo desplegado como una cruz para que se vea bonito.

                Arriba
        Izq  Frente  Der  Atrás
                Abajo

        @param estado: tupla de 54 enteros.
        @return: str con el dibujo del cubo.
        """
        nombres = ['🟨', '🟥', '🟩', '🟦', '🟧', '⬜']
        c = [nombres[v] for v in estado]
        u = c[0:9]
        r = c[9:18]
        f = c[18:27]
        d = c[27:36]
        l = c[36:45]
        b = c[45:54]
        lineas = []
        for i in range(3):
            lineas.append('      ' + ' '.join(u[3*i:3*i+3]))
        for i in range(3):
            lineas.append(
                ' '.join(l[3*i:3*i+3]) + '  ' +
                ' '.join(f[3*i:3*i+3]) + '  ' +
                ' '.join(r[3*i:3*i+3]) + '  ' +
                ' '.join(b[3*i:3*i+3])
            )
        for i in range(3):
            lineas.append('      ' + ' '.join(d[3*i:3*i+3]))
        return '\n'.join(lineas)


# ------------------------------------------------------------
#  Heurística 1: cuadritos mal puestos / 8
# ------------------------------------------------------------

def h_1_problema_1(nodo):
    """
    Primera heurística admisible para el Cubo de Rubik.

    Lo que hago es contar cuántos cuadritos tienen un color que no
    corresponde a su cara y divido entre 8. Cada movimiento mueve 20
    cuadritos (8 de la cara que giras más 12 de las caras vecinas),
    así que en el mejor caso un solo movimiento podría arreglar hasta
    8 cuadritos mal puestos. Por eso dividir entre 8 nunca da un valor
    mayor al real, o sea que es admisible.

    Los centros de cada cara (posiciones 4, 13, 22, 31, 40, 49) nunca
    se mueven, así que siempre están bien puestos.

    @param nodo: NodoBusqueda, nodo.estado es tupla de 54 enteros.
    @return: int, estimación por abajo del número de movimientos.
    """
    estado = nodo.estado
    meta = _ESTADO_RESUELTO
    mal = sum(1 for i in range(54) if estado[i] != meta[i])
    return math.ceil(mal / 8)


# ------------------------------------------------------------
#  Heurística 2: distancia entre caras de cada cuadrito / 4
# ------------------------------------------------------------
_CARA_DE = [i // 9 for i in range(54)]   # cara a la que pertenece el cuadrito i cuando está resuelto

_DISTANCIA_CARAS = [
    # U  R  F  D  L  B
    [0, 1, 1, 2, 1, 1],  # U
    [1, 0, 1, 1, 2, 1],  # R
    [1, 1, 0, 1, 1, 2],  # F
    [2, 1, 1, 0, 1, 1],  # D
    [1, 2, 1, 1, 0, 1],  # L
    [1, 1, 2, 1, 1, 0],  # B
]

def h_2_problema_1(nodo):
    """
    Segunda heurística admisible para el Cubo de Rubik.

    Para cada cuadrito veo en qué cara está ahorita y en cuál debería
    estar según su color. La distancia entre caras puede ser 0 (es la
    misma cara), 1 (son caras vecinas) o 2 (son caras opuestas). Sumo
    todas esas distancias y divido entre 4, porque un movimiento puede
    acercar a lo mucho 4 cuadritos un paso hacia donde deben ir.

    Esta heurística domina a h_1 porque cuando un cuadrito está en una
    cara opuesta a donde debería estar, aquí cuenta 2, mientras que en
    h_1 solo cuenta 1. Entonces h_2 siempre da valores iguales o más
    altos que h_1, lo que hace que se exploren menos nodos.

    @param nodo: NodoBusqueda, nodo.estado es tupla de 54 enteros.
    @return: int, estimación por abajo del número de movimientos.
    """
    estado = nodo.estado
    total = 0
    for i in range(54):
        cara_actual = _CARA_DE[i]        # cara donde está el cuadrito ahorita
        cara_correcta = estado[i]        # el color dice a qué cara pertenece
        total += _DISTANCIA_CARAS[cara_actual][cara_correcta]
    return math.ceil(total / 4)


# ------------------------------------------------------------
#  Utilidad de comparación
# ------------------------------------------------------------

def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara A* con dos heurísticas distintas.
    """
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)

    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12)
          + str(solucion1.costo).center(18)
          + str(nodos1).center(20))
    print('A* con h2'.center(12)
          + str(solucion2.costo).center(18)
          + str(nodos2).center(20))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    print("=" * 50)
    print("  PROBLEMA DEL CAMIÓN MÁGICO (de 1 a 100)")
    print("=" * 50)
    pos_inicial = 1
    problema = PbCamionMagico(100)
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)

    print("=" * 50)
    print("  PROBLEMA DEL CUBO DE RUBIK 3D (3x3x3)")
    print("=" * 50)
    pb = PbCuboRubik()

    # Aplicamos 4 movimientos para crear un estado inicial revuelto
    movimientos_revuelto = ['F', 'R', 'U', 'L']
    s = _ESTADO_RESUELTO
    for mv in movimientos_revuelto:
        s, _ = pb.sucesor(s, mv)
    pos_inicial = s

    print("Cubo resuelto (meta):")
    print(PbCuboRubik.bonito(_ESTADO_RESUELTO))
    print()
    print(f"Cubo revuelto (estado inicial, después de {' → '.join(movimientos_revuelto)}):")
    print(PbCuboRubik.bonito(pos_inicial))
    print()

    # Comparar heurísticas
    compara_metodos(pb, pos_inicial, h_1_problema_1, h_2_problema_1)

    # Mostrar la solución paso a paso usando h_2 (la mejor heurística)
    print("=" * 50)
    print("  SOLUCIÓN PASO A PASO (A* con h2)")
    print("=" * 50)
    solucion, _ = busquedas.busqueda_A_estrella(pb, pos_inicial, h_2_problema_1)
    plan = solucion.genera_plan()

    for i, (estado, accion, costo) in enumerate(plan):
        if i == 0:
            print(f"Paso 0 — Estado inicial:")
        elif accion is None:
            print(f"Paso {i} — ¡Cubo resuelto! (costo total: {plan[i-1][2]})")
        else:
            print(f"Paso {i} — Movimiento: {accion}  (costo acumulado: {costo})")
        print(PbCuboRubik.bonito(estado))
        print()
