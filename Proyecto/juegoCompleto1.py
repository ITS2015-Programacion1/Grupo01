#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine


class FondoConMovimiento(pilasengine.fondos.Fondo):

    def iniciar(self):
        self.imagen = 'Mapa.png'  # definir imagen
        self.velocidad = 1  # velocidad a la que se movera el fondo

    def actualizar(self):
        self.x -= self.velocidad  # mover hacia la izquierda

        # Si el fondo llega al borde izquierdo de la pantall
        # entonces cambiar su posicion en X
                # Si el fondo llega al borde izquierdo de la pantall
        # entonces cambiar su posicion en X
        if self.x + self.ancho <= 0:
            self.x = self.ancho

class Tubo(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = 'Ubuntu.png'  # definir imagen
        self.velocidad = 1  # velocidad con la que se movera el tubo
        self.x = 288  # posicion en X en la que aparecera

        # posicion en Y aleatoria entre 159 y 250
        self.y = self.pilas.azar(50, 200)
        #puntos.escala=[1, 0, 5, 1], .1
        #puntos.aumentar(1)

    def actualizar(self):
        self.x -= self.velocidad  # mover tubo constantemente

        # Si el tubo llega al al borde izquierdo de la pantalla
        # entonces lo eliminamos
        if self.x + self.ancho <= -144:
             self.eliminar()

def crear_tubos():
# funcion que sera llamada como una tarea
    tubo1 = Tubo(pilas)
    tubo2 = Tubo(pilas)
    tubo2.rotacion = 180
    tubo2.y = tubo1.y - (tubo1.alto / 2) * 2 - 100

pilas = pilasengine.iniciar(ancho=288, alto=511)
# Crear fondo 1 con posicion en X de 288 (no visible)
fondo55 = FondoConMovimiento(pilas)
fondo55.x = 288
# Crear fondo 2
fondo22 = FondoConMovimiento(pilas)
# Crear fondo 1 con posicion en X de 288 (no visible)
fondo = FondoConMovimiento(pilas)
fondo.x = 288

# Crear fondo 2
fondo2 = FondoConMovimiento(pilas)
fondo3 = FondoConMovimiento(pilas)
# llamar a la funcion crear_tubos cada 2.5 segundos
pilas.tareas.siempre(4, crear_tubos)
class SaltarUnaVez(pilas.comportamientos.Comportamiento):
    """Realiza un salto, cambiando los atributos 'y'."""

    def iniciar(self, receptor, velocidad_inicial=10, cuando_termina=None):
        """Se invoca cuando se anexa el comportamiento a un actor.

        :param receptor: El actor que comenzará a ejecutar este comportamiento.
        """
        super(SaltarUnaVez, self).iniciar(receptor)
        self.velocidad_inicial = velocidad_inicial
        self.cuando_termina = cuando_termina
        self.sonido_saltar = self.pilas.sonidos.cargar("audio/saltar.wav")
        self.suelo = int(self.receptor.y)
        self.velocidad = self.velocidad_inicial
        self.sonido_saltar.reproducir()
        self.velocidad_aux = self.velocidad_inicial
        self.receptor.saltando = True

    def actualizar(self):
        self.receptor.y += self.velocidad
        self.velocidad -= 0.3

        if self.receptor.y <= self.suelo:
            self.velocidad_aux /= 3.5
            self.velocidad = self.velocidad_aux

            if self.velocidad_aux <= 1:
                # Si toca el suelo
                self.receptor.y = self.suelo
                if self.cuando_termina:
                    self.cuando_termina()
                self.receptor.saltando = False
                return True
teclas = {
            pilas.simbolos.w: 'arriba',
            pilas.simbolos.ESPACIO: 'boton',
        }
mi_control = pilas.control.Control(teclas)
"""Del ejemplo 'control_personalizado.py"""

class FlappyConControles(pilasengine.actores.Actor):
    #Clase que define todos los aspectos del Actor
    def iniciar(self):    
        #Define la imagen que se utilizara para el actor"
        self.imagen = pilas.imagenes.cargar_grilla("Windows.png", 3)
        #Define la escala de tamaño del actor
        self.escala = 1.2
        #Define la posicion X en la cual se posicionara el actor
        self.x = -80
        #Define la posicion Y en la cual se posicionara el actor
        self.y = -200
        #Define la posicion X en la cual se posicionara la camara
        pilas.camara.x = [0]
        self.saltando = False

    def actualizar(self):
        self.x += 0
        #Define cuanto avanzara el actor
        self.imagen.avanzar()
        #Define cuanto avanzara la camara
        pilas.camara.x += .001
        #Define los controles
        if pilas.control.arriba:
            self.y +=1
            self.hacer("SaltarUnaVez")
FlappyConControles(pilas)
pilas.comportamientos.vincular(SaltarUnaVez)

pilas.ejecutar()