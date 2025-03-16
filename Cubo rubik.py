class CuboRubik:
    def __init__(self):
        # Cada cara del cubo se representa como una matriz de 3x3
        # Cada elemento de la matriz es un color, por ejemplo 'R' para rojo, 'G' para verde, etc.
        self.cara_frontal = [['B' for _ in range(3)] for _ in range(3)]  # Rojo
        self.cara_izquierda = [['O' for _ in range(3)] for _ in range(3)]  # Naranja
        self.cara_derecha = [['R' for _ in range(3)] for _ in range(3)]  # Verde
        self.cara_trasera = [['G' for _ in range(3)] for _ in range(3)]  # Blanco
        self.cara_superior = [['Y' for _ in range(3)] for _ in range(3)]  # Amarillo
        self.cara_inferior = [['W' for _ in range(3)] for _ in range(3)]  # Azul

        # self.cara_frontal = [['A','B','C'],['D','F','G'],['H','I','J']]
        # self.cara_izquierda = [['1x','2x','3x'],['4x','5x','6x'],['7x','8x','9x']]
        # self.cara_derecha = [['1y','2y','3y'],['4y','5y','6y'],['7y','8y','9y']]
        # self.cara_trasera = [['a','b','c'],['d','f','g'],['h','i','j']]
        # self.cara_superior = [['1z','2z','3z'],['4z','5z','6z'],['7z','8z','9z']]
        # self.cara_inferior = [['1w','2w','3w'],['4w','5w','6w'],['7w','8w','9w']]
        
    # Pretty print provisional que imprime cada matriz (cara) del cubo
    def notSoPrettyPrint(self):
        print("\nCara Frontal:")
        for fila in self.cara_frontal:
            print(' '.join(fila))
        print("\nCara Izquierda:")
        for fila in self.cara_izquierda:
            print(' '.join(fila))
        print("\nCara Derecha:")
        for fila in self.cara_derecha:
            print(' '.join(fila))       
        print("\nCara Trasera:")
        for fila in self.cara_trasera:
            print(' '.join(fila)) 
        print("\nCara Superior:")
        for fila in self.cara_superior:
            print(' '.join(fila))       
        print("\nCara Inferior:")
        for fila in self.cara_inferior:
            print(' '.join(fila))
        

    # Método para rotar una cara del cubo 90° en sentido horario
    # Por ejemplo, si tenemos
    # 1 2 3
    # 4 5 6
    # 7 8 9
    # después de rotarla, debería quedar
    # 7 4 1
    # 8 5 2
    # 9 6 3
    def rotar_cara(self, cara):
        if cara == 'frontal':
            self.cara_frontal = [list(x) for x in zip(*self.cara_frontal[::-1])]
        elif cara == 'izquierda':
            self.cara_izquierda = [list(x) for x in zip(*self.cara_izquierda[::-1])]
        elif cara == 'derecha':
            self.cara_derecha = [list(x) for x in zip(*self.cara_derecha[::-1])]
        elif cara == 'trasera':
            self.cara_trasera = [list(x) for x in zip(*self.cara_trasera[::-1])]        
        elif cara == 'superior':
            self.cara_superior = [list(x) for x in zip(*self.cara_superior[::-1])]
        elif cara == 'inferior':
            self.cara_inferior = [list(x) for x in zip(*self.cara_inferior[::-1])]
        else:
            print("Cara no válida")

    # Método que con una cara dada, llama a la función rotar_cara con la cara dada
    # y luego mueve las piezas adyacentes a esa cara. Es básicamente para manejar
    # las piezas adyacentes.
    # Por ejemplo, si movemos la cara frontal, las piezas adyacentes a la cara frontal
    # deben moverse a la derecha, arriba, izquierda y abajo
    def mover(self, movimiento):
        if movimiento == 'F':
            self.rotar_cara('frontal')
            
            temp = [self.cara_izquierda[i][2] for i in range(3)] #guarda la columna derecha de la cara izquierda  
            temp2 = [self.cara_derecha[i][0] for i in range(3)] #guarda la columna izquierda de la cara derecha
            temp3 = self.cara_superior[2][:] #guarda la fila inferior de la cara superior
            temp4 = self.cara_inferior[0][:] #guarda la fila superior de la cara inferior

            # print("columna derecha de la cara izquierda - temp3: ",temp3)
            # print("columna izquierda de la cara derecha - temp4: ",temp4)
            # print("fila inferior de la cara superior - temp: ",temp)
            # print("fila superior de la cara inferior - temp2: ",temp2)

            # Cambia la cara superior
            for i in range(3):
                self.cara_superior[2][i] = temp[::-1][i]
            # Cambia la cara inferior
            for i in range(3):
                self.cara_inferior[0][i] = temp2[::-1][i]
            # Cambia la cara izquierda
            for i in range(3):
                self.cara_izquierda[i][2] = temp4[i] 
            # Cambia la cara derecha
            for i in range(3):
                self.cara_derecha[i][0] = temp3[i]

        elif movimiento == 'L':
            self.rotar_cara('izquierda')

            temp = [self.cara_frontal[i][0] for i in range(3)] #guarda la columna izquierda de la cara frontal
            temp2 = [self.cara_trasera[i][2] for i in range(3)] #guarda la columna derecha de la cara trasera
            temp3 = [self.cara_superior[i][0] for i in range(3)] #guarda la columna izquierda de la cara superior
            temp4 = [self.cara_inferior[i][0] for i in range(3)] #guarda la columna izquierda de la cara inferior

            # print("columna izquierda de la cara frontal - temp: ",temp)
            # print("columna derecha de la cara trasera - temp2: ",temp2)
            # print("columna izquierda de la cara superior - temp3: ",temp3)
            # print("columna izquierda de la cara inferior - temp4: ",temp4)

            # Cambia la cara superior
            for i in range(3):
                self.cara_superior[i][0] = temp2[::-1][i] 
            # Cambia la cara inferior
            for i in range(3):
                self.cara_inferior[i][0] = temp[i]
            # Cambia la cara frontal
            for i in range(3):
                self.cara_frontal[i][0] = temp3[i]
            # Cambia la cara trasera
            for i in range(3):
                self.cara_trasera[i][2] = temp4[::-1][i]

        elif movimiento == 'R':
            self.rotar_cara('derecha')

            temp = [self.cara_frontal[i][2] for i in range(3)] #guarda la columna derecha de la cara frontal
            temp2 = [self.cara_trasera[i][0] for i in range(3)] #guarda la columna izquierda de la cara trasera
            temp3 = [self.cara_superior[i][2] for i in range(3)] #guarda la columna derecha de la cara superior
            temp4 = [self.cara_inferior[i][2] for i in range(3)] #guarda la columna derecha de la cara inferior

            # print("columna derecha de la cara frontal - temp: ",temp)
            # print("columna izquierda de la cara trasera - temp2: ",temp2)
            # print("columna derecha de la cara superior - temp3: ",temp3)
            # print("columna derecha de la cara inferior - temp2: ",temp4)

            # Cambia la cara superior
            for i in range(3):
                self.cara_superior[i][2] = temp[i]
            # Cambia la cara inferior
            for i in range(3):
                self.cara_inferior[i][2] = temp2[::-1][i]
            # Cambia la cara frontal
            for i in range(3):
                self.cara_frontal[i][2] = temp4[i]
            # Cambia la cara trasera
            for i in range(3):
                self.cara_trasera[i][0] = temp3[::-1][i]

        elif movimiento == 'B':
            self.rotar_cara('trasera')

            temp = [self.cara_izquierda[i][0] for i in range(3)] #guarda la columna izquierda de la cara izquierda
            temp2 = [self.cara_derecha[i][2] for i in range(3)] #guarda la columna derecha de la cara derecha
            temp3 = self.cara_superior[0][:] #guarda la fila superior de la cara superior
            temp4 = self.cara_inferior[2][:] #guarda la fila inferior de la cara inferior

            # print("columna izquierda de la cara izquierda - temp: ",temp)
            # print("columna derecha de la cara derecha - temp2: ",temp2)
            # print("fila superior de la cara superior - temp3: ",temp3)
            # print("fila inferior de la cara inferior - temp4: ",temp4)

            # Cambia la cara superior
            for i in range(3):
                self.cara_superior[0][i] = temp2[i]
            # Cambia la cara inferior
            for i in range(3):
                self.cara_inferior[2][i] = temp[i]
            # Cambia la cara izquierda
            for i in range(3):
                self.cara_izquierda[i][0] = temp3[::-1][i]
            # Cambia la cara derecha
            for i in range(3):
                self.cara_derecha[i][2] = temp4[::-1][i]

        elif movimiento == 'U':
            self.rotar_cara('superior')

            temp = self.cara_frontal[0][:] #guarda la fila superior de la cara frontal
            temp2 = self.cara_izquierda[0][:] #guarda la fila superior de la cara izquierda
            temp3 = self.cara_derecha[0][:] #guarda la fila superior de la cara derecha
            temp4 = self.cara_trasera[0][:] #guarda la fila superior de la cara trasera

            # print("fila superior de la cara frontal - temp: ",temp)
            # print("fila superior de la cara izquierda - temp2: ",temp2)
            # print("fila superior de la cara derecha - temp3: ",temp3)
            # print("fila superior de la cara trasera - temp4: ",temp4)

            # Cambia la cara izquierda
            for i in range(3):
                self.cara_izquierda[0][i] = temp[i]
            # Cambia la cara derecha
            for i in range(3):
                self.cara_derecha[0][i] = temp4[i]
            # Cambia la cara frontal
            for i in range(3):
                self.cara_frontal[0][i] = temp3[i]
            # Cambia la cara trasera
            for i in range(3):
                self.cara_trasera[0][i] = temp2[i]
                 
        elif movimiento == 'D':
            self.rotar_cara('inferior')

            temp = self.cara_frontal[2][:] #guarda la fila inferior de la cara frontal
            temp2 = self.cara_izquierda[2][:] #guarda la fila inferior de la cara izquierda
            temp3 = self.cara_derecha[2][:] #guarda la fila inferior de la cara derecha
            temp4 = self.cara_trasera[2][:] #guarda la fila inferior de la cara trasera

            # print("fila inferior de la cara frontal - temp: ",temp)
            # print("fila inferior de la cara izquierda - temp2: ",temp2)
            # print("fila inferior de la cara derecha - temp3: ",temp3)
            # print("fila inferior de la cara trasera - temp4: ",temp4)
            
            # Cambia la cara izquierda
            for i in range(3):
                self.cara_izquierda[2][i] = temp4[i]
            # Cambia la cara derecha
            for i in range(3):
                self.cara_derecha[2][i] = temp[i]
            # Cambia la cara frontal
            for i in range(3):
                self.cara_frontal[2][i] = temp2[i]
            # Cambia la cara trasera
            for i in range(3):
                self.cara_trasera[2][i] = temp3[i]

cubo = CuboRubik()
cubo.notSoPrettyPrint()

cubo.mover('R')
cubo.mover('R')
cubo.mover('R')
cubo.mover('U')
cubo.mover('U')
cubo.mover('U')

print("\nEstado inicial:")
cubo.notSoPrettyPrint()

cubo.mover('U')
cubo.mover('R')

print("\nCubo arreglado despues de girar U y R:")
cubo.notSoPrettyPrint()


    # """
    # Esta heurística es sobre el tiempo usando el camión máximo posible y 
    # luego caminando. Es admisible porque asume el mejor escenario posible con el camión.

    # """
    # #problema = nodo.problema
    # N = nodo.problema.N
    # x_actual = nodo.estado[0]
    # if x_actual >= N:
    #     return 0
    # k = 0
    # while x_actual * (2 ** (k + 1)) <= N:
    #     k += 1
    # tiempo_camion = 2 * k
    # nueva_x = x_actual * (2 ** k)
    # restante = N - nueva_x
    # return tiempo_camion + restante
