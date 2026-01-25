import pygame
import sys
import os

from vista import Vista_Hitbox_Doom
from modelo import Grafo_Cuerpo

ANCHO = 800
ALTO = 600

## inicio del juego
pygame.init()
pygame.mixer.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Grafos con Doom")

reloj = pygame.time.Clock()

## Cargar musica
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_musica = os.path.join(carpeta_actual, "doom_music.mp3")

try:
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  ## -1 para que se repita infinitamente
    print("Musica de fondo cargada y reproduciendo.")
except:
    print("No se encontro la musica de fondo")
## Backend
juego = Grafo_Cuerpo()
juego.inicializar_personaje()

## Vista
vista = Vista_Hitbox_Doom(PANTALLA)

estado = "MENU"
balas = 10
puntaje = 0
ubi_boton = pygame.Rect(300, 400, 200, 80)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # 1. MENU -> EMPEZAR JUEGO
            if estado == "MENU":
                estado = "JUEGO"
                # Reseteamos todo para empezar limpio
                balas = 10
                puntaje = 0
                juego = Grafo_Cuerpo()
                juego.inicializar_personaje()

            # 2. JUEGO -> DISPARAR
            elif estado == "JUEGO":
                if balas > 0:
                    balas = balas - 1 # Gastamos una bala
                    vista.temblor += 2 # Aumenta dificultad visual
                    
                    # Detectamos impacto
                    lista = list(juego.nodos.values())
                    nodo_tocado = vista.detectar_impacto(mouse_pos[0], mouse_pos[1], lista)
                    
                    if nodo_tocado:
                        print(f"¡Le diste a {nodo_tocado.nombre}!")
                        puntaje += 100 # Sumamos puntos
                        
                        # Daño para matar en 3 tiros exactos
                        danio = nodo_tocado.vida_max / 3
                        nodo_tocado.medir_golpes(danio)
                        
                        # Rebote 
                        vecino = juego.calcular_rebote(nodo_tocado)
                        if vecino:
                            vecino.medir_golpes(10)
                            puntaje += 50
                    
                    # Si se acaban las balas, cambiamos a pantalla final
                    if balas == 0:
                        estado = "GAMEOVER"

            # 3. GAME OVER -> VOLVER AL MENU
            elif estado == "GAMEOVER":
                # Boton VERDE: Siguiente Jugador (Reiniciar Juego Directo)
                if vista.boton_reset.collidepoint(mouse_pos):
                    print("Reiniciando para siguiente jugador...")
                    balas = 10
                    puntaje = 0
                    juego = Grafo_Cuerpo()
                    juego.inicializar_personaje()
                    estado = "JUEGO"

                # Boton AZUL: Volver al Menu Principal
                elif vista.boton_menu.collidepoint(mouse_pos):
                    print("Volviendo al menu...")
                    estado = "MENU"

    # DIBUJAR EN PANTALLA
    PANTALLA.fill((0,0,0)) # Limpiar pantalla

    if estado == "MENU":
        vista.dibujar_menu()
        pygame.mouse.set_visible(True)
    
    elif estado == "JUEGO":
        # Diccionario de nodos a lista para poder dibujarlos
        lista_nodos_finales = list(juego.nodos.values())
        vista.dibujar_grafo(lista_nodos_finales)
        
        # Ocultamos el mouse normal y dibujamos la mira
        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()
        vista.dibujar_mira(mx, my)

    elif estado == "GAMEOVER":
        # Dejamos el fondo congelado
        lista = list(juego.nodos.values())
        vista.dibujar_grafo(lista)
        # Ponemos el letrero encima
        vista.dibujar_game_over(puntaje)
        pygame.mouse.set_visible(True)
    
    # ACTUALIZAR PANTALLA
    pygame.display.flip()
    reloj.tick(60) ## 60 FPS