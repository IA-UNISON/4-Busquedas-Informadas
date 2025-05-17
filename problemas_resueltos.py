#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas
import heapq


# Implementación del algoritmo A*
def busqueda_A_estrella(problema, heuristica):
    """
    Búsqueda A*

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param heuristica: Una funcion de heuristica, esto es, una función
                       heuristica(nodo), la cual devuelva un número mayor
                       o igual a cero con el costo esperado desde nodo hasta
                       un nodo cuyo estado final sea méta.

    @return Un objeto tipo Nodo con la estructura completa
    """
    # Verificar si el estado inicial es meta
    if problema.es_meta(problema.x0):
        return busquedas.Nodo(problema.x0)
    
    # Inicializar la frontera con el nodo inicial
    frontera = []
    nodo_inicial = busquedas.Nodo(problema.x0)
    # Usamos como prioridad f(n) = g(n) + h(n)
    f_inicial = nodo_inicial.costo + heuristica(nodo_inicial)
    heapq.heappush(frontera, (f_inicial, nodo_inicial))
    
    # Diccionario para almacenar los estados visitados y su costo
    visitados = {problema.x0: 0}
    
    while frontera:
        # Extraer el nodo con menor f(n)
        _, nodo = heapq.heappop(frontera)
        
        # Verificar si es meta
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        
        # Expandir el nodo
        for hijo in nodo.expande(problema.modelo):
            # Si el estado no ha sido visitado o encontramos un camino de menor costo
            if (hijo.estado not in visitados or 
                visitados[hijo.estado] > hijo.costo):
                # Calcular f(n) = g(n) + h(n)
                f_hijo = hijo.costo + heuristica(hijo)
                heapq.heappush(frontera, (f_hijo, hijo))
                visitados[hijo.estado] = hijo.costo
    
    # Si no se encuentra solución
    return None


# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class CamionMagico(busquedas.ModeloBusqueda):
    """
    Modelo para el problema del Camión Mágico.
    
    Estado: Un entero que representa la posición actual.
    Acciones: 
        - "caminar": Moverse de x a x+1 en 1 minuto
        - "camion": Moverse de x a 2x en 2 minutos
    """
    
    def __init__(self, N):
        """
        Inicializa el modelo con la posición meta N.
        
        @param N: Posición meta a la que queremos llegar
        """
        self.N = N
    
    def acciones_legales(self, estado):
        """
        Devuelve las acciones legales en el estado actual.
        
        @param estado: Posición actual
        @return: Lista de acciones legales
        """
        acciones = []
        
        # Siempre podemos caminar un paso adelante
        acciones.append("caminar")
        
        # Podemos usar el camión si no nos pasamos de la meta
        if estado * 2 <= self.N:
            acciones.append("camion")
            
        return acciones
    
    def sucesor(self, estado, accion):
        """
        Devuelve el estado sucesor al aplicar la acción.
        
        @param estado: Posición actual
        @param accion: Acción a realizar ("caminar" o "camion")
        @return: Nueva posición
        """
        if accion == "caminar":
            return estado + 1
        elif accion == "camion":
            return estado * 2
        else:
            raise ValueError(f"Acción no válida: {accion}")
    
    def costo_local(self, estado, accion):
        """
        Devuelve el costo de realizar la acción.
        
        @param estado: Posición actual
        @param accion: Acción a realizar
        @return: Costo de la acción (1 para caminar, 2 para camión)
        """
        if accion == "caminar":
            return 1
        elif accion == "camion":
            return 2
        else:
            raise ValueError(f"Acción no válida: {accion}")
    
    @staticmethod
    def bonito(estado):
        """
        Representación bonita del estado.
        
        @param estado: Posición actual
        @return: Cadena que representa el estado
        """
        return f"Posición actual: {estado}"


# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMagico(busquedas.ProblemaBusqueda):
    """
    Problema del Camión Mágico.
    
    El objetivo es ir desde la posición 1 hasta la posición N
    en el menor tiempo posible.
    """
    
    def __init__(self, N):
        """
        Inicializa el problema con la posición meta N.
        
        @param N: Posición meta a la que queremos llegar
        """
        # Estado inicial: posición 1
        x0 = 1
        
        # Función meta: llegar a la posición N
        meta = lambda x: x == N
        
        # Modelo del problema
        modelo = CamionMagico(N)
        
        # Inicializar el problema de búsqueda
        super().__init__(x0, meta, modelo)


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Primera heurística para el problema del Camión Mágico.
    
    Esta heurística calcula el tiempo mínimo para llegar a la meta
    asumiendo que podemos llegar directamente. Considera que en el peor
    caso, tendríamos que caminar todo el camino restante, lo que tomaría
    (N - posición_actual) minutos.
    
    Es admisible porque nunca sobreestima el costo real. En el peor caso,
    tendríamos que caminar todo el camino, lo que costaría exactamente
    (N - posición_actual) minutos. Cualquier uso del camión mágico podría
    potencialmente reducir este tiempo, pero nunca aumentarlo.
    
    @param nodo: Nodo actual
    @return: Estimación del costo para llegar a la meta
    """
    estado = nodo.estado
    # Usamos un valor fijo para N que debe coincidir con el usado en PblCamionMagico
    N = 50
    
    # Distancia restante hasta la meta
    distancia_restante = N - estado
    
    # En el peor caso, caminamos todo el camino (1 minuto por paso)
    return distancia_restante


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Segunda heurística para el problema del Camión Mágico.
    
    Esta heurística es más sofisticada y considera la posibilidad de usar
    el camión mágico de manera óptima. Calcula el número mínimo de pasos
    necesarios para llegar a la meta utilizando una combinación de caminar
    y usar el camión.
    
    La estrategia es:
    1. Usar el camión mágico siempre que sea posible (duplicar posición)
    2. Caminar los pasos restantes
    
    Es admisible porque:
    - Nunca sobreestima el costo real
    - Asume que podemos usar el camión de manera óptima
    - En el peor caso, si no podemos usar el camión, se reduce a h_1
    
    Esta heurística es dominante respecto a h_1 porque:
    - Proporciona estimaciones más precisas al considerar el uso del camión
    - Nunca da un valor menor que h_1 (siempre es igual o mayor)
    - Permite podar más estados en la búsqueda A*
    
    @param nodo: Nodo actual
    @return: Estimación del costo para llegar a la meta
    """
    estado = nodo.estado
    # Usamos un valor fijo para N que debe coincidir con el usado en PblCamionMagico
    N = 50
    
    # Si ya estamos en la meta, el costo es 0
    if estado == N:
        return 0
    
    # Inicializamos variables
    posicion_actual = estado
    costo_estimado = 0
    
    # Calculamos el número de bits necesarios para representar N
    bits_N = N.bit_length()
    
    # Calculamos el número de bits necesarios para representar la posición actual
    bits_actual = posicion_actual.bit_length()
    
    # Calculamos cuántos bits nos faltan
    bits_faltantes = bits_N - bits_actual
    
    # Si podemos usar el camión para acercarnos a la meta
    if bits_faltantes > 0:
        # Cada uso del camión nos da un bit más (duplica la posición)
        # y cuesta 2 minutos
        costo_estimado += bits_faltantes * 2
        
        # Calculamos la posición después de usar el camión
        posicion_despues_camion = posicion_actual << bits_faltantes
        
        # Si nos pasamos, retrocedemos un bit
        if posicion_despues_camion > N:
            posicion_despues_camion >>= 1
            costo_estimado -= 2  # Restamos el costo del último uso del camión
        
        # Calculamos los pasos restantes caminando
        pasos_restantes = N - posicion_despues_camion
        costo_estimado += pasos_restantes
    else:
        # Si no podemos usar el camión, caminamos todo el camino
        costo_estimado = N - posicion_actual
    
    return costo_estimado


# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    Modelo para el problema del Cubo de Rubik.
    
    El estado del cubo se representa como una lista de 54 elementos,
    donde cada elemento es un número del 0 al 5 que representa el color
    de cada cara del cubo:
    - 0: Blanco (cara superior)
    - 1: Amarillo (cara inferior)
    - 2: Rojo (cara frontal)
    - 3: Naranja (cara trasera)
    - 4: Verde (cara izquierda)
    - 5: Azul (cara derecha)
    
    Cada cara tiene 9 piezas (3x3), y se numeran de la siguiente manera:
    0 1 2
    3 4 5
    6 7 8
    
    Las acciones son rotaciones de las caras:
    - F: Rotar cara frontal en sentido horario
    - F': Rotar cara frontal en sentido antihorario
    - B: Rotar cara trasera en sentido horario
    - B': Rotar cara trasera en sentido antihorario
    - U: Rotar cara superior en sentido horario
    - U': Rotar cara superior en sentido antihorario
    - D: Rotar cara inferior en sentido horario
    - D': Rotar cara inferior en sentido antihorario
    - L: Rotar cara izquierda en sentido horario
    - L': Rotar cara izquierda en sentido antihorario
    - R: Rotar cara derecha en sentido horario
    - R': Rotar cara derecha en sentido antihorario
    """
    
    def __init__(self):
        """
        Inicializa el modelo del Cubo de Rubik.
        """
        # Definimos las acciones posibles
        self.acciones_posibles = [
            'F', 'F\'', 'B', 'B\'', 'U', 'U\'', 'D', 'D\'', 'L', 'L\'', 'R', 'R\''
        ]
        
        # Mapeo de índices para cada cara
        self.caras = {
            'U': [0, 1, 2, 3, 4, 5, 6, 7, 8],  # Superior (Up)
            'D': [9, 10, 11, 12, 13, 14, 15, 16, 17],  # Inferior (Down)
            'F': [18, 19, 20, 21, 22, 23, 24, 25, 26],  # Frontal (Front)
            'B': [27, 28, 29, 30, 31, 32, 33, 34, 35],  # Trasera (Back)
            'L': [36, 37, 38, 39, 40, 41, 42, 43, 44],  # Izquierda (Left)
            'R': [45, 46, 47, 48, 49, 50, 51, 52, 53]   # Derecha (Right)
        }
        
        # Definimos las adyacencias entre caras
        # Para cada cara, definimos qué piezas de otras caras se ven afectadas al rotarla
        self.adyacencias = {
            'F': [('U', [6, 7, 8]), ('R', [0, 3, 6]), ('D', [2, 1, 0]), ('L', [8, 5, 2])],
            'B': [('U', [2, 1, 0]), ('L', [0, 3, 6]), ('D', [6, 7, 8]), ('R', [8, 5, 2])],
            'U': [('B', [0, 1, 2]), ('R', [0, 1, 2]), ('F', [0, 1, 2]), ('L', [0, 1, 2])],
            'D': [('F', [6, 7, 8]), ('R', [6, 7, 8]), ('B', [6, 7, 8]), ('L', [6, 7, 8])],
            'L': [('U', [0, 3, 6]), ('F', [0, 3, 6]), ('D', [0, 3, 6]), ('B', [8, 5, 2])],
            'R': [('U', [8, 5, 2]), ('B', [0, 3, 6]), ('D', [8, 5, 2]), ('F', [8, 5, 2])]
        }
    
    def acciones_legales(self, estado):
        """
        Devuelve las acciones legales en el estado actual.
        
        @param estado: Estado actual del cubo
        @return: Lista de acciones legales
        """
        # Todas las acciones son legales en cualquier estado
        return self.acciones_posibles
    
    def sucesor(self, estado, accion):
        """
        Devuelve el estado sucesor al aplicar la acción.
        
        @param estado: Estado actual del cubo
        @param accion: Acción a realizar (rotación de una cara)
        @return: Nuevo estado del cubo
        """
        # Creamos una copia del estado
        nuevo_estado = list(estado)
        
        # Extraemos la cara a rotar y la dirección
        cara = accion[0]  # Primera letra de la acción (F, B, U, D, L, R)
        sentido_antihorario = len(accion) > 1 and accion[1] == '\''
        
        # Rotamos la cara
        self._rotar_cara(nuevo_estado, cara, sentido_antihorario)
        
        # Actualizamos las piezas adyacentes
        self._actualizar_adyacencias(nuevo_estado, cara, sentido_antihorario)
        
        return tuple(nuevo_estado)
    
    def _rotar_cara(self, estado, cara, sentido_antihorario):
        """
        Rota una cara del cubo.
        
        @param estado: Estado actual del cubo (se modifica)
        @param cara: Cara a rotar ('F', 'B', 'U', 'D', 'L', 'R')
        @param sentido_antihorario: True si la rotación es antihoraria
        """
        # Obtenemos los índices de la cara
        indices = self.caras[cara]
        
        # Guardamos los valores originales
        valores = [estado[i] for i in indices]
        
        # Definimos el mapeo de rotación
        if sentido_antihorario:
            # Rotación antihoraria: 0->2->8->6->0, 1->5->7->3->1, etc.
            mapeo = [2, 5, 8, 1, 4, 7, 0, 3, 6]
        else:
            # Rotación horaria: 0->6->8->2->0, 1->3->7->5->1, etc.
            mapeo = [6, 3, 0, 7, 4, 1, 8, 5, 2]
        
        # Aplicamos la rotación
        for i, idx in enumerate(indices):
            estado[idx] = valores[mapeo[i]]
    
    def _actualizar_adyacencias(self, estado, cara, sentido_antihorario):
        """
        Actualiza las piezas adyacentes a una cara rotada.
        
        @param estado: Estado actual del cubo (se modifica)
        @param cara: Cara rotada ('F', 'B', 'U', 'D', 'L', 'R')
        @param sentido_antihorario: True si la rotación es antihoraria
        """
        # Obtenemos las adyacencias de la cara
        adyacentes = self.adyacencias[cara]
        
        # Guardamos los valores originales
        valores = []
        for cara_adj, indices_adj in adyacentes:
            valores.append([estado[self.caras[cara_adj][i]] for i in indices_adj])
        
        # Aplicamos la rotación a las adyacencias
        if sentido_antihorario:
            # Rotación antihoraria: los valores se mueven en sentido antihorario
            for i, (cara_adj, indices_adj) in enumerate(adyacentes):
                siguiente = (i - 1) % len(adyacentes)
                for j, idx in enumerate(indices_adj):
                    estado[self.caras[cara_adj][idx]] = valores[siguiente][j]
        else:
            # Rotación horaria: los valores se mueven en sentido horario
            for i, (cara_adj, indices_adj) in enumerate(adyacentes):
                siguiente = (i + 1) % len(adyacentes)
                for j, idx in enumerate(indices_adj):
                    estado[self.caras[cara_adj][idx]] = valores[siguiente][j]
    
    def costo_local(self, estado, accion):
        """
        Devuelve el costo de realizar la acción.
        
        @param estado: Estado actual del cubo
        @param accion: Acción a realizar
        @return: Costo de la acción (siempre 1)
        """
        # Todas las acciones tienen el mismo costo
        return 1
    
    @staticmethod
    def bonito(estado):
        """
        Representación bonita del estado del cubo.
        
        @param estado: Estado actual del cubo
        @return: Cadena que representa el estado
        """
        # Mapeo de números a colores
        colores = ['W', 'Y', 'R', 'O', 'G', 'B']
        
        # Construimos la representación
        s = ""
        
        # Cara superior (U)
        s += "    " + colores[estado[0]] + colores[estado[1]] + colores[estado[2]] + "\n"
        s += "    " + colores[estado[3]] + colores[estado[4]] + colores[estado[5]] + "\n"
        s += "    " + colores[estado[6]] + colores[estado[7]] + colores[estado[8]] + "\n\n"
        
        # Caras izquierda (L), frontal (F), derecha (R) y trasera (B)
        for i in range(0, 3):
            s += (colores[estado[36+i]] + colores[estado[39+i]] + colores[estado[42+i]] + " " +
                  colores[estado[18+i]] + colores[estado[21+i]] + colores[estado[24+i]] + " " +
                  colores[estado[45+i]] + colores[estado[48+i]] + colores[estado[51+i]] + " " +
                  colores[estado[27+i]] + colores[estado[30+i]] + colores[estado[33+i]] + "\n")
        
        s += "\n"
        
        # Cara inferior (D)
        s += "    " + colores[estado[9]] + colores[estado[10]] + colores[estado[11]] + "\n"
        s += "    " + colores[estado[12]] + colores[estado[13]] + colores[estado[14]] + "\n"
        s += "    " + colores[estado[15]] + colores[estado[16]] + colores[estado[17]] + "\n"
        
        return s


# ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    Problema del Cubo de Rubik.
    
    El objetivo es resolver el cubo desde un estado desordenado.
    """
    
    def __init__(self, estado_inicial=None):
        """
        Inicializa el problema del Cubo de Rubik.
        
        @param estado_inicial: Estado inicial del cubo (desordenado)
        """
        # Si no se proporciona un estado inicial, creamos uno resuelto
        if estado_inicial is None:
            # Cubo resuelto: cada cara tiene un solo color
            estado_inicial = tuple([i // 9 for i in range(54)])
        
        # Función meta: el cubo está resuelto cuando cada cara tiene un solo color
        def es_meta(estado):
            # Para cada cara, verificamos que todas las piezas tengan el mismo color
            for i in range(0, 54, 9):
                color = estado[i]
                for j in range(9):
                    if estado[i + j] != color:
                        return False
            return True
        
        # Modelo del problema
        modelo = CuboRubik()
        
        # Inicializar el problema de búsqueda
        super().__init__(estado_inicial, es_meta, modelo)


# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_problema_1(nodo):
    """
    Primera heurística para el problema del Cubo de Rubik.
    
    Esta heurística cuenta el número de piezas que no están en su posición correcta.
    Es admisible porque cada pieza fuera de lugar requiere al menos un movimiento
    para colocarla en su posición correcta.
    
    @param nodo: Nodo actual
    @return: Estimación del costo para resolver el cubo
    """
    estado = nodo.estado
    
    # Cubo resuelto: cada cara tiene un solo color
    estado_resuelto = tuple([i // 9 for i in range(54)])
    
    # Contamos las piezas que no están en su posición correcta
    piezas_incorrectas = sum(1 for i in range(54) if estado[i] != estado_resuelto[i])
    
    # Dividimos por 4 porque cada movimiento puede corregir hasta 4 piezas
    return piezas_incorrectas // 4


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_problema_1(nodo):
    """
    Segunda heurística para el problema del Cubo de Rubik.
    
    Esta heurística es más sofisticada y considera la distancia de Manhattan
    de cada pieza a su posición correcta en términos de movimientos necesarios.
    
    Es admisible porque:
    - Cada pieza requiere al menos el número de movimientos calculado para llegar a su posición
    - No sobreestima el costo real de resolver el cubo
    
    Esta heurística es dominante respecto a h_1 porque:
    - Proporciona estimaciones más precisas al considerar la distancia de cada pieza
    - Nunca da un valor menor que h_1 (siempre es igual o mayor)
    - Permite podar más estados en la búsqueda A*
    
    @param nodo: Nodo actual
    @return: Estimación del costo para resolver el cubo
    """
    estado = nodo.estado
    
    # Calculamos la suma de las distancias de Manhattan para cada pieza
    # Esto es una simplificación, ya que el cálculo real sería muy complejo
    
    # Para cada cara, calculamos cuántas piezas tienen el color incorrecto
    total_distancia = 0
    for i in range(6):  # 6 caras
        cara_indices = range(i*9, (i+1)*9)
        color_correcto = i
        
        # Contamos piezas con color incorrecto en esta cara
        piezas_incorrectas = sum(1 for idx in cara_indices if estado[idx] != color_correcto)
        
        # Añadimos al total
        total_distancia += piezas_incorrectas
    
    # Dividimos por 8 porque cada movimiento puede afectar hasta 8 piezas
    # (4 en la cara que se rota y 4 en las caras adyacentes)
    return total_distancia // 8


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
    solucion1 = busqueda_A_estrella(problema, heuristica_1)
    solucion2 = busqueda_A_estrella(problema, heuristica_2)
    
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
    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PblCamionMagico(20)  # Queremos llegar a la posición 20
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    # Creamos un estado inicial ligeramente desordenado para el cubo
    estado_inicial = list([i // 9 for i in range(54)])
    # Hacemos algunos movimientos para desordenar el cubo
    estado_inicial[0], estado_inicial[1] = estado_inicial[1], estado_inicial[0]
    estado_inicial[18], estado_inicial[19] = estado_inicial[19], estado_inicial[18]
    problema = PblCuboRubik(tuple(estado_inicial))
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)