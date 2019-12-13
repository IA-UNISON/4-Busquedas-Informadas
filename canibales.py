import busquedas

class ModeloCanibales(busquedas.ModeloBusqueda):
    """
    Problema de los misioneros y canibales, donde x = ((nM0, nC0), (nM1, nC1), 0)
    es el estado con la cantidad de misioneros, canibales.
    La primera tupla es el numero de misioneros y canibales
    del lado izquierdo, la segunda tupla es el lado derecho.
    El numero es en donde se encuentra la canoa

    Acciones = {(0, 1), (0, 2), (1, 0), (2, 0), (1, 1)}

    donde el primer valor es el numero de misionesros y el segundo
    el de canibales

    la unica accion es pasar la canoa de una orilla a otra,
    que representaremos como una tupla con la cantidad de
    Misioneros y la cantidad de canibales

    x = (m, c, canoa)

    """

    def __init__(self, nM=3, nC=3):
        """
        Se especifican 3 de cada grupo. El estado inicial es siempre
        por la izquierda
        """
        self.nM = nM
        self.nC = nC

    def acciones_legales(self, estado):        

        m, c, canoa = estado
        acciones = []
        
         # las unicas acciones, pues maximo se pueden pasar dos personas
        for tup in ((0,1), (1,0), (1,1), (2,0), (0,2)):
            if canoa == 1:
                if (tup[0] <= m and tup[1] <= c and 
                     (m == 0 or m >= c) and 
                     (m == self.nM or self.nM - m >= self.nC - c)):
                 # if (estado['nM_izq'] - tup[0] >= estado['nC_izq'] - tup[1]
                 #    and estado['nM_der'] + tup[0] >= estado['nC_der'] + tup[1]):
                     acciones.append(tup)
            else:
                # cuando esta a la derecha
                if (tup[0] <= self.nM - m and tup[1] <= self.nC - c and 
                    (m == 0 or m >= c) and 
                    (m == self.nM or self.nM - m >= self.nC - c)):
                
                #if (estado['nM_der'] - tup[0] >= estado['nC_der'] - tup[1]
                #    and estado['nM_izq'] + tup[0] >= estado['nC_izq'] + tup[1]):
                    acciones.append(tup)
        
        return acciones

#        return (
#            tup for tup in ((0,1), (1,0), (1,1), (2,0), (0,2)) if
#            ( (canoa > 0 and tup[0] <= m and tup[1] <= c) or
#              (canoa < 0 and tup[0] <= self.nM - m and tup[1] <= self.nC - c))
#        )

    def sucesor(self, estado, accion):
        """
        Recibe un estado junto con una accion (tupla) para
        generar la transicion
        """
        return (estado[0] - estado[2] * accion[0], 
                estado[1] - estado[2] * accion[1],
                -1 * estado[2])


        # if estado['canoa'] == 'izquierda':
        #     x['nM_der'] += accion[0]
        #     x['nC_der'] += accion[1]
        #     x['nM_izq'] -= accion[0]
        #     x['nC_izq'] -= accion[1]
        #     x['canoa'] = 'derecha'
        # else:
        #     x['nM_der'] -= accion[0]
        #     x['nC_der'] -= accion[1]
        #     x['nM_izq'] += accion[0]
        #     x['nC_izq'] += accion[1]
        #     x['canoa'] = 'izquierda'

        # return x


def es_meta(estado):
    return estado[0] == estado[1] == 0


class PblCanibales(busquedas.ProblemaBusqueda):
    def __init__(self, nM, nC):
        super().__init__( (nM, nC, 1), es_meta, ModeloCanibales(nM,nC))
    
if __name__ is "__main__":

    print("Problema de los canibales resuelto con busqueda a lo ancho:")
    print(busquedas.busqueda_ancho(PblCanibales(3,3)))
    
    print("\nProblema de los canibales resuelto con busqueda a lo profundo:")
    print(busquedas.busqueda_profundo(PblCanibales(3,3)))
    
    print("\nProblema de los canibales resuelto con busqueda profundidad iterativa:")
    print(busquedas.busqueda_profundidad_iterativa(PblCanibales(3,3)))

    print("\nProblema de los canibales resuelto con busqueda costo uniforme:")
    print(busquedas.busqueda_costo_uniforme(PblCanibales(3,3)))    
    