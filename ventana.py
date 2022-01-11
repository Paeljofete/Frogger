import pygame
import sys
from pygame.locals import *
from rectangulo import Rectangulo
from paneljuego import PanelJuego

pygame.init()

# Colores recurrentes guardados en constantes por comodidad y legibilidad.
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDEFROG = (83, 174, 67)

clock = pygame.time.Clock()

#Creación de la ventana y del tamaño de la misma.
ANCHO = 1100
ALTO = 700
SIZE = (ANCHO, ALTO)
MARCO = pygame.display.set_mode(SIZE)

#Tipo de letra.
titulos = pygame.font.Font('fuentes/ArcadeClassic.ttf', 35)
textos = pygame.font.Font('fuentes/ArcadeClassic.ttf', 20)
inicios = pygame.font.Font('fuentes/ARCADE_N.TTF', 40)

#Música de fondo.
pygame.mixer.music.load('musica/musFrog.mp3')
pygame.mixer.music.play(-1)

# Control de teclas.
pulsa = pygame.key.get_pressed()

# Fondo de pantalla de título.
fondo = pygame.image.load('imagenes/fondo.jpg')
anchoImagen = fondo.get_width()
altoImagen = fondo.get_height()
# Dibuja un rectángulo blanco debajo para poner el logo y la rana. Decoración de la ventana.
pygame.draw.rect(MARCO, BLANCO, (0, ALTO - altoImagen, ANCHO, altoImagen))
# Se coloca el logotipo del juego debajo a la izquierda.
MARCO.blit(fondo, (50, ALTO - altoImagen))
decorado = pygame.image.load('imagenes/rana1_.png')
MARCO.blit(decorado, (ANCHO - anchoImagen, ALTO - altoImagen))

# Carteles de la presentación.
bienvenida = titulos.render('by Pael', True, VERDEFROG)
bienvenidaAncho = bienvenida.get_width()
bienvenidaAlto = bienvenida.get_height()
MARCO.blit(bienvenida, ((ANCHO / 2) - bienvenidaAncho, (ALTO - altoImagen / 2)))
version = textos.render('Version   01', True, VERDEFROG)
versionAncho = version.get_width()
versionAlto = version.get_height()
MARCO.blit(version, (ANCHO - versionAncho, ALTO - versionAlto))

volumenS = textos.render('8 subir volumen', True, VERDEFROG)
volumenB = textos.render('2 bajar volumen', True, VERDEFROG)
volumenM = textos.render('5 mute', True, VERDEFROG)
MARCO.blit(volumenS, (10, 10))
MARCO.blit(volumenB, (200, 10))
MARCO.blit(volumenM, (400, 10))

comenzar = inicios.render('pulsa espacio para comenzar', True, VERDEFROG)
comenzarAncho = comenzar.get_width()
comenzarAlto = comenzar.get_height()
# Valores para centrar y punto de partida para el movimiento.
# El operando // devuelve un valor entero, redondea si es decimal.
centraAncho = (ANCHO // 2 - comenzarAncho // 2)
centraAlto = ((ALTO // 4 - comenzarAlto // 2))
comenzarRect = pygame.draw.rect(MARCO, NEGRO, (centraAncho, centraAlto, comenzarAncho, comenzarAlto))
MARCO.blit(comenzar, comenzarRect)

# Se crea lista con el número de cuadrados que se van a poner de animación.
lista_rectangulos = pygame.sprite.Group()
# Las coordenadas para comenzar serán x 0 e y encima de la imágen que hay
# debajo - el número de elementos * el número de pixel que ocupa.
x, y = 0, ALTO - altoImagen - 70
# Cuadrado negro que se pintará encima del último y se confundirá con el
#fondo dando sensación de borrado. Se pone delante puesto que el último
#pintado es el primero de la lista.
rectangulo = Rectangulo(NEGRO, x, y)
lista_rectangulos.add(rectangulo)
#Recorrerá la lista para llegar a la cantidad de elementos que se quieren pintar
#en un recorrido.
while lista_rectangulos.__len__() < 7:
    x += 10
    y += 10
    #Se crea un objeto en cada vuelta y se le pasan las coordenadas.
    rectangulo = Rectangulo(VERDEFROG, x, y)
    lista_rectangulos.add(rectangulo)

rectangulo = Rectangulo(BLANCO, x, y)
lista_rectangulos.add(rectangulo)

def disenio_marco():
    #Icono y título.
    pygame.display.set_caption('Frogger')
    icono = pygame.image.load('imagenes/rana_abajo/rana_icon.png')
    pygame.display.set_icon(icono)

def bajarVolumen():
    #si se pulsa la tecla F2 y además hay sonido se podrá bajar en cada pulsación.
    if pulsa and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
    elif pulsa and pygame.mixer.music.get_volume() == 0.0:
        muteVolumen()

def subirVolumen():
    if pulsa and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)

def muteVolumen():
    pygame.mixer.music.set_volume(0.0)

if __name__ == '__main__':
    disenio_marco()
    #Se ejecuta mientras no haya evento de salida.
    while True:
        # en una variable recibe todos los eventos que tiene preprogramados Pygame.
        for event in pygame.event.get():
            #Si el tipo de evento es QUIT sale del programa, que es cuando presionamos la "x" de la ventana
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    bajarVolumen()
                if event.key == pygame.K_8:
                    subirVolumen()
                if event.key == pygame.K_5:
                    muteVolumen()
                if event.key == pygame.K_SPACE:
                    paneljuego = PanelJuego(MARCO)
        lista_rectangulos.update(y - 70, y - 10, ANCHO)
        lista_rectangulos.draw(MARCO)

        pygame.display.flip()
        clock.tick(60)