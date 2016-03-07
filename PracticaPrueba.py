import random
FILAS = 14
COLUMNAS = 14

tablero = []

def iniciar_tablero(tablero):
    for i in range(FILAS):
        tablero.append([])
        for j in range(COLUMNAS):
            tablero[i].append(".")

def imprimir_tablero(tablero):
    '''Los rangos estan asi para delimitar la matriz acorde con las peticions del enunciado.
    Contamos con un marco de 2 filas y 2 columnas a ambos lados del tablero'''
    for i in range(2,FILAS-2):
        for j in range(2,COLUMNAS-2):
            print tablero[i][j],
        print""
 
'''ste metodo llenara el tablero de juego recibido como parametro y en funcion del nivel seleccionado por el usuario. 
El nivel por defecto es 1.'''         
def llenar_tablero(tablero, nivel=1):
    fila_generada = 0
    columna_generada = 0
    
    ultima_fila = FILAS - 2
    ultima_columna = COLUMNAS - 2
    for i in range(0,nivel):
        fila_generada = random.randint(1,ultima_fila)
        columna_generada = random.randint(1,ultima_columna)
        print fila_generada,columna_generada
        posicion_generada(fila_generada, columna_generada, tablero)
        
    
         
def posicion_generada(fila,columna,tablero):
    if tablero[fila][columna] == "x":
        tablero[fila][columna] = "."
    else:
        tablero[fila][columna] = "x"
              
iniciar_tablero(tablero)
imprimir_tablero(tablero)
llenar_tablero(tablero)
print "Pollas gordas"
imprimir_tablero(tablero)            