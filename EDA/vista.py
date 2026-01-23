import pygame
import random
import math
import os

class VistaJuego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.temblor = 0 

        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(carpeta_actual, "monstruo.png")
        
        print(f"Buscando imagen en: {ruta_imagen}")

        if os.path.exists(ruta_imagen):
            try:
                imagen_original = pygame.image.load(ruta_imagen)

                ancho_real, alto_real = imagen_original.get_size()

                nuevo_alto = 500

                factor = nuevo_alto / alto_real
                nuevo_ancho = int(ancho_real * factor)

                self.imagen_fondo = pygame.transform.scale(imagen_original, (nuevo_ancho, nuevo_alto))

                x_centrado = (800 - nuevo_ancho) // 2
                y_centrado = (600 - nuevo_alto) // 2
                self.pos_imagen = (x_centrado, y_centrado)
                
                print(f"Imagen redimensionada a {nuevo_ancho}x{nuevo_alto} y centrada.")
                
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                self.imagen_fondo = None
        else:
            print("ERROR: No encontré 'monstruo.png'. Revisa el nombre del archivo.")
            self.imagen_fondo = None

    def dibujar_nodo_transparente(self, x, y, radio):
        superficie = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
        rojo_transparente = (255, 0, 0, 100) 
        pygame.draw.circle(superficie, rojo_transparente, (radio, radio), radio)
        self.pantalla.blit(superficie, (x - radio, y - radio))

    def dibujar_grafo(self, lista_nodos):
        if self.imagen_fondo:
            self.pantalla.blit(self.imagen_fondo, self.pos_imagen)
        else:
            pygame.draw.rect(self.pantalla, (50, 50, 50), (200, 100, 400, 400))

        for nodo in lista_nodos:
            for vecino in nodo.nodos_vecinos: 
                pygame.draw.line(self.pantalla, (150, 150, 150), (nodo.x, nodo.y), (vecino.x, vecino.y), 3)

        for nodo in lista_nodos:
            self.dibujar_nodo_transparente(nodo.x, nodo.y, nodo.radio)
            pygame.draw.circle(self.pantalla, (255, 255, 255), (nodo.x, nodo.y), nodo.radio, 1)


    def dibujar_mira(self, mouse_x, mouse_y):
        dx = random.randint(-self.temblor, self.temblor) if self.temblor > 0 else 0
        dy = random.randint(-self.temblor, self.temblor) if self.temblor > 0 else 0
        x_final, y_final = mouse_x + dx, mouse_y + dy
        
        pygame.draw.line(self.pantalla, (0, 255, 0), (x_final - 15, y_final), (x_final + 15, y_final), 2)
        pygame.draw.line(self.pantalla, (0, 255, 0), (x_final, y_final - 15), (x_final, y_final + 15), 2)
        
        return x_final, y_final

    def detectar_impacto(self, x_mira, y_mira, lista_nodos):
        for nodo in lista_nodos:
            distancia = math.sqrt((x_mira - nodo.x)**2 + (y_mira - nodo.y)**2)
            if distancia <= nodo.radio:
                return nodo 
        return None