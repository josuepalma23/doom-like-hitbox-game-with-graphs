import pygame
import sys

from vista import Vista_Hitbox_Doom
from modelo import Grafo_Cuerpo

ANCHO = 800
ALTO = 600

## inicio del juego
pygame.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Grafos con Doom")

reloj = pygame.time.Clock()

## Backend
juego = Grafo_Cuerpo()
juego.inicializar_personaje()

## Vista
vista = Vista_Hitbox_Doom(PANTALLA)

##Bucle del juego
while True:

    ## eventos con el mouse
    for evento in pygame.event.get():
        ## cerrar la ventana con la X
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        ## click izq
        if evento.type == pygame.MOUSEBUTTONDOWN:
            ## lo de JOEL, pero todavia no tenemo, solo voy a probar el disparo y ads
            vista.temblor += 2
            print("Disparo!, Aumenta el ADS")
        
    
    lista_nodos_finales = list(juego.nodos.values())
    vista.dibujar_grafo(lista_nodos_finales)
    pygame.mouse.set_visible(False)

    mx, my = pygame.mouse.get_pos()
    vista.dibujar_mira(mx, my)

    pygame.display.flip()
    reloj.tick(60) ## FPS

