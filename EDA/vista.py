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

        pygame.font.init()
        self.fuente_chica = pygame.font.SysFont("Arial", 25, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", 50, bold=True)
        self.boton_reset = pygame.Rect(200, 400, 400, 50)
        self.boton_menu = pygame.Rect(250, 480, 300, 50)

        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_fondo = os.path.join(carpeta_actual, "disenio_eda.jpg")
        ruta_menu = os.path.join(carpeta_actual, "pantalla_inicio.jpg")

        print(f"buscando img en {ruta_fondo}")

        ##cargar el disenio
        try:
            self.disenio_entorno = pygame.image.load(ruta_fondo)
            self.disenio_entorno = pygame.transform.scale(self.disenio_entorno, (800, 600))
    
        except:
            print("No se encontro la imagen de fondo")
            self.disenio_entorno = None

        try:
            self.disenio_menu = pygame.image.load(ruta_menu)
            self.disenio_menu = pygame.transform.scale(self.disenio_menu, (800, 600))
        except:
            print("No se encontro la imagen del menu")
            self.disenio_menu = None

    ## dibuja la pantalla de game over 
    def dibujar_game_over(self, puntaje, texto_boton="SIGUIENTE JUGADOR"):
        # Un cuadro negro para tapar el fondo
        oscuro = pygame.Surface((800, 600))
        oscuro.set_alpha(200) 
        oscuro.fill((0,0,0))
        self.pantalla.blit(oscuro, (0,0))
        
        # Los textos
        titulo = self.fuente_grande.render("FIN DEL TURNO", True, (255, 0, 0))
        puntos = self.fuente_chica.render(f"Puntaje Final: {puntaje}", True, (255, 255, 255))

        # Posicion de los textos 
        self.pantalla.blit(titulo, (200, 150))
        self.pantalla.blit(puntos, (280, 250))

        # Boton siguiente jugador (Verde)
        pygame.draw.rect(self.pantalla, (0, 150, 0), self.boton_reset) # Rectangulo verde
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.boton_reset, 2) # Borde blanco
        
        # Renderizamos el texto variable (SIGUIENTE o FINALIZAR)
        texto_reset = self.fuente_chica.render(texto_boton, True, (255, 255, 255))
        
        # Centrado simple
        self.pantalla.blit(texto_reset, (290, 410))

        # Boton Menu (Azul)
        pygame.draw.rect(self.pantalla, (0, 0, 150), self.boton_menu) # Rectangulo azul
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.boton_menu, 2) # Borde blanco
        texto_menu = self.fuente_chica.render("VOLVER AL MENÚ", True, (255, 255, 255))
        self.pantalla.blit(texto_menu, (310, 490))


    def dibujar_menu(self):
        if self.disenio_menu:
            self.pantalla.blit(self.disenio_menu, (0,0))
        else:
            self.pantalla.fill((20,20,20))

            titulo = self.fuente_grande.render("DOOM: CAZADOR", True, (255, 0, 0))
            aviso = self.fuente_chica.render("Haz Click en cualquier lado para empezar", True, (255, 255, 255))
            self.pantalla.blit(titulo, (200, 200))
            self.pantalla.blit(aviso, (200, 400))

    def dibujar_grafo(self, lista_nodos):

        ## capa 1: el diseño o el fondo
        if self.disenio_entorno:
            self.pantalla.blit(self.disenio_entorno, (0,0)) ## dibujar el diseño en la pantalla
        else:
            self.pantalla.fill((20,20,20)) ##pintar todo gris si no hay diseño

        ## capa 2: las aristas
        for nodo in lista_nodos:
            for vecino in nodo.vecinos:
                ## dibujamos las aristas con metodos de pygame
                pygame.draw.line(self.pantalla, (150, 0, 0), (nodo.x, nodo.y), (vecino.x, vecino.y), 5)

        ## capa 3: los nodos
        for nodo in lista_nodos:
            if not nodo.destruido:
                # Circulo transparente rojo
                s = pygame.Surface((nodo.radio*2, nodo.radio*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 0, 0, 100), (nodo.radio, nodo.radio), nodo.radio)
                self.pantalla.blit(s, (nodo.x - nodo.radio, nodo.y - nodo.radio))
                
                # Borde blanco fino
                pygame.draw.circle(self.pantalla, (255,255,255), (nodo.x, nodo.y), nodo.radio, 2)

    def dibujar_mira(self, mouse_x, mouse_y):
        ## aumento de la sensibilidad del ads
        dx = random.randint(-self.temblor, self.temblor)
        dy = random.randint(-self.temblor, self.temblor)
        x_final, y_final = mouse_x + dx, mouse_y + dy

        color_mira = (0, 255, 0)
        pygame.draw.line(self.pantalla, color_mira, (x_final - 20, y_final), (x_final + 20, y_final), 2)
        pygame.draw.line(self.pantalla, color_mira, (x_final, y_final - 20), (x_final, y_final + 20), 2)
        
        return x_final, y_final
    

    def detectar_impacto(self, x_mira, y_mira, lista_nodos):
        for nodo in lista_nodos:
            # Formula de Pitagoras para saber si el clic cayó dentro del circulo
            distancia = math.sqrt((x_mira - nodo.x)**2 + (y_mira - nodo.y)**2)
            
            # Si la distancia es menor al radio y el nodo NO esta destruido...
            if distancia <= nodo.radio and not nodo.destruido:
                return nodo 
        
        return None