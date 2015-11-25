#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random
fin_de_juego = False
pilas = pilasengine.iniciar(ancho=1024,alto=512)
a=pilas.fondos.Fondo("mapa.png")
def salir():
    exit()
def iniciar_juego():
    menu.y=30000  
    a.eliminar()
    pilas.actores.MapaTiled('Mapa.tmx')
    puntos = pilas.actores.Puntaje(x=400, y=170)
    cajas = []    
    class SoftwareLibre(pilasengine.actores.Actor):
        def iniciar(self):
            self.imagen = "Ubuntu.png"
        def actualizar(self):
            self.escala=.5
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
    def chau(disparo, enemigo):
        enemigo.aprender(pilas.habilidades.PuedeExplotar)
        enemigo.eliminar()
        puntos.aumentar()
        puntos.escala=[1,0,3,1]
        disparo.aprender(pilas.habilidades.PuedeExplotarConHumo)
        disparo.eliminar()
    man=SoftwareLibre(pilas)
    man.aprender("RotarConMouse")
    man.aprender("moverseComoCoche")
    man.aprender("Disparar",municion=SoftwareLibre, grupo_enemigos=cajas, cuando_elimina_enemigo=chau, frecuencia_de_disparo=4)
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
        puntos.x=100
        puntos.y=-100
        puntos.escala=[1,0,1]
        textot = pilas.actores.Texto("PERDISTE")
        textot.escala=[3,0,1]
        texto = pilas.actores.Texto("Tu puntaje es ")
        texto.escala=1 
        texto.y=-100
    pilas.colisiones.agregar(man, cajas, finalizar_juego)
menu=pilas.actores.Menu(
        [
            ('INICIAR JUEGO', iniciar_juego),
            ('SALIR', salir),
        ])
menu.x = [-300, 300,-200, 200,-100, 100, 0]
pilas.ejecutar()