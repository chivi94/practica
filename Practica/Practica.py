#-*- encoding: utf-8 -*-
'''
Created on 4 de may. de 2016
@author: Antonio Roman Lopez
         Ivan Gonzalez Rincon
'''
import gtk
import random

class Practica:
    
    #Constructor
    def __init__(self,filas, columnas,ruta_desactivado,ruta_activado,ruta_boton,ruta_fichero):
        #Atributos de la clase
        self.nivel = 0;
        self.ruta_boton = ruta_boton;
        self.ruta_desactivado = ruta_desactivado;
        self.ruta_activado = ruta_activado;
        self.ruta_fichero = ruta_fichero;
        self.filas = filas+4;
        self.columnas = columnas+4;
        self.fila = filas;
        self.columna = columnas;
        self.letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
        self.puntuaciones_iniciales = []
        self.historial = [];
        self.tablero = [];
        self.tablero_inicial=[]; 
        self.puntuacion = 0;#Contador de puntuacion realizados
        self.ronda = 0#Contador de la ronda actual
        #Inicio de la interfaz
        self.inicia_interfaz();
        
    #Metodo que accede a los componentes gráficos que se van a usar en la aplicación
    def inicia_interfaz(self):
        #Acceso a la interfaz
        self.interfaz = gtk.Builder();
        self.interfaz.add_from_file('practica.glade');
        self.interfaz.connect_signals(self);    
        #Acceso a los componentes
        #Imagenes de los botones
        self.image_desactivado = gtk.Image();
        self.image_desactivado.set_from_file(self.ruta_desactivado);        
        self.image_activado = gtk.Image();
        self.image_activado.set_from_file(self.ruta_activado);
        #Ventana
        self.ventana = self.interfaz.get_object("wd_ventana");
        self.ventana.resize(200,200);
        self.ventana.set_title("Diglett Mole");
        #Dialogo de peticion de nivel
        self.dlg_nivel = self.interfaz.get_object("dlg_nivel");
        self.dlg_nivel.set_title("Seleccione nivel");
        self.txt_box_nivel = self.interfaz.get_object("txtbox_nivel");
        self.bttn_ok = self.interfaz.get_object("bttn_ok");
        self.bttn_ok.connect("clicked",self.on_dlg_lvl_bttn_clicked);
        self.bttn_cancel = self.interfaz.get_object("bttn_cancel");
        self.bttn_cancel.connect("clicked",self.on_dlg_lvl_bttn_clicked);
        #Acceso al boton de retroceso
        self.btn_deshacer = self.interfaz.get_object("bttn_deshacer");
        self.btn_deshacer.set_size_request(64,64);
        self.image_refresh = gtk.Image();
        self.image_refresh.set_from_file(self.ruta_boton);        
        self.btn_deshacer.set_image(self.image_refresh);      
        self.btn_deshacer.connect("clicked",self.deshacer_jugada);
        #Acceso a la etiqueta que muestra los toques actuales
        self.lbl_toques = self.interfaz.get_object("lbl_toques");
        self.lbl_toques.set_text("Toques realizados:\n"+str(self.puntuacion));
        #Acceso a la etiqueta que muestra la puntuación máxima del nivel actual
        self.lbl_punt_max = self.interfaz.get_object("lbl_max_punt");    
        #Acceso al tablero
        self.tabla = self.interfaz.get_object("tbl_tablero");
        self.tabla.resize(self.filas, self.columnas);
        self.tabla.set_homogeneous(True);
        self.tabla.show();   
        #Iniciamos el dialogo de peticion de nivel
        self.dlg_nivel.run();   
    
    #Método que crea de forma dinámica el diálogo donde se mostrarán las puntuaciones.
    def crea_dlg_punt(self):
        #Dialogo de puntuaciones
        self.dlg_puntuaciones = gtk.Dialog();
        self.dlg_puntuaciones.connect("destroy",self.on_dlg_puntuaciones_delete_event);
        self.dlg_puntuaciones.set_title("Puntuaciones almacenadas");
        self.dlg_puntuaciones.set_border_width(0);
        self.dlg_puntuaciones.set_size_request(300, 300);
        self.scrolled_window = gtk.ScrolledWindow();
        self.scrolled_window.set_border_width(10);
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS);
        self.dlg_puntuaciones.vbox.pack_start(self.scrolled_window, gtk.TRUE, gtk.TRUE, 0);
        self.lbl_puntuaciones_fichero = gtk.Label();
        self.scrolled_window.add_with_viewport(self.lbl_puntuaciones_fichero);
        self.lbl_puntuaciones_fichero.show();
        self.scrolled_window.show();
        #Leemos las puntuaciones
        self.leer_puntuaciones(self.ruta_fichero,self.lbl_puntuaciones_fichero,0);
        
    #Eventos    
    #Evento de cierre de ventana  
    def on_ventana_delete_event(self,widget,data = None):
        gtk.main_quit();
    
    #Evento de cierre de diálogo de petición de nivel
    def on_dlg_nivel_delete_event(self,widget,data = None):
        self.dlg_nivel.hide();
    #Evento de cierre de diálogo de puntuaciones        
    def on_dlg_puntuaciones_delete_event(self,widget,data = None):
        self.dlg_puntuaciones.destroy();
    #Evento que controla el click de los botones del diálogo de petición de nivel
    def on_dlg_lvl_bttn_clicked(self,widget,data = None):
        try:
            texto_boton=widget.get_label();
            if texto_boton == "Ok":
                nivel = self.txt_box_nivel.get_text();
                if nivel != "" and int(nivel)> 0:
                    self.iniciar_nivel(nivel,0);
                    self.dlg_nivel.hide();
                    if self.ventana.get_visible() == False:
                        self.ventana.show();
                else:
                    self.crear_dialogo("Introduzca nivel válido",gtk.MESSAGE_ERROR);
            elif texto_boton == "Cancelar":
                self.txt_box_nivel.set_text("");
                self.dlg_nivel.hide();
                if self.ventana.get_visible() == False:
                    gtk.main_quit();
        except ValueError:
            self.crear_dialogo("Entrada no válida",gtk.MESSAGE_ERROR);
    #Evento que controla el apartado de menú: Archivo -> Nuevo nivel             
    def on_img_menu_nuevo_activate(self,widget,data = None):
        self.txt_box_nivel.has_focus();
        self.dlg_nivel.run();
    #Evento que controla el apartado de menú: Archivo -> Reiniciar nivel
    def on_img_menu_reiniciar_activate(self,widget, data = None):
        self.iniciar_nivel(self.nivel,1);
        
    #Evento que controla el apartado de menú: Archivo -> Puntuaciones
    def on_img_menu_puntuaciones_activate(self,widget, data = None):        
        self.crea_dlg_punt();      
        self.dlg_puntuaciones.show();
    
    #Evento que controla el apartado de menú: Archivo -> Salir 
    def on_img_menu_salir_activate(self,widget, data = None):
        gtk.main_quit();
        
    #Evento que controla el apartado de menú: Ayuda -> Información
    def on_img_menu_info_activate(self,widget,data = None):
        self.crear_dialogo("El objetivo del juego consiste en limpiar el tablero de digletts,\n"
        +"de forma que estén todos escondidos",gtk.MESSAGE_INFO);
        
    #Evento que controla el click sobre el tablero
    def golpeo(self,widget,data = None):
        #Coordenadas del elemento sobre el que se ha hecho click
        coordenadas = widget.get_name();
        #Hacemos split para poder acceder a fila y columna
        coordenadas_separadas = coordenadas.split(".");
        self.realizar_golpe(int(coordenadas_separadas[0]), int(coordenadas_separadas[1]), self.columna);                       
        self.historial.insert(self.puntuacion, coordenadas);
        #Aumentamos los toques dados
        self.puntuacion +=1; 
        self.ronda +=1;     
        self.lbl_toques.set_text("Toques realizados:\n"+str(self.puntuacion));
        completado=self.tablero_completado();
        if completado:
            self.crear_dialogo("!Tablero completado¡",gtk.MESSAGE_INFO);
            try:
                self.comprobar_puntuaciones(self.nivel, self.puntuacion, ruta_fichero);
            except IOError:
                self.formato_puntuaciones(self.puntuaciones_iniciales);
                self.iniciar_fichero(self.puntuaciones_iniciales,self.ruta_fichero);
                self.comprobar_puntuaciones(self.nivel, self.puntuacion,ruta_fichero);
            finally:                
                self.ventana.hide();
                self.dlg_nivel.run();
                
    #Método que realiza un golpe sobre el tablero.
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
    
    #Metodo que comprobará si se ha completado el tablero
    def tablero_completado(self):
        contador = 0
        for i in range(self.fila*self.columna):
            estado_imagen = self.tablero[i].get_child().get_name();
            print estado_imagen;
            if estado_imagen == "activado":
                contador+=1;
        #Si todo el tablero esta desactivado, el programa termina
        if contador == 0:
            return True
        #En caso contrario, continua
        else:
            return False
       
    
    #Método que se encarga de iniciar el juego con el nivel pasado como argumento
    def iniciar_nivel(self,nivel,flag):
        self.ronda = 0;
        self.nivel = int(nivel);
        self.crear_tablero(self.filas, self.columnas);
        self.tablero = self.tabla.get_children();
        #Si se pasa un 0, se esta haciendo un nivel nuevo
        if flag == 0:
            self.crear_nivel(int(nivel));
            
        #Si se pasa un 1, se esta reiniciando un nivel
        elif flag ==1:
            for elemento in self.tablero_inicial:
                posicion = elemento.split(".");
                self.realizar_golpe(posicion[0],posicion[1], self.columna);
        self.txt_box_nivel.set_text("");
        self.puntuacion = 0;
        self.lbl_toques.set_text("Toques realizados:\n"+str(self.puntuacion));
        self.historial = [];
        #Mostramos en la etiqueta correspondiente la puntuación máxima de ese nivel
        self.leer_puntuaciones(self.ruta_fichero, self.lbl_punt_max, self.nivel);
    #Método que modifica el tablero en función del nivel pasado como argumento
    def crear_nivel(self,nivel):
        posicion = 0;
        self.tablero_inicial=[];
        while(nivel > 0):
            a = random.randint(2,self.fila+1)
            b = random.randint(2,self.columna+1)
            self.tablero_inicial.insert(posicion, str(a)+"."+str(b));
            self.realizar_golpe(a,b, self.columna);
            posicion +=1;
            nivel = nivel-1;
            
    #Método que crea un cuadro diálogo con la información pasada como argumentos
    def crear_dialogo(self,texto,icono):
        dialog = gtk.MessageDialog(self.ventana,0,icono,gtk.BUTTONS_OK,texto);
        response = dialog.run();  
        if response == gtk.RESPONSE_OK:
            dialog.destroy();
    #Método que crea el tablero de juego
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

    #Metodo que a partir de las coordenadas del tablero indica en que posición de la lista se encuentra
    def posicion_tablero(self,fila,columna):
        elemento = str(fila) + "." + str(columna)
        for i in range(0,len(self.tablero)):
            if(self.tablero[i].get_name() == str(elemento)):
                return i
            
    
    #Método que a partir de una posición dada del tablero, cambia tanto esa posición como las dos inferiores y superiores a ella.
    def modificar_posicion5(self,fila,columna,posicion):
        a = self.posicion_tablero(fila, columna)+ posicion;
        if (a<self.fila*self.columna and a>= 0):
            self.comprobar_posicion(fila, columna,a);
            if (self.reducir_casilla(fila, columna, 1)< self.columnas-4 and self.reducir_casilla(fila, columna, 1) >= 0 ):
                self.comprobar_posicion(fila, columna,a+1);
            if (self.reducir_casilla(fila, columna, -1)< self.columnas-4 and self.reducir_casilla(fila, columna, -1) >= 0 ):
                self.comprobar_posicion(fila, columna,a-1);
            if (self.reducir_casilla(fila, columna, 2)< self.columnas-4 and self.reducir_casilla(fila, columna, 2) >= 0 ):
                self.comprobar_posicion(fila, columna,a+2);
            if (self.reducir_casilla(fila, columna, -2)< self.columnas-4 and self.reducir_casilla(fila, columna, -2) >= 0 ):
                self.comprobar_posicion(fila, columna,a-2);
        
        print self.posicion_tablero(fila, columna)
        
    #Método que a partir de una posición dada, cambia tanto es posición como la inferior y superior a ella.
    def modificar_posicion3(self,fila,columna,posicion):
        a = self.posicion_tablero(fila, columna)+ posicion;
        if (a<self.fila*self.columna and a>= 0):
            self.comprobar_posicion(fila, columna,a);
            if (self.reducir_casilla(fila, columna, 1)< self.columnas-4 and self.reducir_casilla(fila, columna, 1) >= 0 ):
                self.comprobar_posicion(fila, columna,a+1);
            if (self.reducir_casilla(fila, columna, -1)< self.columnas-4 and self.reducir_casilla(fila, columna, -1) >= 0 ):
                self.comprobar_posicion(fila, columna,a-1);
            
        
        print self.posicion_tablero(fila, columna)
    
    
    #Metodo que reduce la casilla del array a un numero menor que el de sus filas para poder comprobarlo depues 
    def reducir_casilla(self,fila,columna,variable):
        a = self.posicion_tablero(fila, columna)
        while (a >= self.columna):
            a = a - self.columna
        print a+variable
        return a+variable
    
    #Método que comprueba el estado de la imagen dentro del tablero para modificarla.
    def comprobar_posicion(self,fila,columna,bandera):
        imagen_actual = self.tablero[bandera].get_child(); 
        estado_imagen = self.tablero[bandera].get_child().get_name();
        if estado_imagen == "desactivado":       
            imagen_actual.set_from_file(self.ruta_activado);
            imagen_actual.set_name("activado");
        else:
            imagen_actual.set_from_file(self.ruta_desactivado);
            imagen_actual.set_name("desactivado");  
             
    #Método que deshace la jugada actual, siempre que no sea la primera del nivel.
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
            self.crear_dialogo("No se puede deshacer la jugada actual",gtk.MESSAGE_ERROR);
            
    
    #Método que lee las puntuaciones del fichero
    def leer_puntuaciones(self,ruta,label,nivel):
        try:
            fichero = open(ruta,"r");
            #En este caso, cargamos las puntuaciones en el dialogo que muestra todas las puntuaciones
            if nivel == 0:
                label.set_text("");
                for linea in fichero:
                    punt = linea.split(":");
                    nivel_guardado = punt[0];
                    toques_nivel =punt[1];
                    label.set_text(label.get_text()+"\n"+
                                   "Nivel:"+nivel_guardado+
                                   " Puntuación:"+toques_nivel+"\n");
            #En este otro caso, mostramos la puntuación del nivel actual al jugador en la etiqueta inferior izquierda de la interfaz
            else:
                for linea in fichero:
                    punt = linea.split(":")
                    nivel_guardado = int(punt[0])
                    toques_nivel =int(punt[1])       
                    if nivel_guardado == nivel: 
                        label.set_text("Nivel actual:"+str(nivel)+
                                   "\nPuntuación:"+str(toques_nivel));
                        break;
            fichero.close();
        except IOError:
            self.crear_dialogo("Aún no hay puntuaciones guardadas. Se crearán cuando se complete un nivel",gtk.MESSAGE_INFO);
            if label.get_name() == "lbl_max_punt":
                label.set_text("Nivel actual:"+
                                    "\nPuntuación:");
    #Método que modificará el fichero, si conviene.              
    def comprobar_puntuaciones(self,nivel,puntuacion,ruta):
        fichero = open(ruta,"r")
        lineas = []
        for linea in fichero:
            punt = linea.split(":")
            nivel_guardado = int(punt[0])
            toques_nivel =int(punt[1])
        
            if (toques_nivel > puntuacion) and (nivel_guardado == nivel) and (puntuacion>0): 
                nueva_puntuacion = str(nivel_guardado)+":"+str(puntuacion)
                self.crear_dialogo("¡Puntuación mejorada!"+
                                   "\nPuntuación anterior:"+str(toques_nivel)+
                                   "\nPuntuación actual"+str(puntuacion),gtk.MESSAGE_INFO);
            else:
                nueva_puntuacion = str(nivel_guardado)+":"+str(toques_nivel) 
            lineas.append(nueva_puntuacion)
        fichero.close()
        #Volcamos el array con las nuevas puntuaciones
        fichero = open(ruta,"w")
        for linea in lineas:
            fichero.write(linea)
            fichero.write("\n")
        fichero.close()  

    #Método que inicia un array con el formato usado para almacenar las puntuaciones
    def formato_puntuaciones(self,puntuaciones):
        for i in range (1,len(self.letras)+1):
            puntuaciones.append(str(i)+":"+str(50))

    #Método que inicia el fichero de puntuaciones si dicho fichero no existe
    def iniciar_fichero(self,puntuaciones,ruta):
        #Volcamos el array con las nuevas puntuaciones
        fichero = open(ruta,"w")
        for puntuacion in puntuaciones:
            fichero.write(puntuacion)
            fichero.write("\n")
        fichero.close()
if __name__ == '__main__':
    ruta_fichero = "puntuaciones.txt";
    ruta_boton = ".//iconos//refresh.png";
    ruta_desactivado = ".//iconos//desactivado.png";
    ruta_activado = ".//iconos//activado.png";
    practica = Practica(10,10,ruta_desactivado,ruta_activado,ruta_boton,ruta_fichero);
    gtk.main();