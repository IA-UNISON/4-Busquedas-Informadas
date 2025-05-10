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
    def __init__(self,meta):
        """
        Inicializa el modelo con una posición meta.
        
        @param meta: Posición final a la que queremos llegar
        
        """
        self.meta = meta

    def acciones_legales(self, estado):
        """
        Determina las acciones legales en un estado dado.
        
        @param estado: Posición actuan en la recta
        @return: Lista de acciones legales
        
        """
        acciones = []
        
        # Siempre podemos caminar a la siguiente posición, pero no nos pasemos de meta
        if estado + 1 <= self.meta:
            acciones.append("me gusta caminar")
        
        # También a veces se me antoja usar el camión mágico (vende cosas cósmicas),
        # pero tampoco debemos pasarnos de meta
        if 2 * estado <= self.meta:
            acciones.append("camion magico cosmico")
        
        return acciones

    def sucesor(self, estado, accion):
        """
        Determina el estado sucesor al aplicar una acción.
        
        @param estado: Posición actual en la línea
        @param accion: Acción al aplicar ('me gusta caminar' o 'camion magico cosmico')
        @return: Nueva posición resultante
        
        """
        if accion == "me gusta caminar":
            return estado + 1
        elif accion == "camion magico cosmico":
            return 2 * estado
        raise ValueError(f"No reconozco esta accion carnal: {accion}")

    def costo_local(self, estado, accion):
        """
        Determina el costo de aplicar una acción en un estado.
        
        @param estado: Posición actual en la línea
        @param accion: Acción a aplicar ('me gusta caminar' o 'camion magico cosmico')
        @return: Costo de la acción (tiempo en minutos)
        
        """
        if accion == "me gusta caminar":
            return 1 # de tu vida
        elif accion == "camion magico cosmico":
            return 2 # de tu vida con todo y papas
        raise ValueError(f"No reconozco esta accion carnal: {accion}")

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posicion: {estado}"
 
