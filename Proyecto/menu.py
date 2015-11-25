#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
def iniciar_juego():
    pass
def opciones():
    menu.y=100000
    fondoDelMenu.x= [0, 2000]
    b = pilas.interfaz.Boton("Dificultad")
    def moverse():
        b.escala_x = [  2, 0.8, 1], 0.15
        b.escala_y = [0.8, 2,   1], 0.1
        d = pilas.azar(-50, 50)
        b.rotacion = [d, 1], 0.1
    b.conectar(moverse)
    def d():
        def cuando_selecciona(opcion_seleccionada):
            pilas.avisar("Ha seleccionado la opcion: " + opcion_seleccionada)
        opcion = pilas.interfaz.ListaSeleccion(['facil', 'media', 'dificil'], cuando_selecciona)
    b.conectar(d)
def salir()
    exit()

menu=pilas.actores.Menu(
        [
            ('INICIAR JUEGO', iniciar_juego),
            ('OPCIONES', opciones),
            ('SALIR', salir),
        ])
menu.x = [-300, 300,-200, 200,-100, 100, 0]