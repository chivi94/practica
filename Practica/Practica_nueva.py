#-*- encoding: utf-8 -*-
'''
Created on 4 de may. de 2016
@author: Antonio Roman Lopez
         Ivan Gonzalez Rincon
'''
import gtk

class Practica:
    
    def __init__(self,filas, columnas,ruta_desactivado,ruta_activado,ruta_boton,ruta_borde):
        #Atributos de la clase
        self.ruta_boton = ruta_boton;
        self.ruta_desactivado = ruta_desactivado;
        self.ruta_activado = ruta_activado;
        self.ruta_borde = ruta_borde;
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
        #Ventana
        self.ventana = self.interfaz.get_object("wd_ventana");
        self.ventana.resize(200,200);
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
        
        self.tablero = [];
        #Tablero de juego
        self.crear_tablero(self.filas,self.columnas);
        #Bordes del tablero
        self.bordes_tablero(self.filas,self.columnas);
        #Volcamos la tabla en el array
        self.tablero = self.tabla.get_children();              
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
        print coordenadas;
        #Hacemos split para poder acceder a fila y columna
        coordenadas_separadas = coordenadas.split(".");   
        self.modificar_posicion(int(coordenadas_separadas[0]), int(coordenadas_separadas[1]), widget.get_child());
    
    #Tablero de juego
    def crear_tablero(self,filas,columnas):
        for i in range(2,self.filas-2):
            for j in range(2,self.columnas-2):
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
                self.tabla.attach(self.event_box,i,i+1,j,j+1);
    #Método que genera la cruz de 'x' en el tablero en función de la posición pasada como parámetro
    def bordes_tablero(self,filas, columnas):
        #Borde de la tabla
        #Borde superior
        for j in range (2,columnas-2):
            for i in range (2):
                self.img_borde = gtk.Image();
                self.img_borde.set_from_file(self.ruta_borde);
                self.img_borde.show();
                #EventBox sirve para poder controlar los eventos de click en la imagen
                self.event_box = gtk.EventBox();                
                #Indice de los eventbox              
                self.name = str(i)+"."+str(j);
                self.event_box.set_name(self.name);
                self.event_box.add(self.img_borde);
                self.event_box.show();
                self.tabla.attach(self.event_box,j,j+1,i,i+1);
        #Borde izquierdo
        for j in range (0,columnas):
            for i in range (2):
                self.img_borde = gtk.Image();
                self.img_borde.set_from_file(self.ruta_borde);
                self.img_borde.show();
                #EventBox sirve para poder controlar los eventos de click en la imagen
                self.event_box = gtk.EventBox();                
                #Indice de los eventbox              
                self.name = str(i)+"."+str(j);
                self.event_box.set_name(self.name);
                self.event_box.add(self.img_borde);
                self.event_box.show();
                self.tabla.attach(self.event_box,i,i+1,j,j+1);
        #Borde derecho
        for j in range (0,columnas):
            for i in range (filas-2,filas):
                self.img_borde = gtk.Image();
                self.img_borde.set_from_file(self.ruta_borde);
                self.img_borde.show();
                #EventBox sirve para poder controlar los eventos de click en la imagen
                self.event_box = gtk.EventBox();                
                #Indice de los eventbox              
                self.name = str(i)+"."+str(j);
                self.event_box.set_name(self.name);
                self.event_box.add(self.img_borde);
                self.event_box.show();
                self.tabla.attach(self.event_box,i,i+1,j,j+1);
        #Borde inferior
        for j in range (2,columnas-2):
            for i in range (filas-2,filas):
                self.img_borde = gtk.Image();
                self.img_borde.set_from_file(self.ruta_borde);
                self.img_borde.show();
                #EventBox sirve para poder controlar los eventos de click en la imagen
                self.event_box = gtk.EventBox();                
                #Indice de los eventbox              
                self.name = str(i)+"."+str(j);
                self.event_box.set_name(self.name);
                self.event_box.add(self.img_borde);
                self.event_box.show();
                self.tabla.attach(self.event_box,j,j+1,i,i+1); 
    
    #Método que genera la cruz de 'x' en el tablero en función de la posición pasada como parámetro
    def modificar_posicion(self,fila,columna,widget):
        #Cuadrado generado central(3x5)
        for fila_actual in range(fila-1,fila+2):
            for columna_actual in range(columna-2,columna+3):
                self.comprobar_posicion(fila_actual, columna_actual,widget);
        #Fila superior 
        for fil_sup in range(fila-2,fila-1):
            for col_sup in range (columna-1,columna+2):
                self.comprobar_posicion(fil_sup, col_sup,widget);
        #Fila inferior
        for fil_inf in range(fila+2,fila+3):
            for col_inf in range (columna-1,columna+2):
                self.comprobar_posicion(fil_inf, col_inf,widget);

    #Método que modificará la posición pasada como parámetro, en el tablero indicado
    def comprobar_posicion(self,fila,columna,widget):
        estado_imagen = widget.get_name();
        if estado_imagen == "desactivado":       
            widget.set_from_file(self.ruta_activado);
            widget.set_name("activado");
        else:
            widget.set_from_file(self.ruta_desactivado);
            widget.set_name("desactivado");     
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
    ruta_borde = "iconos\borde.png";
    practica = Practica(3,3,ruta_desactivado,ruta_activado,ruta_boton,ruta_borde);
    gtk.main();