# ------------------------------------------------------------
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para ir desde el 
    punto $1$ hasta el punto $N$ en el menor tiempo posible.

    """
    def __init__(self, meta):
        """
        Inicializa el problema del camión mágico.
        
        @param meta: Posición final a la que queremos llegar
        
        """
        # Le echamos leña al modelo
        modelo = CamionMagico(meta)
        
        # Se define la función meta para saber que ya llegue y dormir la neta
        meta_func = lambda estado: estado == meta
        
        # Inicializamos la clase padre
        super().__init__(1, meta_func, modelo)
    

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Heurística basada en el número mínimo de pasos necesarios para
    alcanzar la meta usando una estrategia óptima de duplicación.
    
    Esta heurística es admisible por lo siguiente:
    1. Asumimos que podemos llegar a la meta usando solo operaciones de duplicación
    (camión mágico cósmico) y una cantidad mínima de pasos a pie.
    2. Cada operación de duplicación toma 2 minutos, y cada paso a patín toma 1 minuto.
    3. Nunca sobreestima el costo real porque calcula el mínimo teórico de pasos.
    
    @param nodo: Nodo actual en el árbol de búsqueda
    @return: Estimación del costo mínimo para llegar a la meta

    """
    estado_actual = nodo.estado
    
    # Accedemos a la meta a través del modelo del problema
    meta = nodo.problema.modelo.meta
    
    # Si ya llegamos o nos pasamos de la meta, el costo restante es 0
    if estado_actual >= meta:
        return 0
    
    # Calculamos la diferencia que falta para llegar a la meta
    diferencia = meta - estado_actual
    
    # Una estrategia: usamos el camión mágico cósmico (duplicar) en la medida de lo posible,
    # luego caminamos. Esto nos ayuda a aproximar el costo mínimo
    
    import math
    
    # La potencia de 2 más cercana pero menor o igual a la posición actual
    pot_2 = 2 ** math.floor(math.log2(estado_actual))
    
    # Calculamos cuantas veces me puedo aventar la duplicación para no pasarme
    # la meta por pendejo :C
    pasos_camion = 0
    pos_actual = estado_actual
    
    while pos_actual * 2 <= meta:
        pos_actual *= 2
        pasos_camion += 1
    
    # Y pues para el resto tocó hacer cardio (caminar)
    pasos_pie = meta - pos_actual
    
    # Total: cada paso en el camión mágico cósmico cuesta 2, cada paso a patín cuesta 1
    return pasos_camion * 2 + pasos_pie


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Heurística simplista que estima el costo como la distancia directa a la meta,
    asumiendo que solo caminamos (porque somos bien sanos, osea un paso por minuto).
    
    Esta heurística es admisible por lo siguiente:
    1. Caminar siempre cuesta 1 minuto por paso
    2. En el peor de los casos, podríamos llegar a la meta caminando todo el trayecto.
    3. Cualquier uso del camión mágico cósmico (duplica la posición) nunca empeora este costo.
    
    Esta heurística es menos informada (coloquialmente, ignorante), pero es admisible :D
    
    @param nodo: Nodo actual en el árbol de búsqueda
    @return: Estimación del costo mínimo para llegar a la meta

    """
    estado_actual = nodo.estado
    
    # Accedemos a la meta a través del modelo
    meta = nodo.problema.modelo.meta
    
    # Si ya llegamos o se nos fue el rollo (pasarnos de la meta), el costo restante es 0
    if estado_actual >= meta:
        return 0
    
    # La estimación simplista en cuestión, como el Quijote y los molinos de viento
    return meta - estado_actual

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    # -------------------------------------------------------------------------------------------
    # Aquí inicia mi dolor de cabeza que no me lo quita ningún valium
    #--------------------------------------------------------------------------------------------
    """
    Modelo para el cubo de Rubik estándar 3x3x3
    
    El estado del cubo lo representaremos como un diccionario:
    - 'F': cara frontal (Front)
    - 'B': cara trasera (Back)
    - 'U': cara superior (Up)
    - 'D': cara inferior (Down)
    - 'L': cara izquierda (Left)
    - 'R': cara derecha (Right)
    
    Cada cara es una matriz de 3x3 que contiene los colores.
    Los colores se representan como letras:
    - 'W': blanco (White) - cara U
    - 'Y': amarillo (Yellow) - cara D
    - 'R': rojo (red) - cara F
    - 'O': naranja (Orange) - cara B
    - 'G': verde (Green) - cara L
    - 'B': azul (Blue) - cara R
    
    Las acciones son movimientos estándar de la notación del cubo:
    - 'F', 'F', 'F2': rotación de la cara frontal (sentido horario, antihorario, doble)
    - 'B', 'B', 'B2': rotación de la cara trasera
    - 'U', 'U', 'U2': rotación de la cara superior
    - 'D', 'D', 'D2': rotación de la cara inferior
    - 'L', 'L', 'L2': rotación de la cara izquierda
    - 'R', 'R', 'R2': rotación de la cara derecha
    
    """
    def __init__(self):
        """
        Inicializa el modelo del cubo de Rubik
        
        """
        # Definimos los colores para cada cara en el estado resuelto
        self.colores = {
            'U': 'W', # Up (blanco)
            'D': 'Y', # Down (amarillo)
            'F': 'R', # Front (rojo)
            'B': 'O', # Back (naranja)
            'L': 'G', # Left (verde)
            'R': 'B'  # Right (azul)
        }
        
    def estado_inicial(self):
        """
        Devuelve un cubo resuelto como estado inicial
        
        """
        estado = {}
        
        # Inicializamos cada cara con su color correspondiente
        for cara, color in self.colores.items():
            estado[cara] = [[color for _ in range(3)] for _ in range(3)]
            
        return estado

    def acciones_legales(self, estado):
        """
        Determina las acciones legales en un estado dado.
        
        En el cubo Rubik, todas las acciones son legales en cualquier estado.
        
        @param estado: Estado actual del cubo
        @return: Lista de acciones legales
        
        """
        # Movimientos básicos: sentido horario, antihorario y doble giro
        caras = ['F', 'B', 'U', 'D', 'L', 'R']
        
        # Generamos todas las acciones posibles (spoiler, un chingo)
        acciones = []
        for cara in caras:
            # Movimiento en sentido horario
            acciones.append(cara)
            # Movimiento en sentido antihorario (notación con prima)
            acciones.append(f"{cara}")
            # Doble movimiento (giro de 180°)
            acciones.append(f"{cara}2")
            
        return acciones

    def sucesor(self, estado, accion):
        """
        Determina el estado sucesor al aplicar una acción
        
        @param estado: Estado actual del cubo
        @param accion: Acción a aplicar (movimiento del cubo)
        @return: Nuevo estado resultante
        
        """
        # Hay que checar que pueda hashear el diccionario (me apendeje)
        if isinstance(estado, tuple):
            estado = self.hasheable_a_estado(estado)
        
        # Copio el estado para que no sé modifique
        nuevo_estado = self._copiar_estado(estado)
        
        # Extracción de la cara y el tipo de movimiento
        if len(accion) == 1:
            
            # Movimiento simple
            cara = accion
            repeticiones = 1
            
        elif len(accion) > 1 and accion[1] == "'":
            
            # Movimiento antihorario
            cara = accion[0]
            repeticiones = 3 # Tres movimientos para tres (sentido horario)
            
        elif len(accion) > 1 and accion[1] == "2":
            
            # Doble movimiento
            cara = accion[0]
            repeticiones = 2
            
        else:
            raise ValueError(f"Sepa que madres hiciste (no reconozco tu accion): {accion}")
        
        # Aplicamos el movimiento al cantidad de veces indicada
        for _ in range(repeticiones):
            nuevo_estado = self._aplicar_movimiento(nuevo_estado, cara)
            
        return nuevo_estado
    
    def _copiar_estado(self,estado):
        """
        Crea una copia profunda del estado.
        
        @param estado: Estado del cubo a copiar
        @return: Copia profunda del estado
        
        """
        nuevo_estado = {}
        for cara, matriz in estado.items():
            nuevo_estado[cara] = [fila[:] for fila in matriz]
        return nuevo_estado
    
    def _aplicar_movimiento(self, estado, cara):
        """
        Aplica un movimiento básico en sentido horario.
        
        @param estado: Estado actual del cubo
        @para cara: Cara a rotar ('F', 'B', 'U', 'D', 'L', 'R')
        @return: Nuevo estado después de aplicar el movimiento
        
        """
        # Primero rotamos la cara 90 grados en sentido horario
        estado[cara] = self._rotar_cara_horario(estado[cara])
        
        # Actualizamos las aristas afectadas según la cara
        if cara == 'F':     # Frontal
            # Guardamos de forma temporal la fila superior
            temp = [estado['U'][2][0], estado['U'][2][1], estado['U'][2][2]]
            
            # Movemos izquierda -> superior
            estado['U'][2][0] = estado['L'][2][2]
            estado['U'][2][1] = estado['L'][1][2]
            estado['U'][2][2] = estado['L'][0][2]
            
            # Movemos inferior -> izquierda
            estado['L'][0][2] = estado['D'][0][0]
            estado['L'][1][2] = estado['D'][0][1]
            estado['L'][2][2] = estado['D'][0][2]
            
            # Movemos derecha -> inferior
            estado['D'][0][0] = estado['R'][2][0]
            estado['D'][0][1] = estado['R'][1][0]
            estado['D'][0][2] = estado['R'][0][0]
            
            # Movemos temporal (superior) -> derecha
            estado['R'][0][0] = temp[2]
            estado['R'][1][0] = temp[1]
            estado['R'][2][0] = temp[0]
            
        elif cara == 'B':   # Trasera
            # Guardamos de forma temporal la fila superior
            temp = [estado['U'][0][0], estado['U'][0][1], estado['U'][0][2]]
            
            # Movemos derecha -> superior
            estado['U'][0][0] = estado['R'][0][2]
            estado['U'][0][1] = estado['R'][1][2]
            estado['U'][0][2] = estado['R'][2][2]
            
            # Movemos inferior -> derecha
            estado['R'][0][2] = estado['D'][2][2]
            estado['R'][1][2] = estado['D'][2][1]
            estado['R'][2][2] = estado['D'][2][0]
            
            # Movemos izquierda -> inferior
            estado['D'][2][0] = estado['L'][0][0]
            estado['D'][2][1] = estado['L'][1][0]
            estado['D'][2][2] = estado['L'][2][0]
            
            # Movemos temporal (superior) -> izquierda
            estado['L'][0][0] = temp[2]
            estado['L'][1][0] = temp[1]
            estado['L'][2][0] = temp[0]
            
        elif cara == 'U':   # Superior
            # Guardamos de forma temporal la fila superior de frontal
            temp = [estado['F'][0][0], estado['F'][0][1], estado['F'][0][2]]
            
            # Movemos derecha -> frontal
            estado['F'][0][0] = estado['R'][0][0]
            estado['F'][0][1] = estado['R'][0][1]
            estado['F'][0][2] = estado['R'][0][2]
            
            # Movemos trasera -> derecha
            estado['R'][0][0] = estado['B'][0][0]
            estado['R'][0][1] = estado['B'][0][1]
            estado['R'][0][2] = estado['B'][0][2]
            
            # Movemos izquierda -> trasera
            estado['B'][0][0] = estado['L'][0][0]
            estado['B'][0][1] = estado['L'][0][1]
            estado['B'][0][2] = estado['L'][0][2]
            
            # Movemos temporal (frontal) -> izquierda
            estado['L'][0][0] = temp[0]
            estado['L'][0][1] = temp[1]
            estado['L'][0][2] = temp[2]
            
        elif cara == 'D':   # Inferior
            # Guardamos de forma temporal la fila inferior de frontal
            temp = [estado['F'][2][0], estado['F'][2][1], estado['F'][2][2]]
            
            # Movemos izquierda -> frontal
            estado['F'][2][0] = estado['L'][2][0]
            estado['F'][2][1] = estado['L'][2][1]
            estado['F'][2][2] = estado['L'][2][2]
            
            # Movemos trasera -> izquierda
            estado['L'][2][0] = estado['B'][2][0]
            estado['L'][2][1] = estado['B'][2][1]
            estado['L'][2][2] = estado['B'][2][2]
            
            # Movemos derecha -> trasera
            estado['B'][2][0] = estado['R'][2][0]
            estado['B'][2][1] = estado['R'][2][1]
            estado['B'][2][2] = estado['R'][2][2]
            
            # Movemos temporal (frontal) -> derecha
            estado['R'][2][0] = temp[0]
            estado['R'][2][1] = temp[1]
            estado['R'][2][2] = temp[2]
            
        elif cara == 'L':   # Izquierda
            # Guardamos de forma temporal la columna izquierda de frontal
            temp = [estado['F'][0][0], estado['F'][1][0], estado['F'][2][0]]
            
            # Movemos inferior -> frontal
            estado['F'][0][0] = estado['D'][0][0]
            estado['F'][1][0] = estado['D'][1][0]
            estado['F'][2][0] = estado['D'][2][0]
            
            # Movemos trasera -> inferior
            estado['D'][0][0] = estado['B'][2][2]
            estado['D'][1][0] = estado['B'][1][2]
            estado['D'][2][0] = estado['B'][0][2]
            
            # Movemos superior -> trasera
            estado['B'][0][2] = estado['U'][2][0]
            estado['B'][1][2] = estado['U'][1][0]
            estado['B'][2][2] = estado['U'][0][0]
            
            # Movemos temporal (frontal) -> superior
            estado['U'][0][0] = temp[0]
            estado['U'][1][0] = temp[1]
            estado['U'][2][0] = temp[2]
            
        elif cara == 'R':    # Derecha
            # Guardamos de forma temporal la columna derecha de frontal
            temp = [estado['F'][0][2], estado['F'][1][2], estado['F'][2][2]]
            
            # Movemos superior -> frontal
            estado['F'][0][2] = estado['U'][0][2]
            estado['F'][1][2] = estado['U'][1][2]
            estado['F'][2][2] = estado['U'][2][2]
            
            # Movemos trasera -> superior
            estado['U'][0][2] = estado['B'][2][0]
            estado['U'][1][2] = estado['B'][1][0]
            estado['U'][2][2] = estado['B'][0][0]
            
            # Movemos inferior -> trasera
            estado['B'][0][0] = estado['D'][2][2]
            estado['B'][1][0] = estado['D'][1][2]
            estado['B'][2][0] = estado['D'][0][2]
            
            # Movemos temporal (frontal) -> inferior
            estado['D'][0][2] = temp[0]
            estado['D'][1][2] = temp[1]
            estado['D'][2][2] = temp[2]
            
        return estado
    
    def _rotar_cara_horario(self, cara):
        """
        Rota una cara 90 grados en sentido horario.
        
        @param cara: Matriz 3x3 que representa la cara
        @return: Nueva matriz rotada
        
        """
        # Creamos una nueva matriz para la cara rotada
        nueva_cara = [[None for _ in range(3)] for _ in range(3)]
        
        # Rotamos 90 grados en sentido horario
        for i in range(3):
            for j in range(3):
                nueva_cara[j][2-i] = cara[i][j]
                
        return nueva_cara


    def estado_a_hasheable(self, estado):
        """
        Convierte el estado del cubo (diccionario) a una representación hasheable (tupla).
        
        @param estado: Estado del cubo (diccionario)
        @return: Tupla hasheable que representa el estado
        """
        estado_hasheable = []
        # Para cada cara en un orden fijo
        for cara in sorted(estado.keys()):
            # Convertimos la matriz en una tupla de tuplas
            matriz_cara = tuple(tuple(fila) for fila in estado[cara])
            estado_hasheable.append((cara, matriz_cara))
        
        return tuple(estado_hasheable)

    def hasheable_a_estado(self, estado_hasheable):
        """
        Convierte un estado hasheable de vuelta a la representación de diccionario.
        
        @param estado_hasheable: Tupla hasheable que representa el estado
        @return: Diccionario con el estado del cubo
        """
        estado = {}
        for cara, matriz_cara in estado_hasheable:
            # Convertimos la tupla de tuplas de vuelta a una lista de listas
            estado[cara] = [list(fila) for fila in matriz_cara]
        
        return estado
    
    def costo_local(self, estado, accion):
        """
        Determina el costo de aplicar una acción en un estado.
        
        En el caso del cubo Rubik, todas las acciones tienen el mismo costo.
        
        @param estado: Estado actual del cubo
        @param accion: Acción a aplicar
        @return: Costo de la acción (1 para todos los movimientos)
        
        """
        # Todos los movimientos tienen el mismo costo
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado
        
        @param estado: Estado del cubo a imprimir
        @return: Representación en texto del estado

        """
        resultado = []
        
        # Imprimimos la cara superior
        resultado.append("    U    ")
        for fila in estado['U']:
            resultado.append("   " + "".join(fila) + "   ")
        
        # Imprimimos las caras L, F, R, B en una línea
        for i in range(3):
            linea = estado['L'] + estado['F'][i] + estado['R'][i] + estado['B'][i]
            resultado.append("".join(linea))
        
        # Imprimimos la cara inferior (D)
        resultado.append("    D    ")
        for fila in estado['D']:
            resultado.append("   " + "".join(fila) + "   ")
        
        return "\n".join(resultado)
    
    def es_estado_final(self, estado):
        """
        Verifica si el estado es el estado final (cubo resuelto).
        
        @param restado: Estado actual del cubo
        @return: True si el cubo está resuelto, False en caso contrario
        
        """
        
        # Por esta madre no dormí
        if isinstance(estado, tuple):
            estado = self.hasheable_a_estado(estado)
            
        # Un cubo está resuelto cuando cada cara tiene un solo color
        for cara, matriz in estado.items():
            color = matriz[0][0] # Color de referencia
            for fila in matriz:
                for celda in fila:
                    if celda != color:
                        return False
                    
        return True
    
    def mezclar_cubo(self, n_movimientos=20):
        """
        Genera un estado mezclado aplicando n movimientos aleatorios.
        
        @param n_movimientos: Número de movimientos aleatorios
        @return: Estado mezclado del cubo
        
        """
        import random
        
        estado = self.estado_inicial()
        acciones = self.acciones_legales(estado)
        
        for _ in range(n_movimientos):
            accion = random.choice(acciones)
            estado = self.sucesor(estado, accion)
            
        return estado
 
 # ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.
    
    Se parte de un cubo mezclado y se busca llegar al estado resuelto aplicando una
    secuencia óptima de movimientos.

    """
    def __init__(self, estado_inicial=None, n_mezcla=20):
        """
        Inicializa el problema del cubo de Rubik.
        
        @param estado_inicial: Estado inicial del ubo
        @oaram n_mezcla: Número de movimientos para mezclar el cubo si no se da
        estado_inicial
        
        """
        
        # Creamos el modelo
        modelo = CuboRubik()
        
        # En caso de no proporcionar estado inicial, mezclamos el cubo
        if estado_inicial is None:
            estado_inicial = modelo.mezclar_cubo(n_mezcla)
        
        # Verificamos si el cubo está resuelto
        meta = modelo.es_estado_final
        
        # Inicializamos la clase padre
        super().__init__(estado_inicial, meta, modelo)
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Heurística basada en el número de piezas mal colocadas.
    
    Esta heurística cuenta cuántas piezas (esquinas, aristas y centros)
    no están en su posición correcta respecto al estado resuelto.
    
    Es admisible porque:
    1. Cada pieza mal colocada requiere al menos un movimiento para colocarla.
    2. En realidad, mover una pieza a su posición correcta generalmente
       descoloca otras piezas, así que el costo real será mayor.
    3. Por lo tanto, esta heurística nunca sobreestima el costo real.
    
    @param nodo: Nodo actual en el árbol de búsqueda
    @return: Estimación del costo mínimo para resolver el cubo

    """
    estado = nodo.estado
    modelo = nodo.problema.modelo
    
    # Estado resuelto para comparar
    estado_resuelto = modelo.estado_inicial()
    
    # Contamos las piezas mal colocadas
    piezas_incorrectas = 0
    
    # Verificamos las caras
    for cara in estado.keys():
        for i in range(3):
            for j in range(3):
                # Si el color no coincide con el estado resuelto
                if estado[cara][i][j] != estado_resuelto[cara][i][j]:
                    piezas_incorrectas += 1
    
    # Cada pieza mal colocadas requiere al menos un movimiento
    return piezas_incorrectas // 4 # Dividimos entre 4 para hacerla más informativa, pero seguir siendo admisible

# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Heurística basada en la cantidad de stickers mal colocados,
    normalizada según cuantos stickers mueve cada acción (~8).
    
    Es admisible porque:
    1. Cada movimiento puede corregir hasta 8 stickers
    2. Nunca sobreestima el costo real.
    
    @param nodo: Nodo actual en el árbol de búsqueda
    @return: Estimación del costo mínimo para resolver el cubo 
    
    """
    estado = nodo.estado
    errores = 0
    
    for cara, matriz in estado.items():
        color_objetivo = matriz[1][1]
        for i in range(3):
            for j in range(3):
                if (i, j) != (1, 1):
                    if matriz[i][j] != color_objetivo:
                        errores += 1
                        
    return errores // 8


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


    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PblCamionMágico(100)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PblCuboRubik(n_mezcla=5)  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    