import pygame
import sys
from vista import VistaJuego

class NodoFalso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 40
        self.vecinos = []

pygame.init()
PANTALLA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Prueba de Abigail")
reloj = pygame.time.Clock()

n1 = NodoFalso(400, 100) 
n2 = NodoFalso(400, 300) 
n1.vecinos.append(n2)    
n2.vecinos.append(n1)
mis_nodos = [n1, n2]

vista = VistaJuego(PANTALLA)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            vista.temblor += 5 
            print("¡Bang! Aumentando temblor...")

    PANTALLA.fill((20, 20, 20)) 
    
    pygame.mouse.set_visible(False)
    mx, my = pygame.mouse.get_pos()
    
    vista.dibujar_grafo(mis_nodos)
    vista.dibujar_mira(mx, my)

    pygame.display.flip()
    reloj.tick(60)