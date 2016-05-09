#-*- encoding: utf-8 -*-
'''
Created on 4 de may. de 2016

@author: Antonio Roman Lopez
         Ivan Gonzalez Rincon
'''
import gtk

class Practica:
    
    def __init__(self,filas, columnas,ruta_desactivado,ruta_activado,ruta_boton):
        #Atributos de la clase
        self.ruta_boton = ruta_boton;
        self.ruta_desactivado = ruta_desactivado;
        self.ruta_activado = ruta_activado;
        self.filas = filas+4;
        self.columnas = columnas+4;
        
        #Interfaz
        #Iconos genericos
        self.image_desactivado = gtk.Image();
        self.image_desactivado.set_from_file(self.ruta_desactivado);
        
        self.image_activado = gtk.Image();
        self.image_activado.set_from_file(self.ruta_activado);
        
        #Acceso a la interfaz
        self.interfaz = gtk.Builder();
        self.interfaz.add_from_file('practica.glade');
        self.interfaz.connect_signals(self);
        
        #Acceso a los componentes
        #Acceso al boton de retroceso
        self.btn_deshacer = self.interfaz.get_object("bttn_deshacer");
        self.image_refresh = gtk.Image();
        self.image_refresh.set_from_file(self.ruta_boton);
        
        self.btn_deshacer.set_image(self.image_refresh);
        #Acceso al tablero
        self.tabla = self.interfaz.get_object("tbl_tablero");
        self.tabla.resize(self.filas, self.columnas);
        self.tabla.set_homogeneous(True);
        self.tabla.show();
        
        #Matriz en la que almacenaremos nuestro tablero
        self.tablero = [];
        self.iniciar_tablero(self.tablero);
        
        self.x = 0;
        self.y = 0;
        for i in range(self.filas):
            for j in range(self.columnas):
                #Creamos imágenes y las añadimos al tablero
                self.img_desactivado = gtk.Image();
                self.img_desactivado.set_from_file(self.ruta_desactivado);
                #Estado
                self.img_desactivado.set_name("desactivado");
                self.img_desactivado.show();
                #EventBox sirve para poder controlar los eventos de click en la imagen
                self.event_box = gtk.EventBox();                
                #Indice de los eventbox              
                self.name = str(i)+"."+str(j);
                self.event_box.set_name(self.name);
                self.event_box.add(self.img_desactivado);
                self.event_box.connect('button-press-event',self.golpeo);
                self.event_box.show();
                self.tabla.attach(self.event_box,self.x+2,self.x+3,self.y+2,self.y+3);
                
                #Añadimos los componentes a nuestra matriz
                self.tablero[i][j] = self.event_box;
                self.x +=1;
            self.x = 0;
            self.y +=1;
            
        #Conexión a eventos
        self.interfaz.connect_signals(self);
        
    #Eventos    
    #Evento de cierre de ventana  
    def on_ventana_delete_event(self,widget,data = None):
        gtk.main_quit();
        
    #Evento de click en imagen de tablero
    def golpeo(self,widget,data = None):
        #Coordenadas del elemento sobre el que se ha hecho click
        coordenadas = widget.get_name();
        #Hacemos split para poder acceder a fila y columna
        coordenadas_separadas = coordenadas.split(".");   
        self.modificar_posicion(int(coordenadas_separadas[0]), int(coordenadas_separadas[1]), self.tablero); 
        
    #Método que genera la cruz de 'x' en el tablero en función de la posición pasada como parámetro
    def modificar_posicion(self,fila,columna,tablero):
        #Cuadrado generado central(3x5)
        for fila_actual in range(fila-1,fila+2):
            for columna_actual in range(columna-2,columna+3):
                self.comprobar_posicion(tablero, fila_actual, columna_actual);
        #Fila superior 
        for fil_sup in range(fila-2,fila-1):
            for col_sup in range (columna-1,columna+2):
                self.comprobar_posicion(tablero, fil_sup, col_sup);
        #Fila inferior
        for fil_inf in range(fila+2,fila+3):
            for col_inf in range (columna-1,columna+2):
                self.comprobar_posicion(tablero, fil_inf, col_inf);

    #Método que modificará la posición pasada como parámetro, en el tablero indicado
    def comprobar_posicion(self,tablero,fila,columna):
        imagen_actual = tablero[fila][columna].get_child(); 
        estado_imagen = tablero[fila][columna].get_child().get_name();
        if estado_imagen == "desactivado":       
            imagen_actual.set_from_file(self.ruta_activado);
            imagen_actual.set_name("activado");
        else:
            imagen_actual.set_from_file(self.ruta_desactivado);
            imagen_actual.set_name("desactivado");     
    #Métodos
    #Método que inicia la matriz de juego(tablero) con puntos
    def iniciar_tablero(self,tablero):
        for i in range(self.filas):
            tablero.append([]);   
            for j in range (self.columnas):
                tablero[i].append(".");
                
if __name__ == '__main__':
    ruta_boton = "iconos\refresh.png";
    ruta_desactivado = "iconos\desactivado.png";
    ruta_activado = "iconos\activado.png";
    practica = Practica(3,3,ruta_desactivado,ruta_activado,ruta_boton);
    gtk.main();