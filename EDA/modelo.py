import math
import random

class Nodo:
    def __init__(self, id, nombre, x, y, radio, vida_max = 100):

        self.id = id
        self.nombre = nombre
        self.vida_max = vida_max
        self.vida_actual = vida_max 
        self.destruido = False

        ## coordenadas en el espacio
        self.x = x
        self.y = y
        self.radio = radio

        ## que nodos estan conectados
        self.vecinos = []

    def conectar(self, sig_nodo):

        ## agregar al vecino en la lista
        if sig_nodo not in self.vecinos:
            self.vecinos.append(sig_nodo)

            ## no es bidireccional, se agrega el nodo automaticamente
            if self not in sig_nodo.vecinos:
                sig_nodo.vecinos.append(self)
            
    def medir_golpes(self, cantidad):
        
        ## si el nodo se muere, se muere
        if self.destruido:
            return False
        
        ## resta la vida
        self.vida_actual -= cantidad

        ## la vida no puede ser negativa
        if self.vida_actual < 0:
            self.vida_actual = 0

        print(f"Le pegaste a {self.nombre}!, con {cantidad} de daño, Vida Actual: {self.vida_actual}/{self.vida_max}")

        ## condicion para la muerte de un nodo
        if self.vida_actual == 0:
            self.destruido = True 
            print(f"Destruiste su {self.nombre}!")
            return True
        
        return False

    ## para lo de almacenar datos en un JSON
    def to_dict(self):
        return {
                "id": self.id,
                "nombre": self.nombre,
                "vida_actual": self.vida_actual,
                "destruido": self.destruido
            }

class Grafo_Cuerpo:
    def __init__(self):
        self.nodos = {} ## podemos acceder por id a los nodos

    def agregar_nodo(self, nodo):
        self.nodos[nodo.id] = nodo

    def inicializar_personaje(self):

        ## id, nombre, posX, posY, radio y vida del nodo
        cabeza = Nodo(1, "Cabeza", 400, 110, 50, vida_max=50)       
        torso = Nodo(2, "Torso", 400, 270, 60, vida_max=100)
        brazo_izq = Nodo(3, "Brazo Izq", 270, 270, 30, vida_max=50) 
        brazo_der = Nodo(4, "Brazo Der", 530, 270, 30, vida_max=50) 
        piernas = Nodo(5, "Piernas", 400, 480, 50, vida_max=50)     

        ## conectamos los nodos.
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

        ## el rebote solo vale para nodos vivos y adyacentes
        vecinos_activos = []

        for vecino in nodo_golpeado.vecinos:
            if vecino.destruido == False:
                vecinos_activos.append(vecino)
        
        ## si no hay vecinos vivos, se falla el tiro
        if not vecinos_activos:
            print("Fallaste el tiro, no hay mas nodos disponibles")
            return None
        
        ## rebote aleatorio
        vecino_aleatorio = random.choice(vecinos_activos)
        print(f"La bala reboto hacia {vecino_aleatorio.nombre}")
        return vecino_aleatorio