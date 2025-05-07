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
    meta = nodo.padre.modelo.meta if nodo.padre else nodo.estado
    
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
    
    # Total: casa paso en el camión mágico cósmico cuesta 2, cada paso a patín cuesta 1
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
    meta = nodo.padre.modelo.meta if nodo.padre else nodo.estado
    
    # Si ya llegamos o se nos fue el rollo (paranos de la meta), el costo restante es 0
    if estado_actual >= meta:
        return 0
    
    # La estimación simplista en cuestión, como el Quijote y los molinos de viento
    return meta - estado_actual

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik.busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        raise NotImplementedError('Hay que hacerlo de tarea')
 
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
# ------------------------------------------------------------
def h_1_problema_1(nodo):
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
def h_2_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0



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
    problema = PblCamionMágico( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    