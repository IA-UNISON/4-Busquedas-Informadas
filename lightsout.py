#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Belen Chavarría'


import busquedas


class LightsOut(busquedas.ModeloBusqueda):
    # --------------------------------------------------------
    # Problema 2:  Completa la clase
    # para el modelo de lights out
    # --------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas
    adjacentes cambian (si estan prendidas se apagan y viceversa).

    El juego consiste en una matriz de 5 X 5, cuyo estado puede
    ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------

    Las acciones posibles son de elegir cambiar una luz y sus casillas
    adjacentes, por lo que la accion es un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self):
        # conjunto de acciones?
        self.acciones =  [i for i in range(25)]

       # raise NotImplementedError('Hay que hacerlo de tarea')
        
    def acciones_legales(self, estado):
        
        #devuelve una lista de casillas donde se puede dar click(Todas)
        return range(25)

        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        
        s = list(estado)
        
        s[accion]= 0 if s[accion]==1 else 1

        lim = (accion//5)*5
        for i in [1,-1]:
            if accion + i>lim and accion + i<lim + 5:
                s[accion + i]= 0 if s[accion + i]==1 else 1

        for i in [5,-5]:
            if accion + i>-1 and accion + i<25:
                s[accion + i]= 0 if s[accion + i]==1 else 1
                      
        return tuple(s)
        
        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        #cantidad de luces encendidas, despues de ejecutar la acción

        on=0
        s = self.sucesor(estado,accion)
        for i in range(25):
            if s[i]==1:
                on+=1 
                
        return on
        

        raise NotImplementedError('Hay que hacerlo de tarea')

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        return cadena


# ------------------------------------------------------------
#  Problema 3: Completa el problema de LightsOut
# ------------------------------------------------------------
class ProblemaLightsOut(busquedas.ProblemaBusqueda):
    
    def __init__(self, pos_ini):
        """
        Utiliza la superclase para hacer el problema

        """
        # Completa el código
        x0 = tuple(pos_ini)
        def meta(x):
            #si todas las casillas están apagadas devuelve True, si no False
            for i in range(25):
                if x[i]==1:
                    return False           
            return True
            

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    # La primer idea consiste en que el máximo de luces que podemos
    # apagar en una sola jugada es 5. Por lo que en el mejor de los
    # casos tendremos puras cruces que se apagan con un click cada una
    # si dividimos entre 5 el total de luces encendidas seria el mínimo 
    # requerido para apagarlas todas, por lo que la heuristica sería
    # admisible.
    
    total=0
    for i in range(25):
        total+= nodo.estado[i]

    return int(total/5)

# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    # En esta parte se consideran las luces encendidas en la primer fila 
    # que se necesitan apagar. Es muy tonta, no debe ser admisible porque no
    # significa que se tengan que apagar estas luces una por una, pueden ser
    # todas en un solo movimiento si son tres.
    fila1 = [i for i in range(5) if nodo.estado[i]==1]
    
    return len(fila1)


    
def h_3(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    # consiste en contar los grupos de a lo mas 5 luces adyaacentes que estan encendidas.
    # Hasta ahora, fue la mejor heurística que encontré. Según mi parecer no es admisible
    # porque los grupos podrían estar mejor distribuidos y reducirse la cantidad de estos.
    
    vecindad ={}

    for i in range(25):
        flag = False
        if nodo.estado[i] == 1:
            #buscamos en las vecindades para ver si pertenece a alguna
            for x in vecindad.keys():
                if len(vecindad[x])<5:
                    for xi in vecindad[x]:
                        if abs(xi-i)==5 or (xi%5==0 and i-xi==1) or (xi%5==4 and xi-i==1) or abs(xi-i)==1:
                            flag=True
                            vecindad[x].append(i)
                            break
                    if flag==True:
                        break
                
            if flag == False:
                vecindad[i] = [i]
    
    return len(vecindad)
    

def prueba_modelo():
    """
    Prueba la clase LightsOut

    """
    p0 = (0, 0, 1, 0, 0,
          0, 1, 1, 1, 0,
          0, 0, 1, 0, 0,
          0, 0, 0, 0, 0,
          0, 0, 0, 0, 0)
    
    p1 = (0, 0, 1, 0, 0,
          0, 1, 1, 0, 0,
          0, 0, 0, 1, 1,
          0, 0, 0, 1, 0,
          0, 0, 0, 0, 0)
    
    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 = (1, 0, 0, 1, 0,
              1, 0, 1, 1, 0,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a4 = (1, 0, 0, 0, 1,
              1, 0, 1, 1, 1,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)

    modelo = LightsOut()

    assert modelo.acciones_legales(pos_ini) == range(25)
    assert modelo.sucesor(p0, 13) == p1
    assert modelo.sucesor(pos_ini, 0) == pos_a0
    assert modelo.sucesor(pos_a0, 4) == pos_a4
    assert modelo.sucesor(pos_a4, 24) == pos_a24
    assert modelo.sucesor(pos_a24, 15) == pos_a15
    assert modelo.sucesor(pos_a15, 12) == pos_a12
    print("Paso la prueba de la clase LightsOut")


def compara_metodos(pos_inicial, heuristica_1, heuristica_2, heuristica_3):
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
    
    print('-' * 50)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados')
    print('-' * 50 + '\n\n')
    
    solucion4 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                             heuristica_3)
    print('A* con h3'.center(10) + str(solucion4.costo).center(20) +
          str(solucion4.nodos_visitados))
    print('-' * 50 + '\n\n')
    
    solucion3 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                             heuristica_2)
    print('A* con h2'.center(10) + str(solucion3.costo).center(20) +
          str(solucion3.nodos_visitados))
    print('-' * 50 + '\n\n')
    
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_1)
    
    print('A* con h1'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')
    
    solucion1 = busquedas.busqueda_costo_uniforme(ProblemaLightsOut(pos_inicial))
    

    
    print('A* con BCU'.center(10) + str(solucion1.costo).center(19) +
          str(solucion1.nodos_visitados))
    print('-' * 50 + '\n\n')
    
    


if __name__ == "__main__":

    print("Antes de hacer otra cosa,")
    print("vamos a verificar medianamente la clase LightsOut")
    prueba_modelo()

    
    prueba1 = (0, 0, 1, 0, 0,
               0, 1, 1, 1, 0,
               0, 0, 1, 0, 0,
               0, 0, 0, 0, 0,
               0, 0, 0, 0, 0)
    
    
    prueba2 = (0, 0, 1, 1, 0,
               0, 1, 1, 1, 0,
               0, 0, 1, 0, 1,
               0, 1, 0, 0, 0,
               0, 0, 0, 0, 0)
    
    # Tres estados iniciales interesantes
    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)


    print("\n\nPara el problema en prueba1")
    print("\n{}".format(LightsOut.bonito(prueba1)))
    compara_metodos(prueba1, h_1, h_2,h_3)

    print("\n\nPara el problema simétrico")
    print("\n".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2,h_3)
    
    print("\n\nPara el problema Bonito")
    print("\n".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2, h_3)
    
    print("\n\nPara el problema en diagonal")
    print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_2, h_3)
    
      
    
    
    

