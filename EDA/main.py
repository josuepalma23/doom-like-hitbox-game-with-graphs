import pygame
import sys
import os
import random
import math
import json 

from vista import Vista_Hitbox_Doom
from modelo import Grafo_Cuerpo

ANCHO = 800
ALTO = 600

## Inicio del juego
pygame.init()
pygame.mixer.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Grafos con Doom - Final Clean")

reloj = pygame.time.Clock()

## Cargar musica
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_musica = os.path.join(carpeta_actual, "doom_music.mp3")

try:
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) 
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

## Variables globales de turno
jugador_turno = 1
puntajes_finales = [0, 0] 

## Opciones de estrategia
tipo_municion = "NORMAL" 
descripcion_bonus = "" 
multiplicador_puntos = 1.0
incremento_temblor = 2 

## Datos almacenados para el archivo el archivo json
datos_sesion = {
    "Jugador 1": {"Danio_Total": 0, "Nodos_Destruidos": [], "Puntaje": 0},
    "Jugador 2": {"Danio_Total": 0, "Nodos_Destruidos": [], "Puntaje": 0}
}

def guardar_datos_json(datos):
    """Exporta los resultados a un archivo JSON localmente"""
    try:
        with open("resultados_partida.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
        print("Datos guardados como: resultados_partida.json")
    except Exception as e:
        print(f"Error guardando JSON: {e}")


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        ## Detectar seleccion de estrategia
        if evento.type == pygame.KEYDOWN and estado == "ESTRATEGIA":
            if evento.key == pygame.K_a:
                tipo_municion = "PESADA"
                descripcion_bonus = "EFECTO: Daño Crítico (+50% Pts) | RETROCESO ALTO"
                multiplicador_puntos = 1.5      
                incremento_temblor = 25         
                estado = "JUEGO"
            elif evento.key == pygame.K_s:
                tipo_municion = "LIGERA"
                descripcion_bonus = "EFECTO: Daño Estándar | RETROCESO BAJO"
                multiplicador_puntos = 1.0      
                incremento_temblor = 5          
                estado = "JUEGO"
        

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # MENU para empezar el juego
            if estado == "MENU":
                ## Reiniciar variables para nueva partida
                jugador_turno = 1
                puntajes_finales = [0, 0]
                
                datos_sesion = {
                    "Jugador 1": {"Total Damage": 0, "Nodos Destruidos": [], "Puntaje": 0},
                    "Jugador 2": {"Total Damage": 0, "Nodos Destruidos": [], "Puntaje": 0}
                }
                
                balas = 3 
                puntaje = 0
                vista.temblor = 0
                juego = Grafo_Cuerpo()
                juego.inicializar_personaje()
                
                estado = "ESTRATEGIA" 
                

            # Disparar en el juego
            elif estado == "JUEGO":
                if balas > 0:
                    balas = balas - 1
                    # aumento de dificultad y temblor
                    vista.temblor += incremento_temblor 

                    # Punteria
                    dx = vista.temblor 
                    if dx > 0:
                        error_x = random.randint(-dx, dx)
                        error_y = random.randint(-dx, dx)
                    else:
                        error_x = 0; error_y = 0

                    tiro_x = mouse_pos[0] + error_x
                    tiro_y = mouse_pos[1] + error_y

                    lista = list(juego.nodos.values())
                    nodo_tocado = vista.detectar_impacto(tiro_x, tiro_y, lista)

                    key_jugador = f"Jugador {jugador_turno}" 

                    if nodo_tocado:
                        puntos_base = 100
                        puntos_reales = int(puntos_base * multiplicador_puntos)
                        puntaje += puntos_reales
                        
                        danio = math.ceil(nodo_tocado.vida_max / 3)
                        fue_destruido = nodo_tocado.medir_golpes(danio)
                        datos_sesion[key_jugador]["Total Damage"] += danio
                        
                        if fue_destruido:
                             bonus = int(150 * multiplicador_puntos)
                             puntaje += bonus
                             datos_sesion[key_jugador]["Nodos Destruidos"].append(nodo_tocado.nombre)
                        
                        vecino = juego.calcular_rebote(nodo_tocado)
                        if vecino:
                            vecino.medir_golpes(10)  
                            datos_sesion[key_jugador]["Total Damage"] += 10
                            puntaje += 50

                    if balas == 0:
                        puntajes_finales[jugador_turno - 1] = puntaje
                        datos_sesion[key_jugador]["Puntaje"] = puntaje 
                        estado = "GAMEOVER"

            # 3. GAME OVER, reiniciar o menu
            elif estado == "GAMEOVER":
                
                if vista.boton_reset.collidepoint(mouse_pos):
                    
                    ## cambio de turno o finalizacion
                    if jugador_turno == 1:
                        # si es el J1, pasamos al J2
                        jugador_turno = 2
                        balas = 3
                        puntaje = 0
                        vista.temblor = 0
                        juego = Grafo_Cuerpo()
                        juego.inicializar_personaje()
                        estado = "ESTRATEGIA" 
                    
                    else:
                        # si es J2, fin del juego, regresa a menu
                        print("Fin del juego, regresando al menú...")
                        guardar_datos_json(datos_sesion)
                        estado = "MENU"
                    

                elif vista.boton_menu.collidepoint(mouse_pos):
                    estado = "MENU"

    # DIBUJAR EN PANTALLA
    PANTALLA.fill((0,0,0)) 

    if estado == "MENU":
        vista.dibujar_menu()
        pygame.mouse.set_visible(True)

    ## dibujar pantalla de estrategia
    elif estado == "ESTRATEGIA":
        PANTALLA.fill((20, 20, 40)) 
        fuente = pygame.font.SysFont("Arial", 30, bold=True)
        titulo = fuente.render(f"JUGADOR {jugador_turno}: ELIGE TU MUNICIÓN", True, (255, 255, 0))
        txt_a = fuente.render("[A] PESADA:  +50% Puntos | Mucho Retroceso", True, (255, 100, 100))
        txt_s = fuente.render("[S] LIGERA:  Puntos Normales | Puntería Estable", True, (100, 255, 100))
        PANTALLA.blit(titulo, (150, 150))
        PANTALLA.blit(txt_a, (100, 250))
        PANTALLA.blit(txt_s, (100, 320))

    elif estado == "JUEGO":
        lista_nodos_finales = list(juego.nodos.values())
        vista.dibujar_grafo(lista_nodos_finales)
        pygame.mouse.set_visible(False)
        mx, my = pygame.mouse.get_pos()
        vista.dibujar_mira(mx, my)
        
        ## hud con informacion de bonus
        score_p1 = puntaje if jugador_turno == 1 else puntajes_finales[0]
        score_p2 = puntaje if jugador_turno == 2 else puntajes_finales[1]
        fuente_hud = pygame.font.SysFont("Arial", 20, bold=True)
        texto_hud = f"P1: {score_p1}  |  P2: {score_p2}  |  BALAS: {balas}  |  MUNICIÓN: {tipo_municion}"
        hud = fuente_hud.render(texto_hud, True, (255, 255, 255))
        PANTALLA.blit(hud, (10, 10))
        # Descripcion Bonus
        fuente_desc = pygame.font.SysFont("Arial", 16)
        desc = fuente_desc.render(descripcion_bonus, True, (255, 255, 150))
        PANTALLA.blit(desc, (10, 35)) 

    elif estado == "GAMEOVER":
        lista = list(juego.nodos.values())
        vista.dibujar_grafo(lista)
        
        ## mostrar pantalla final segun el jugador
        if jugador_turno == 2:
            vista.dibujar_game_over(puntaje, "FINALIZAR PARTIDA")
        else:
            vista.dibujar_game_over(puntaje, "SIGUIENTE JUGADOR")
            
        pygame.mouse.set_visible(True)

    pygame.display.flip()
    reloj.tick(60)