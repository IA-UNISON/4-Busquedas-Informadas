from busquedas import (
    NodoBusqueda,
    ProblemaBusqueda, 
    busqueda_ancho, 
    busqueda_A_estrella,
    busqueda_profundidad_iterativa,
    busqueda_profundo
)


class EsclavistasAfricanos(ProblemaBusqueda):
    """
    Si hay mas africanos que esclavistas los matan y se liberan, si hay mas esclavistas no pasa nada
    
    Estado: (e_izq, a_izq, bote)
    - e_izq: esclavistas en izquierda 
    - a_izq: africanos en izquierda 
    - bote: 1=izquierda, 0=derecha
    """ 
    
    def __init__(self):
        self.x0 = (3, 3, 1)
    
    def acciones(self, estado):
        """Retorna acciones válidas: (e, a) personas a mover"""
        e_izq, a_izq, bote = estado
        e_der = 3 - e_izq
        a_der = 3 - a_izq
        
        movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        validas = []
        
        for e, a in movimientos:
            if bote == 1:
                if e_izq >= e and a_izq >= a:
                    validas.append((e, a))
            else:
                if e_der >= e and a_der >= a:
                    validas.append((e, a))
        
        return validas
    
    def sucesor(self, estado, accion):
        e_izq, a_izq, bote = estado
        e, a = accion
        
        if bote == 1:
            nuevo = (e_izq - e, a_izq - a, 0)
        else:
            nuevo = (e_izq + e, a_izq + a, 1)
        
        if self.accion_legal(nuevo):
            return nuevo, 1
        else:
            return estado, float('inf')
    
    def terminal(self, estado):
        return estado == (0, 0, 0)
    
    def accion_legal(self, estado):
        e_izq, a_izq, bote = estado
        e_der = 3 - e_izq
        a_der = 3 - a_izq
        
        if e_izq < 0 or a_izq < 0 or e_der < 0 or a_der < 0:
            return False
        if e_izq > 3 or a_izq > 3 or e_der > 3 or a_der > 3:
            return False
        
        if e_izq > 0 and a_izq > e_izq:
            return False
        if e_der > 0 and a_der > e_der:
            return False
        
        return True


def heuristica_simple(nodo):
    """Número de personas en izquierda"""
    e_izq, a_izq, _ = nodo.estado
    return e_izq + a_izq


def main():
    problema = EsclavistasAfricanos()
    print(f"Heuristica inicial {heuristica_simple(NodoBusqueda(problema.x0))}")
    print("Búsqueda en anchura:")
    plan_bfs, nodos_bfs = busqueda_ancho(problema, problema.x0)
    print(f"Solución encontrada en {plan_bfs.profundidad} pasos")
    print(f"Nodos visitados: {nodos_bfs}\n")
    
    print("Búsqueda en a lo profundo:")
    plan_dfs, nodos_dfs = busqueda_profundo(problema, problema.x0)
    print(f"Solución encontrada en {plan_dfs.profundidad} pasos")
    print(f"Nodos visitados: {nodos_dfs}\n")
    
    print("Búsqueda en a la profundidad iterativa:")
    plan_dfis, nodos_dfis = busqueda_profundidad_iterativa(problema, problema.x0)
    print(f"Solución encontrada en {plan_dfis.profundidad} pasos")
    print(f"Nodos visitados: {nodos_dfis}\n")
    
    print("Búsqueda A*:")
    plan_a, nodos_a = busqueda_A_estrella(problema, heuristica_simple)
    print(f"Solución encontrada en {plan_a.profundidad} pasos")
    print(f"Nodos visitados: {nodos_a}")


if __name__ == "__main__":
    main()