import pygame
import random
import math

class VistaJuego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.temblor = 0 
        self.color_nodo = (200, 50, 50) 

    def dibujar_grafo(self, lista_nodos):

        for nodo in lista_nodos:
            for vecino in nodo.vecinos:
                pygame.draw.line(self.pantalla, (100,100,100), (nodo.x, nodo.y), (vecino.x, vecino.y), 3)

        for nodo in lista_nodos:
            pygame.draw.circle(self.pantalla, self.color_nodo, (nodo.x, nodo.y), nodo.radio)

            pygame.draw.circle(self.pantalla, (255, 255, 255), (nodo.x, nodo.y), nodo.radio, 2)

    def dibujar_mira(self, mouse_x, mouse_y):

        dx = random.randint(-self.temblor, self.temblor)
        dy = random.randint(-self.temblor, self.temblor)
        x_final, y_final = mouse_x + dx, mouse_y + dy
        
        pygame.draw.line(self.pantalla, (0, 255, 0), (x_final - 15, y_final), (x_final + 15, y_final), 2)
        pygame.draw.line(self.pantalla, (0, 255, 0), (x_final, y_final - 15), (x_final, y_final + 15), 2)
        
        return x_final, y_final