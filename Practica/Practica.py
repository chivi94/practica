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
        self.filas = filas;
        self.columnas = columnas;
        
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
        self.tabla.resize(self.filas+4, self.columnas+4);
        self.tabla.set_homogeneous(True);
        self.tabla.show();
        
        
        self.x = 0;
        self.y = 0;
        for i in range(self.filas):
            for j in range(self.columnas):
                #Creamos imágenes y las añadimos al tablero
                self.img_desactivado = gtk.Image();
                self.img_desactivado.set_from_file(self.ruta_desactivado); 
                self.img_desactivado.set_name("desactivado");
                self.img_desactivado.show();
                self.name = str(i)+"--"+str(j);
                self.img_desactivado.set_name(self.name);
                #EventBox sirve para poder controlar los eventos de click en la imagen
                self.event_box = gtk.EventBox();
                self.event_box.add(self.img_desactivado);
                self.event_box.connect('button-press-event',self.golpeo);
                self.event_box.show();
                #Las posiciones se indican así para poder dejar un marco de 2 filas y 2 columnas tanto a derecha como izquierda
                self.tabla.attach(self.event_box,self.x+2,self.x+3,self.y+2,self.y+3);
                self.x +=1;
            self.x = 0;
            self.y +=1;
            
        #Eventos
        self.interfaz.connect_signals(self);
        
        
    #Evento de cierre de ventana  
    def on_ventana_delete_event(self,widget,data = None):
        gtk.main_quit();
        
    #Evento de click en imagen de tablero
    def golpeo(self,widget,data = None):
        image_hijo = widget.get_child();
        if image_hijo.get_name() == "desactivado":
            image_hijo.set_from_file(self.ruta_desactivado);
            image_hijo.set_name("activado");
        else:
            image_hijo.set_from_file(self.ruta_activado);
            image_hijo.set_name("desactivado");
        
        
if __name__ == '__main__':
    ruta_boton = "iconos\refresh.png";
    ruta_desactivado = "iconos\desactivado.png";
    ruta_activado = "iconos\activo.png";
    practica = Practica(10,10,ruta_desactivado,ruta_activado,ruta_boton);
    gtk.main();