import pygame
import sys
from vista import VistaJuego
from modelo import Grafo_Cuerpo  

pygame.init()
PANTALLA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Proyecto Final - Integración")
reloj = pygame.time.Clock()

logica_juego = Grafo_Cuerpo()

logica_juego.inicializar_personaje() 

lista_nodos_reales = list(logica_juego.nodos.values())

vista = VistaJuego(PANTALLA)

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            vista.temblor += 2
            if vista.temblor > 20: vista.temblor = 20

            nodo_tocado = vista.detectar_impacto(mouse_pos[0], mouse_pos[1], lista_nodos_reales)
            
            if nodo_tocado:
                print(f"\n--- IMPACTO ---")
                print(f"¡Le diste a: {nodo_tocado.nombre}!")
                
                nodo_tocado.medir_golpes(20) 
                
                nodo_vecino = logica_juego.calcular_rebote(nodo_tocado)
                
                
                if nodo_vecino:
                    print(f"¡REBOTE! El daño saltó a: {nodo_vecino.nombre}")
                    nodo_vecino.medir_golpes(10) 
            else:
                print("Disparo al aire...")

    PANTALLA.fill((0, 0, 0))

    vista.dibujar_grafo(lista_nodos_reales)
    
    vista.dibujar_mira(mouse_pos[0], mouse_pos[1])

    pygame.display.update()
    reloj.tick(60)