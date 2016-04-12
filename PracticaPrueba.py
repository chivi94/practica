#-*- encoding: utf-8 -*-
'''
Created on 7 de mar. de 2016
@authors: Antonio Roman Lopez
          Ivan Gonzalez Rincon
'''
import random

#Variables usadas para iniciar el fichero
puntuaciones_iniciales = []
ruta_fichero = "puntuaciones.txt"
#Tenemos un marco de 2x2 para controlar la generaciï¿½n de posiciones en los extremos del tablero.
#Por ello, necesitamos 2 filas y 2 columnas mas a cada lado.
FILAS = 14
COLUMNAS = 14

tablero = []
historial_jugadas=[]
puntuacion = 0
#Este contador llevara la cuenta de la ronda en la que el usuario se encuentra para 
#poder deshacer jugada.
ronda_actual = 0

#Lista con las letras de las distintas filas
#26 niveles en total
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def iniciar_tablero(tablero):
    for i in range(FILAS):
        tablero.append([])
        for j in range(COLUMNAS):
            tablero[i].append(".")

def imprimir_tablero(tablero):
    '''Los rangos estan asi para delimitar la matriz acorde con las peticiones del enunciado.
    Contamos con un marco de 2 filas y 2 columnas a ambos lados del tablero'''
    cont_letras = 0
    #Indices de las columnas
    print " ",
    for indice in range(0,COLUMNAS-4):
        print indice,
    print ""
    
    for i in range(2,FILAS-2):   
        print letras[cont_letras] ,
        for j in range(1,COLUMNAS-3):
            print tablero[i][j],
        print""
        cont_letras+=1
 
'''Este metodo llenara el tablero de juego recibido como parametro y en funcion del nivel seleccionado por el usuario. 
El nivel por defecto es 1.'''         
def llenar_tablero(tablero, nivel=1):
    '''Las columnas siguen la notacion 0-9 y las filas asociadas a las letras la notacion 1-10'''
    fila_generada = 0
    columna_generada = 0    
    ultima_fila = FILAS - 4
    ultima_columna = COLUMNAS - 5
    for i in range(0,nivel):
        fila_generada = random.randint(1,ultima_fila)
        columna_generada = random.randint(0,ultima_columna)
        print fila_generada,columna_generada                      
        modificar_posicion(fila_generada, columna_generada, tablero)                  
                 
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
        if tablero[fila][columna] == "x":       
            tablero[fila][columna] = "."
        else:
            tablero[fila][columna] = "x"

'''Metodo que deshara la jugada actual del jugador.
Debera volver a un estado anterior siempre que el actual no sea el primer turno de juego.
'''
def deshacer_jugada(tablero):
    if  len(historial_jugadas)>0:
        global ronda_actual
        peticion=historial_jugadas[ronda_actual-1]
        numero_fila= (ord(letra_fila)-ord("a"))+2
        numero_columna = int(peticion[1])+2
        modificar_posicion(numero_fila-1, numero_columna-2, tablero)
        historial_jugadas.remove(peticion)
        ronda_actual -=1
    else:
        print "No se puede deshacer la jugada actual"   

#Metodo que comprobara si se ha completado el tablero
def tablero_completado(tablero):
    contador = 0
    for i in range(2,FILAS-2):
        for j in range(1,COLUMNAS-3):
            if tablero[i][j] == 'x':
                contador+=1
    #Si todo el tablero esta desactivado, el programa termina
    if contador == 0:
        print "Enhorabuena, has completado el nivel,¡Hasta la próxima!"
        return False
    #En caso contrario, continua
    else:
        return True

def comprobar_puntuaciones(nivel,puntuacion):
    fichero = open("puntuaciones.txt","r")
    lineas = []
    for linea in fichero:
        punt = linea.split(":")
        nivel_guardado = int(punt[0])
        toques_nivel =int(punt[1])
        
        if (toques_nivel > puntuacion) and (nivel_guardado == nivel): 
            nueva_puntuacion = str(nivel_guardado)+":"+str(puntuacion)
            print "¡Puntuación del nivel mejorada!"
            print "Puntuación anterior:",toques_nivel
            print "Puntuación actual:",puntuacion
        else:
           nueva_puntuacion = str(nivel_guardado)+":"+str(toques_nivel) 
        lineas.append(nueva_puntuacion)
    fichero.close()
    #Volcamos el array con las nuevas puntuaciones
    fichero = open("puntuaciones.txt","w")
    for linea in lineas:
        fichero.write(linea)
        fichero.write("\n")
    fichero.close()  

def formato_puntuaciones(puntuaciones):
    for i in range (1,50):
        puntuaciones.append(i+":"+50)

def iniciar_fichero(puntuaciones,ruta):
    #Volcamos el array con las nuevas puntuaciones
    fichero = open(ruta,"w")
    for puntuacion in puntuaciones:
        fichero.write(puntuacion)
        fichero.write("\n")
    fichero.close() 
     
def peticion_nivel(tablero):
    correcto = False
    while not correcto:
        try:
            nivel = int(raw_input("Introduzca nivel:"))  
            if nivel <= 0 or nivel > len(letras):
                print "Nivel no válido, máximo:",len(letras)
            else:
                correcto = True
        except ValueError:
            print "Entrada no válida"  
            
    return nivel


iniciar_tablero(tablero)
nivel=peticion_nivel(tablero)  
llenar_tablero(tablero, nivel)
#Juego
continuar = True
while continuar:
    imprimir_tablero(tablero)   
    peticion = raw_input("Seleccione coordenadas:")
    peticion_correcta = peticion.replace(" ", "").lower()
    #Comprobacion de la peticion realizada por el usuario
    try:
        if len(peticion)==2:
            letra_fila = peticion_correcta[0]
            #Con ord obtenemos el valor ASCII de los caracteres pasados como argumentos.Sumamos 2 para compensar el marco usado  
            numero_fila= (ord(letra_fila)-ord("a"))+2
            numero_columna = int(peticion_correcta[1])+2
            modificar_posicion(numero_fila-1, numero_columna-2, tablero)
            #Metemos el tablero actual en la posiciÃ³n correspondiente a la ronda que se estÃ¡ jugando
            historial_jugadas.insert(ronda_actual, peticion_correcta)
            print historial_jugadas[ronda_actual]
            ronda_actual+=1
            puntuacion +=1  
            continuar = tablero_completado(tablero)          
        elif peticion == "salir":
            continuar = False
        elif peticion == "deshacer":
        #Codigo que revertira un movimiento realizado por el jugador
            deshacer_jugada(tablero)
        else:
            print "Peticion no valida"  
    except IndexError:
        print "Indice no válido"
    except ValueError:
        print "Entrada inválida"
    except IOError:
        formato_puntuaciones(puntuaciones_iniciales)
        iniciar_fichero(puntuaciones_iniciales,ruta_fichero)
    finally:
        comprobar_puntuaciones(nivel, puntuacion)
print "¡Hasta la próxima!"