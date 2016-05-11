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
        self.fila = filas;
        self.columna = columnas;
        self.historial = [];
        self.puntuacion = 0;#Contador de puntuacion realizados
        self.ronda = 0#Contador de la ronda actual
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
        '''self.image_refresh = gtk.Image();
        self.image_refresh.set_from_file(self.ruta_boton);        
        self.btn_deshacer.set_image(self.image_refresh);'''
        self.btn_deshacer.set_label("Deshacer jugada");
        self.btn_deshacer.connect("clicked",self.deshacer_jugada);
        #Acceso a la etiqueta que muestra los puntuacion actuales
        self.lbl_toques = self.interfaz.get_object("lbl_toques");
        self.lbl_toques.set_text("Toques realizados:\n"+str(self.puntuacion));
        
        #Acceso al tablero
        self.tabla = self.interfaz.get_object("tbl_tablero");
        self.tabla.resize(self.filas, self.columnas);
        self.tabla.set_homogeneous(True);
        self.tabla.show();
        
        self.tablero = [];
        #Tablero de juego
        self.crear_tablero(self.filas,self.columnas);
        #Bordes del tablero
        #self.bordes_tablero(self.filas,self.columnas);
        #Volcamos la tabla en el array
        self.tablero = self.tabla.get_children();              
        #Conexi�n a eventos
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
        self.realizar_golpe(int(coordenadas_separadas[0]), int(coordenadas_separadas[1]), self.columna);                       
        self.historial.insert(self.puntuacion, coordenadas);
        #Aumentamos los toques dados
        self.puntuacion +=1; 
        self.ronda +=1;     
        self.lbl_toques.set_text("Toques realizados:\n"+str(self.puntuacion));
        
    def realizar_golpe(self,fila,columna,posicion):
        #Columna central 
        self.modificar_posicion5(fila, columna,0);
        #Columna izquierda grande
        self.modificar_posicion5(fila, columna,posicion);
        #Columna derecha grande
        self.modificar_posicion5(fila, columna,-posicion);
        #Columna izquierda pequeña
        self.modificar_posicion3(fila, columna,posicion*2);
        #Columna derecha pequeña
        self.modificar_posicion3(fila, columna,-posicion*2);
    #Tablero de juego
    def crear_tablero(self,filas,columnas):
        for i in range(2,self.filas-2):
            for j in range(2,self.columnas-2):
                #Creamos im�genes y las a�adimos al tablero
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

    #Metodo que a partir de las coordenadas del tablero te indica en que posicon de la lista se encuentra
    def posicion_tablero(self,fila,columna):
        elemento = str(fila) + "." + str(columna)
        for i in range(0,len(self.tablero)):
            if(self.tablero[i].get_name() == str(elemento)):
                return i
            
    
    #Metodo que a partir de una posicion de tablero camba esa posicion y las dos inferiores y superiores a ella
    def modificar_posicion5(self,fila,columna,posicion):
        a = self.posicion_tablero(fila, columna)+ posicion;
        if (a<self.fila*self.columna and a>= 0):
            self.comprobar_posicion(fila, columna,a);
            if (self.metodo_prueba(fila, columna, 1)< self.columnas-4 and self.metodo_prueba(fila, columna, 1) >= 0 ):
                self.comprobar_posicion(fila, columna,a+1);
            if (self.metodo_prueba(fila, columna, -1)< self.columnas-4 and self.metodo_prueba(fila, columna, -1) >= 0 ):
                self.comprobar_posicion(fila, columna,a-1);
            if (self.metodo_prueba(fila, columna, 2)< self.columnas-4 and self.metodo_prueba(fila, columna, 2) >= 0 ):
                self.comprobar_posicion(fila, columna,a+2);
            if (self.metodo_prueba(fila, columna, -2)< self.columnas-4 and self.metodo_prueba(fila, columna, -2) >= 0 ):
                self.comprobar_posicion(fila, columna,a-2);
        
        print self.posicion_tablero(fila, columna)
        
    #Metodo que a parir de una posicion de tablero cmbia esa posicion y la inferior y superior
    def modificar_posicion3(self,fila,columna,posicion):
        a = self.posicion_tablero(fila, columna)+ posicion;
        if (a<self.fila*self.columna and a>= 0):
            self.comprobar_posicion(fila, columna,a);
            if (self.metodo_prueba(fila, columna, 1)< self.columnas-4 and self.metodo_prueba(fila, columna, 1) >= 0 ):
                self.comprobar_posicion(fila, columna,a+1);
            if (self.metodo_prueba(fila, columna, -1)< self.columnas-4 and self.metodo_prueba(fila, columna, -1) >= 0 ):
                self.comprobar_posicion(fila, columna,a-1);
            
        
        print self.posicion_tablero(fila, columna)
    
    
    #Metodo que reduce la casilla del array a un numero menor que el de sus filas para poder comprobarlo depues
    
    def metodo_prueba(self,fila,columna,variable):
        a = self.posicion_tablero(fila, columna)
        while (a >= self.columna):
            a = a - self.columna
        print a+variable
        return a+variable
    #M�todo que genera la cruz de 'x' en el tablero en funci�n de la posici�n pasada como par�metro
    def comprobar_posicion(self,fila,columna,bandera):
        imagen_actual = self.tablero[bandera].get_child(); 
        estado_imagen = self.tablero[bandera].get_child().get_name();
        if estado_imagen == "desactivado":       
            imagen_actual.set_from_file(self.ruta_activado);
            imagen_actual.set_name("activado");
        else:
            imagen_actual.set_from_file(self.ruta_desactivado);
            imagen_actual.set_name("desactivado");  
             
    #M�todo que inicia la matriz de juego(tablero) con puntos
    def iniciar_tablero(self,tablero):
        for i in range(self.filas):
            tablero.append([]);   
            for j in range (self.columnas):
                tablero[i].append(".");
    '''Método que deshará la jugada actual del jugador.
    Deberá volver a un estado anterior siempre que el actual no sea el primer turno de juego.
    '''
    def deshacer_jugada(self,widget,data = None):
        if  len(self.historial)>0 and self.ronda>0:       
            peticion=self.historial[self.ronda-1];
            peticion_separada = peticion.split(".");
            numero_fila= int(peticion_separada[0]);
            numero_columna = int(peticion_separada[1]);
            self.realizar_golpe(numero_fila, numero_columna, self.columna);
            self.historial.remove(peticion)
            self.ronda -=1
        else:
            dialog = gtk.MessageDialog(self.ventana,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,"No se puede deshacer la jugada actual");
            response = dialog.run();  
            if response == gtk.RESPONSE_OK:
                dialog.destroy();
if __name__ == '__main__':
    ruta_boton = "iconos\refresh.png";
    ruta_desactivado = "iconos\desactivado.png";
    ruta_activado = "iconos\activado.png";
    ruta_borde = "iconos\borde.png";
    practica = Practica(5,5,ruta_desactivado,ruta_activado,ruta_boton,ruta_borde);
    gtk.main();