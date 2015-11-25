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