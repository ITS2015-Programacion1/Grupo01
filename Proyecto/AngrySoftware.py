#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random
fin_de_juego = False
pilas = pilasengine.iniciar(ancho=1024,alto=468)

 

class opciones(pilasengine.escenas.Escena):
    fondoDelMenu=pilas.fondos.Fondo("Mapa.png")
    fondoDelMenu.x= [0, 2000]
    b = pilas.interfaz.Boton("Dificultad")
    def opcionesdedificultad():
        def cuando_selecciona(opcion_seleccionada):
            pilas.avisar("Ha seleccionado la opcion: " + opcion_seleccionada)
        opcion = pilas.interfaz.ListaSeleccion(['facil','dificil'], cuando_selecciona)
        opcion.y = -30
    b.conectar(opcionesdedificultad)

    

class iniciarjuego(pilasengine.escenas.Escena):
    def iniciarjueguito():
        fondoDelJuego = pilas.actores.MapaTiled('Mapa.tmx')
        puntos = pilas.actores.Puntaje(x=400, y=170)
        cajas = []    
        class SoftwareLibre(pilasengine.actores.Actor):
            def iniciar(self):
                self.imagen = "Ubuntu.png"
            def actualizar(self):
                self.escala=.5
                self.aprender("EliminarseSiSaleDePantalla")
        class Windows(pilasengine.actores.Actor):
            def iniciar(self):
                self.imagen = "Windows.png"
            def actualizar(self):
                rectangulo = pilas.fisica.Rectangulo(0, 0, 60, 50, sensor=True, dinamica=False)
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
        man=SoftwareLibre(pilas)    
        rad = pilas.fisica.Rectangulo(0, 0, 70, 70, sensor=True, dinamica=False)
        man.aprender(pilas.habilidades.Imitar,rad)
        man.aprender("moverseComoCoche")
        man.aprender("Disparar",municion=SoftwareLibre, grupo_enemigos=cajas, cuando_elimina_enemigo=eliminar_enemigo, frecuencia_de_disparo=1)
        man.x= 0 
        man.y= 0
        pilas.actores.vincular(Windows)
        def finalizar_juego():
            global fin_de_juego
            fin_de_juego = True
            for s in range(2):
                sonido_de_explosion = pilas.sonidos.cargar('explosion.wav')
                sonido_de_explosion.reproducir()
            for enemigo in cajas:
                enemigo.eliminar()
            man.aprender(pilas.habilidades.PuedeExplotar)
            man.eliminar()
            enemigo.eliminar()
            T=pilas.actores.Texto("JAMAS PODRAS CONTRA EL IMPERIO DEL SOFTWARE ROBADOOO!!!")
            T.escala=[0,3,0]
        pilas.colisiones.agregar(man, cajas, finalizar_juego)
class Menu(pilasengine.escenas.Escena):
    def salir(self):
        exit()
    def opciones(self):
        pilas.escenas.opciones()
    def iniciar_juego(self):
        pilas.escenas.iniciarjuego()
    def iniciar(self):
        fondoDelMenu=pilas.fondos.Fondo("Mapa.png")
        self.menu=pilas.actores.Menu([('INICIAR JUEGO', self.iniciar_juego),('OPCIONES', self.opciones),('SALIR', self.salir) ])
        self.menu.x = [-300,200,-100,0]

    
pilas.escenas.vincular(Menu)
pilas.escenas.vincular(opciones)
pilas.escenas.vincular(iniciarjuego)

pilas.escenas.Menu()
    
pilas.ejecutar()