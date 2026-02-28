![](ia.png)

Análisis de Heurísticas
1. Formalización
Camión Mágico

Estados: enteros de 1 a N.

Inicial: 1.

Meta: N.

Acciones:

caminar (+1, costo 1)

camion (×2, costo 2)

Cubo Rubik Simplificado

Estados: tuplas 3x3.

Inicial: generado desde la meta.

Meta: (1,2,3,4,5,6,7,8,9)

Acciones: {R, L, U, D}

Costo: 1 por movimiento.

2. Admisibilidad
Camión Mágico

h1(n) = N − estado
Nunca sobreestima porque representa el caso mínimo usando solo “caminar”.

h2(n) = (N − estado) // 2
No sobreestima ya que considera el mejor caso usando duplicaciones.

Ambas son admisibles.

Cubo Rubik

h1: número de piezas fuera de lugar.
Cada pieza incorrecta requiere al menos un movimiento → admisible.

h2: distancia Manhattan total.
Cada movimiento desplaza una pieza a lo sumo una posición → admisible.

3. Comparación

Camión:

h1: 12 nodos

h2: 13 nodos
No hay dominancia clara.

Cubo:

h1: 16 nodos

h2: 7 nodos
h2 explora menos nodos manteniendo optimalidad, por lo que domina empíricamente.

4. Conclusión

Heurísticas más informadas reducen nodos explorados sin perder optimalidad, confirmando la efectividad de A*.

# Búsquedas

## Objetivos

1. Desarrollar el algoritmo de búsqueda A*
2. Aplicar el algoritmo A* en un entorno y con diferentes heurísticas
3. A partir de una descripción, ser capaz de formalizar un problema de búsqueda (lights-outs)
4. Desarrollar la habilidad y creatividad para definir heurísticas no triviales.
5. Poder analizar, así sea informalmente, la admisibilidad de una heurística.
6. Comparar heurísticas no triviales.

De forma paralela, en esta tarea se desarrolla el uso de la herencia en objetos en python. Igualmente, para este problema, los estudiantes manejarán estructuras de datos más complejas como los `deque`, los `heapq`, tablas *hash* y conjuntos (como estructura de datos).

## Instrucciones:

1. En el archivo `busquedas.py` se encuentra la clase abstracta `ProblemaBusqueda` (para búsquedas), la clase `NodoBusqueda`, para la estructura de datos que nos ayudará en la búsqueda, así como ls 4 búsquedas no informadas más utilizadas: BFS, DFS, IDS y UCS. Estas búsquedas las vimos en clase y no vamos a repetir. 
   
   En clase se dio un ejemplo de el uso de dichas búsquedas. Revisa y familiarizate con dichas clases y funciones. Si es necesario desarrolla un problema pequeñito para que las pruebes (el problema de los *misioneros y los canibales* es un ejemplo fácil de programar y fácil de aplicar).
   
2. En el mismo archivo, en la parte final, se encuentra el encabezado para desarrollar la función de búsqueda utilizando el algoritmo A*. Recuerda que en general estamos haciendo la búsqueda en grafos con el fin de reducir el número de estados explorados. Con el fin que pruebes si el algoritmo que desarrollaste funciona, en el archivo `ocho_puzzle.py` se encuentra programado y funcionando el problema del ocho puzzle, así como las dos heurísticas vistas en clase. Con el fin de comparar resultados, se presenta la solución de 3 problemas (3 estados iniciales diferentes) con ambas heurísticas y con la búsqueda de costo uniforme. Puedes cambiar esto y experimentar, hasta que estes seguro que tu algoritmo es eficiente.
   
3. En el archivo `problemas.py` se encuentran unos nuevos problemas de planeación. Desarrolla los modelos de cada reto, definiendo los métodos de `acciones`, `sucesor`, `terminal` y modificando el método `__init__`. 

4. Desarrolla una heurística para cada reto, específica porque consideras que es admisible, y prográmala en la función `h_1_{nombre del problema}`. 
   
5. Ahora desarrolla una segunda heurística (proponer una puede ser algo dificil, pero dos ya implica creatividad). Argumenta porque crees que es admisible esta heurística.
   
6. Ejecuta el programa y revisa las soluciones con ambas heurísticas, y sobre esto, determina si hay una que parece dominante sobre la otra, y porqué.


