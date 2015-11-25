#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random
fin_de_juego = False
pilas = pilasengine.iniciar(ancho=1024,alto=768)

class EscenaMenu(pilasengine.escenas.Escena):
    def iniciar(self):
        #Contenido de la escena principal: logo, menu...
        self.fondo = self.pilas.fondos.Fondo("Mapa.png")
        self.menu_inicial()
    def menu_inicial(self):
        #creamos opciones
        OpcionesDelMenu = [
            ("INICIAR JUEGO", self.iniciar_juego),
            ("OPCIONES", self.opciones),
            ("SALIR", self.salir)
        ]
        self.menu = self.pilas.actores.Menu(OpcionesDelMenu, y = 0)
        self.musica_menu = pilas.musica.cargar('1.mp3')
        self.musica_menu.reproducir()
        
    def iniciar_juego(self):
        self.pilas.escenas.IniciarJuego()
        self.musica_menu.detener()
        self.musica_juego = pilas.musica.cargar('2.mp3')
        self.musica_juego.reproducir()

        
    
    def opciones(self):
        self.pilas.escenas.Opciones()

    def salir(self):
        exit()
    
class IniciarJuego(pilasengine.escenas.Escena):
    def iniciar(self):
        fondoDelJuego = pilas.actores.MapaTiled('mapita.tmx')
        fondoDelJuego.escala= 1
        puntos = pilas.actores.Puntaje(x=400, y=170)
        cajas = []
        class Apple(pilasengine.actores.Actor):
            def iniciar(self):
                self.imagen="a.png"
            def actualizar(self):
                self.escala = .5
                if pilas.control.izquierda:
                    self.figura.velocidad_x = -10
                    self.espejado = True
                elif pilas.control.derecha:
                    self.figura.velocidad_x = 10
                    self.espejado = False
                else:
                    self.figura.velocidad_x = 0
                if pilas.control.arriba:
                    self.figura.velocidad_y = 10
                elif pilas.control.abajo:
                    self.figura.velocidad_y = -10
                else:
                    self.figura.velocidad_y = 0
                self.y = self.figura.y
                self.x = self.figura.x
                def controles(self):
                	teclitas = {
                	pilas.simbolos.a: 'izquierda',
            		pilas.simbolos.d: 'derecha',
            		pilas.simbolos.w: 'arriba',
            		pilas.simbolos.s: 'abajo',
            		pilas.simbolos.ESPACIO: 'boton',
        			}
                	mi_control = pilas.control.Control(teclitas)
                	self.aprender(pilas.habilidades.MoverseConElTeclado, control=mi_control)
            	


                
        class SoftwareLibre(pilasengine.actores.Actor):
            def iniciar(self):
                self.imagen = "Ubuntu.png"
            def actualizar(self):
                self.escala=.3
                
        class Windows(pilasengine.actores.Actor):
            def iniciar(self):
                self.imagen = "Windows.png"
            def actualizar(self):
                rectangulo = pilas.fisica.Rectangulo(0, 0, 60, 50, sensor=True, dinamica=True)
                self.figura_de_colision = rectangulo

                
        class Perseguir(pilasengine.habilidades.Habilidad):
            def iniciar(self, receptor, actor_perseguido, velocidad):
                self.receptor = receptor
                self.otro = actor_perseguido
                self.velocidad = velocidad
                x_pos=random.randint(0,1)
                y_pos=random.randint(0,1)
                y_delta = random.randrange(200, 300)
                x_delta = random.randrange(200, 300)
                if x_pos == 0:
                    self.receptor.x = self.otro.x + x_delta
                if x_pos == 1:
                    self.receptor.x = self.otro.x - x_delta
                if y_pos == 0:
                    self.receptor.y = self.otro.y + y_delta
                if y_pos == 1:
                    self.receptor.y = self.otro.y - y_delta
            def actualizar(self):
                if self.receptor:
                    if self.receptor.x > self.otro.x:                
                        self.receptor.x -= self.velocidad
                    else:
                        self.receptor.x += self.velocidad

                    if self.receptor.y > self.otro.y:
                        self.receptor.y -= self.velocidad
                    else:
                        self.receptor.y += self.velocidad
        pilas.habilidades.vincular(Perseguir)
        def crear_caja():
            enemigo = Windows(pilas)
            enemigo.aprender("Perseguir", man, 1)
            enemigo.escala = 1
            enemigo.aprender("LimitadoABordesDePantalla")
            cajas.append(enemigo)
            if fin_de_juego:
                return False
            else:
                return True
        TCW = pilas.tareas.agregar(1, crear_caja)


        def eliminar_enemigo(disparo, enemigo):
            enemigo.aprender(pilas.habilidades.PuedeExplotar)
            enemigo.eliminar()
            puntos.aumentar()
            puntos.escala=[1,0,3,1]
            disparo.aprender(pilas.habilidades.PuedeExplotarConHumo)
            disparo.eliminar()
        man=Apple(pilas)   
        rad = pilas.fisica.Rectangulo(0, 0, 70, 70, sensor=True, dinamica=False)
        man.aprender(pilas.habilidades.Imitar,rad)
        man.aprender("moverseComoCoche")
        man.aprender("Disparar",municion=SoftwareLibre, grupo_enemigos=cajas, cuando_elimina_enemigo=eliminar_enemigo, frecuencia_de_disparo=2)
        man.x= 0 
        man.y= 0
        pilas.actores.vincular(Windows)
        def finalizar_juego():
            global fin_de_juego
            fin_de_juego = True
            for s in range(2):
                sonido_de_explosion = pilas.sonidos.cargar('explosion.wav')
                sonido_de_explosion.reproducir()
            self.sonido_final = pilas.musica.cargar('3.mp3')
            self.sonido_final.reproducir()
            for enemigo in cajas:
                enemigo.eliminar()
            man.aprender(pilas.habilidades.PuedeExplotar)
            man.eliminar()
            enemigo.eliminar()
            T=pilas.actores.Texto("JAMAS PODRAS CONTRA EL IMPERIO DEL SOFTWARE ROBADOOO!!!")
            T.escala=[0,3,0]
        pilas.colisiones.agregar(man, cajas, finalizar_juego) 
    
class Opciones(pilasengine.escenas.Escena):
    def iniciar(self):
        self.fondo = self.pilas.fondos.Fondo("Mapa.png")
        self.fondo.x = [0,2000]
        self.b = pilas.interfaz.Boton("Dificultad")
        def moverse():
            self.b.escala_x = [  2, 0.8, 1], 0.15
            self.b.escala_y = [0.8, 2,   1], 0.1
            self.d = pilas.azar(-50, 50)
            self.b.rotacion = [d, 1], 0.1
        self.b.conectar(moverse)
        def d():
            def cuando_selecciona(opcion_seleccionada):
                pilas.escenas.EscenaMenu()
            opcion = pilas.interfaz.ListaSeleccion(['facil', 'media', 'dificil'], cuando_selecciona)
            opcion.y = -40
        self.b.conectar(d)
        
        
        
        
pilas.escenas.vincular(IniciarJuego)
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(Opciones)
pilas.escenas.EscenaMenu()
pilas.ejecutar()