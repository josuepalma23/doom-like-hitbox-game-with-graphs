import math
import random

class Nodo:
    def __init__(self, id, nombre, x, y, radio, vida_max = 100):

        self.id = id
        self.nombre = nombre
        self.vida_max = vida_max
        self.vida_actual = vida_max 
        self.destruido = False

        self.x = x
        self.y = y
        self.radio = radio

        self.nodos_vecinos = []

    def conectar(self, sig_nodo):

        if sig_nodo not in self.nodos_vecinos:
            self.nodos_vecinos.append(sig_nodo)

            if self not in sig_nodo.nodos_vecinos:
                sig_nodo.nodos_vecinos.append(self)
            
    def medir_golpes(self, cantidad):
        
        if self.destruido:
            return False
        
        self.vida_actual -= cantidad

        if self.vida_actual < 0:
            self.vida_actual = 0

        print(f"Le pegaste a {self.nombre}!, con {cantidad} de daño, Vida Actual: {self.vida_actual}/{self.vida_max}")

        if self.vida_actual == 0:
            self.destruido = True 
            print(f"Destruiste su {self.nombre}!")
            return True
        
        return False

    def to_dict(self):
        return {
                "id": self.id,
                "nombre": self.nombre,
                "vida_actual": self.vida_actual,
                "destruido": self.destruido
            }

class Grafo_Cuerpo:
    def __init__(self):
        self.nodos = {} 

    def agregar_nodo(self, nodo):
        self.nodos[nodo.id] = nodo

    def inicializar_personaje(self):

        ## MODIFICACIÓN DE COORDENADAS (CENTRADO Y MÁS GRANDE)
        cabeza = Nodo(1, "Cabeza", 400, 110, 50, vida_max=50)       
        torso = Nodo(2, "Torso", 400, 270, 60, vida_max=100)
        brazo_izq = Nodo(3, "Brazo Izq", 270, 270, 30, vida_max=50) 
        brazo_der = Nodo(4, "Brazo Der", 530, 270, 30, vida_max=50) 
        piernas = Nodo(5, "Piernas", 400, 480, 50, vida_max=50)     

        cabeza.conectar(torso)

        torso.conectar(brazo_der)
        torso.conectar(brazo_izq)
        torso.conectar(piernas)

        lista_miembros = [cabeza, torso, brazo_der, brazo_izq, piernas]

        for miembro in lista_miembros:
            self.agregar_nodo(miembro)

        print("Inicializamos el grafico, se conectan los nodos.")

    def calcular_rebote(self, nodo_golpeado):

        print(f"calculamos el daño desde {nodo_golpeado.nombre}")

        vecinos_activos = []


        for vecino in nodo_golpeado.nodos_vecinos:
            if vecino.destruido == False:
                vecinos_activos.append(vecino)
        
        if not vecinos_activos:
            print("Fallaste el tiro, no hay mas nodos disponibles")
            return None
        
        vecino_aleatorio = random.choice(vecinos_activos)
        print(f"La bala reboto hacia {vecino_aleatorio.nombre}")
        return vecino_aleatorio