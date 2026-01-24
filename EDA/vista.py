import pygame
import random
import math
import os

class Vista_Hitbox_Doom:
    ## definimos atributos visuales
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.temblor = 0
        self.color_nodo = (200, 50, 50) ## color tipo sangre para los nodos

        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(carpeta_actual, "disenio_eda.jpg")

        print(f"buscando img en {ruta_imagen}")

        ##cargar el disenio
        try:
            self.disenio_entorno = pygame.image.load(ruta_imagen)
            self.disenio_entorno = pygame.transform.scale(self.disenio_entorno, (800, 600))
    
        except:
            print("No se encontro la imagen de fondo")
            self.disenio_entorno = None

    '''
    Dibujamos al juego por capas:
        primero, el fondo
        segundo, las aristas del grafo
        tercero, los nodos
    '''
    def dibujar_grafo(self, lista_nodos):

        ## capa 1: el disenio o el fondo
        if self.disenio_entorno:
            self.pantalla.blit(self.disenio_entorno, (0,0)) ## dibujar el disenio en la pantalla
        else:
            self.pantalla.fill((20,20,20)) ##pintar todo gris si no hay disenio

        ## capa 2: las aristas
        for nodo in lista_nodos:
            for vecino in nodo.vecinos:
                ## dibujamos las aristas con metodos de pygame
                pygame.draw.line(self.pantalla, (255, 0, 0), (nodo.x, nodo.y), (vecino.x, vecino.y), 5)

        ## capa 3: los nodos
        for nodo in lista_nodos:
            ## dibujamos los circulos
            pygame.draw.circle(self.pantalla, (255,255,255), (nodo.x, nodo.y), nodo.radio, 2)


    def dibujar_mira(self, mouse_x, mouse_y):
        ## aumento de la sensibilidad del ads
        dx = random.randint(-self.temblor, self.temblor)
        dy = random.randint(-self.temblor, self.temblor)
        x_final, y_final = mouse_x + dx, mouse_y + dy

        color_mira = (0, 255, 0)
        pygame.draw.line(self.pantalla, color_mira, (x_final - 20, y_final), (x_final + 20, y_final), 2)
        pygame.draw.line(self.pantalla, color_mira, (x_final, y_final - 20), (x_final, y_final + 20), 2)
        pygame.draw.circle(self.pantalla, color_mira, (x_final, y_final), 15, 1)
        
        return x_final, y_final