import random
#Tenemos un marco de 2x2 para controlar la generacion de posiciones en los extremos del tablero.
#Por ello, necesitamos 2 filas y 2 columnas mas a cada lado.
FILAS = 14
COLUMNAS = 14

tablero = []

def iniciar_tablero(tablero):
    for i in range(FILAS):
        tablero.append([])
        for j in range(COLUMNAS):
            tablero[i].append(".")

def imprimir_tablero(tablero):
    '''Los rangos estan asi para delimitar la matriz acorde con las peticiones del enunciado.
    Contamos con un marco de 2 filas y 2 columnas a ambos lados del tablero'''
    for i in range(2,FILAS-2):
        for j in range(2,COLUMNAS-2):
            print tablero[i][j],
        print""
 
'''Este metodo llenara el tablero de juego recibido como parametro y en funcion del nivel seleccionado por el usuario. 
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
        modificar_posicion(5, 5, tablero)                  
                 
def modificar_posicion(fila,columna,tablero):
    #Cuadrado generado central(3x5)
    fila = fila+1
    columna = columna+1
    for fila_actual in range(fila-1,fila+2):
        for columna_actual in range(columna-2,columna+3):
            comprobar_posicion(tablero, fila_actual, columna_actual)
    #Fila superior 
    for fil_sup in range(fila-2,fila-1):
        for col_sup in range (columna-1,columna+2):
            comprobar_posicion(tablero, fil_sup, col_sup)
    #Fila inferior
    for fil_inf in range(fila+2,fila+3):
        for col_inf in range (columna-1,columna+2):
            comprobar_posicion(tablero, fil_inf, col_inf)
            
def comprobar_posicion(tablero,fila,columna):   
    try:   
        if tablero[fila][columna] == "x":       
            tablero[fila][columna] = "."
        else:
            tablero[fila][columna] = "x"
    except IndexError:
        print "Indice no valido"
        

#Metodo que comprueba la peticion realizada por el usuario, y en caso que esta sea salir, termina la ejecucion.
def comprobar_peticion(peticion):
    if len(peticion)==2:
        letra_fila = peticion[0]
        #Con ord obtenemos el valor ASCII de los caracteres pasados como argumentos.Sumamos 2 para compensar el marco usado  
        numero_fila= (ord(letra_fila)-ord("a"))+2
        numero_columna = int(peticion[1])+2
        modificar_posicion(numero_fila-1, numero_columna-2, tablero)
        return True
    elif peticion == "salir":
        return False
    elif peticion == "deshacer":
        #Codigo que revertira un movimiento realizado por el jugador
        print "Se incluira en versiones posteriores"
        return True
    else:
        print "Peticion no valida"
        return True
                        
iniciar_tablero(tablero)
llenar_tablero(tablero, 1)       
#Juego
continuar = True
while(continuar):
    imprimir_tablero(tablero)   
    peticion = raw_input("Seleccione coordenadas:")
    peticion_correcta = peticion.replace(" ", "").lower()
    continuar=comprobar_peticion(peticion_correcta)         