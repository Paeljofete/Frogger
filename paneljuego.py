import pygame
import sys
import time

pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (133, 0, 217)
ROJO = (224, 0, 0)
VERDEFROG = (83, 174, 67)

# Tipo de letra.
titulos = pygame.font.Font('fuentes/ArcadeClassic.ttf', 35)
textos = pygame.font.Font('fuentes/ArcadeClassic.ttf', 20)
inicios = pygame.font.Font('fuentes/ARCADE_N.TTF', 40)
recomenzar = pygame.font.Font('fuentes/ARCADE_N.TTF', 30)

clock = pygame.time.Clock()

# Información pantalla, se recoge en el momento para que sea como la ventana del panel presentación.
ancho = 1100
alto = 700

# Efectos de sonido.
sonidoTiempo = pygame.mixer.Sound('musica/sound-frogger-time/sound-frogger-time.wav')
sonidoVida = pygame.mixer.Sound('musica/sound-frogger-coin-in/sound-frogger-coin-in.wav')
sonidoSalto = pygame.mixer.Sound('musica/sound-frogger-hop/sound-frogger-hop.wav')
sonidoAgua = pygame.mixer.Sound('musica/sound-frogger-plunk/sound-frogger-plunk.wav')
sonidoAtrop = pygame.mixer.Sound('musica/sound-frogger-squash/sound-frogger-squash.wav')
sonidoGanador = pygame.mixer.Sound('musica/sound-frogger-extra/sound-frogger-extra.wav')

avatar = pygame.image.load('imagenes/rana_izquierda/icono_izq.png')
carretera = pygame.image.load('imagenes/carreteras.png')
agua = pygame.image.load('imagenes/aguas.png')
meta = pygame.image.load('imagenes/metas.png')
avatarArriba = pygame.image.load('imagenes/rana_arriba/avatar_quieto.png')
avatarAbajo = pygame.image.load('imagenes/rana_abajo/rana_icon.png')
avatarDcha = pygame.image.load('imagenes/rana_derecha/icono_dch.png')

cocheAmI = pygame.image.load('imagenes/coches/cocheAmI.png')
cocheBlI = pygame.image.load('imagenes/coches/cocheBlI.png')
camion2 = pygame.image.load('imagenes/coches/camion2.png')

tortuga = pygame.image.load('imagenes/agua/tortugas.png')
tronco1 = pygame.image.load('imagenes/agua/tronco1.png')
tronco2 = pygame.image.load('imagenes/agua/tronco2.png')

vidaPerdida = pygame.image.load('imagenes/vidaPerdida.png')

movimientoIzquierda = [pygame.image.load('imagenes/rana_izquierda/icono_izq.png'),
                       pygame.image.load('imagenes/rana_izquierda/1posicion_izq.png'),
                       pygame.image.load('imagenes/rana_izquierda/2posicion_izq.png'),
                       pygame.image.load('imagenes/rana_izquierda/3posicion_izq.png')]

movimientoDerecha = [pygame.image.load('imagenes/rana_derecha/icono_dch.png'),
                     pygame.image.load('imagenes/rana_derecha/1posicion_dch.png'),
                     pygame.image.load('imagenes/rana_derecha/2posicion_dch.png'),
                     pygame.image.load('imagenes/rana_derecha/3posicion_dch.png')]

movimientoArriba = [pygame.image.load('imagenes/rana_arriba/avatar_quieto.png'),
                    pygame.image.load('imagenes/rana_arriba/1salto_arriba.png'),
                    pygame.image.load('imagenes/rana_arriba/2salto_arriba.png'),
                    pygame.image.load('imagenes/rana_arriba/salto.png')]

movimientoAbajo = [pygame.image.load('imagenes/rana_abajo/rana_icon.png'),
                   pygame.image.load('imagenes/rana_abajo/1salto_abajo.png'),
                   pygame.image.load('imagenes/rana_abajo/2salto_abajo.png'),
                   pygame.image.load('imagenes/rana_abajo/3salto_abajo.png')]

# Gestión velocidad movimiento.
velocidad1 = 10
velocidad2 = 6
velocidad3 = -6

# Coordenadas de cada carril de la carretera.
carril1Loc = 456
carril2Loc = 396
carril3Loc = 336
# Lista para generar los coches en cada carril.
carril1 = [100, 300, 700, 1000]
carril2 = [150, 450, 850]
carril3 = [250, 500, 650, 900]

# Coordenadas de cada canal del agua.
canal1Loc = 216
canal2Loc = 156
canal3Loc = 96
# Lista para generar los troncos y tortugas en cada canal.
canal1 = [50, 350, 700]
canal2 = [100, 600]
canal3 = [200, 550, 950]

# Lista para contabilizar las vidas
ranas = []

class PanelJuego():
    #################################################################################################
    # Método del juego.
    def __init__(self, marco):
        super().__init__()

        # Va a ir contando las imágenes que se han añadido al movimiento.
        cuentaMovimientos = 0
        # Será el ancho menos los pixel del avatar. Se va a tomar el avatar como referente para proporcionar el fondo.
        coordAncho = 1038
        # Alto menos alto del avatar por 2 para que se quede colocado sobre la franja del tiempo.
        coordAlto = 576
        # Pixeles que se moverá el decorado, avatar...
        longitudMovimiento = 60
        # Contador para ir quitando segundos al tiempo
        retroceso = 480

        # Control de vidas y de puntos.
        disponibles = 5
        puntos = 0

        izquierda = False
        derecha = False
        arriba = False
        abajo = False
        pulsadoI = False
        pulsadoD = False
        pulsadoUp = False
        pulsadoDown = False

        salir = True

        while salir:
            self.fondo(marco, puntos, retroceso, disponibles)

            for event in pygame.event.get():
                # Si el tipo de evento es QUIT sale del programa, que es cuando presionamos la "x" de la ventana
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()

                if event.type == pygame.KEYDOWN:
                    # Si se pulsa la tecla a la izquierda y está dentro de los límites de la pantalla.
                    if event.key == pygame.K_LEFT and coordAncho > 18:
                        coordAncho -= longitudMovimiento
                        izquierda = True
                        derecha = False
                        arriba = False
                        abajo = False
                        pulsadoI = True
                        pulsadoD = False
                        pulsadoUp = False
                        pulsadoDown = False
                    elif event.key == pygame.K_RIGHT and coordAncho < 1038:
                        coordAncho += longitudMovimiento
                        izquierda = False
                        derecha = True
                        arriba = False
                        abajo = False
                        pulsadoI = False
                        pulsadoD = True
                        pulsadoUp = False
                        pulsadoDown = False
                    elif event.key == pygame.K_UP and coordAlto > 36:
                        coordAlto -= longitudMovimiento
                        izquierda = False
                        derecha = False
                        arriba = True
                        abajo = False
                        pulsadoI = False
                        pulsadoD = False
                        pulsadoUp = True
                        pulsadoDown = False
                        puntos += 10
                    elif event.key == pygame.K_DOWN and coordAlto < 576:
                        coordAlto += longitudMovimiento
                        izquierda = False
                        derecha = False
                        arriba = False
                        abajo = True
                        pulsadoI = False
                        pulsadoD = False
                        pulsadoUp = False
                        pulsadoDown = True
                    else:
                        izquierda = False
                        derecha = False
                        arriba = False
                        abajo = False

            # Movimientos de los coches.
            # Recorre la lista de carriles.
            for i in range(0, len(carril1)):
                # Si la posición en la que se encuentra es mayor o igual a 1100
                # ha llegado al final del ancho de la pantalla, por lo tanto se
                # pone en 0 para comenzar otra vez. -89 en este caso que es el
                # ancho de los coches.
                if carril1[i] >= 1100:
                    carril1[i] = -89
                # Sino, la posición será igual a la posición + la velocidad que es
                # lo que irá sumando píxeles y dará la sensación de movimiento.
                else:
                    carril1[i] = (carril1[i] + velocidad1)

            for i in range(0, len(carril2)):
                # Recoge el ancho real de cada ítem para que desaparezca por completo de
                # la pantalla.
                if carril2[i] <= -207:
                    carril2[i] = 1100
                # Sino, la posición será igual a la posición + la velocidad que es
                # lo que irá restando píxeles en este caso para que el movimiento
                # sea hacía la izquierda.
                else:
                    carril2[i] = (carril2[i] + velocidad3)

            for i in range(0, len(carril3)):
                if carril3[i] >= 1100:
                    carril3[i] = -89
                else:
                    carril3[i] = (carril3[i] + velocidad2)

            # Movimientos del agua.
            for i in range(0, len(canal3)):
                if canal3[i] >= 1100:
                    canal3[i] = -246
                else:
                    canal3[i] = (canal3[i] + velocidad1)

            for i in range(0, len(canal1)):
                if canal1[i] >= 1100:
                    canal1[i] = -175
                else:
                    canal1[i] = (canal1[i] + velocidad2)

            for i in range(0, len(canal2)):
                if canal2[i] <= -186:
                    canal2[i] = 1100
                else:
                    canal2[i] = (canal2[i] + velocidad3)

            for r in ranas:
                self.marco.blit(avatarAbajo, (r, 36))

            self.carretera(marco)
            self.lago(marco)

            # Son 4 las imágenes de movimiento, por ello debe reproducir las 4 en cada movimiento.
            if cuentaMovimientos + 1 >= 4:
                cuentaMovimientos = 0
            if izquierda:
                sonidoSalto.play()
                self.marco.blit(movimientoIzquierda[cuentaMovimientos], (coordAncho, coordAlto))
                cuentaMovimientos += 1
                # Si ha llegado a los 4 movimientos cambia el estado para que la rana quede en posición quieta, sino sigue
                # realizando el movimiento hasta la siguiente pulsación.
                if cuentaMovimientos + 1 >= 4:
                    izquierda = False
            elif derecha:
                sonidoSalto.play()
                self.marco.blit(movimientoDerecha[cuentaMovimientos], (coordAncho, coordAlto))
                cuentaMovimientos += 1
                if cuentaMovimientos + 1 >= 4:
                    derecha = False
            elif arriba:
                sonidoSalto.play()
                self.marco.blit(movimientoArriba[cuentaMovimientos], (coordAncho, coordAlto))
                cuentaMovimientos += 1
                if cuentaMovimientos + 1 >= 4:
                    arriba = False
            elif abajo:
                sonidoSalto.play()
                self.marco.blit(movimientoAbajo[cuentaMovimientos], (coordAncho, coordAlto))
                cuentaMovimientos += 1
                if cuentaMovimientos + 1 >= 4:
                    abajo = False
            else:
                # según la última tecla que se ha pulsado la rana mirará al lado correspondiente para seguir el movimiento
                # de manera más natural.
                if pulsadoI == True:
                    self.marco.blit(avatar, (coordAncho, coordAlto))
                elif pulsadoD == True:
                    self.marco.blit(avatarDcha, (coordAncho, coordAlto))
                elif pulsadoUp == True:
                    self.marco.blit(avatarArriba, (coordAncho, coordAlto))
                elif pulsadoDown == True:
                    self.marco.blit(avatarAbajo, (coordAncho, coordAlto))
                else:
                    self.marco.blit(avatar, (coordAncho, coordAlto))

            # Evitar atropellos carretera.
            # Cuando coincidan las coordinadas de alto con la del carril.
            if coordAlto == carril1Loc:
                for c in carril1:
                    # Posición del ítem y coordenadas en las que está junto
                    # con el tamaño de los objetos de la lista.
                    salir = self.choque(c, coordAncho, 89)
                    if salir == False:
                        sonidoAtrop.play()
                        self.gameover(marco, puntos, disponibles, retroceso, coordAncho, coordAlto, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown )
                        break

            if coordAlto == carril2Loc:
                for c in carril2:
                    salir = self.choque(c, coordAncho, 207)
                    if salir == False:
                        sonidoAtrop.play()
                        self.gameover(marco, puntos, disponibles, retroceso, coordAncho, coordAlto, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown)
                        break

            if coordAlto == carril3Loc:
                for c in carril3:
                    salir = self.choque(c, coordAncho, 89)
                    if salir == False:
                        sonidoAtrop.play()
                        self.gameover(marco, puntos, disponibles, retroceso, coordAncho, coordAlto, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown)
                        break

            # Saltar a troncos en el agua.
            natacion = True

            if coordAlto == canal1Loc:
                for c in canal1:
                    natacion = self.choque(c, coordAncho, 175)
                    # Si cae al agua o llega a la posición final de pantalla.
                    if natacion == False or coordAncho == 1100:
                        break
                if natacion == False:
                    # Si se ha montado en el tronco o tortugas se moverá con ellos.
                    coordAncho = coordAncho + velocidad2
                else:
                    salir = False
                    if salir == False:
                        sonidoAgua.play()
                        self.gameover(marco, puntos, disponibles, retroceso, coordAncho, coordAlto, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown)
                        break

            if coordAlto == canal2Loc:
                for c in canal2:
                    natacion = self.choque(c, coordAncho, 186)
                    if natacion == False or coordAncho == 0:
                        break
                if natacion == False:
                    coordAncho = coordAncho + velocidad3
                else:
                    salir = False
                    if salir == False:
                        sonidoAgua.play()
                        self.gameover(marco, puntos, disponibles, retroceso, coordAncho, coordAlto, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown)
                        break

            if coordAlto == canal3Loc:
                for c in canal3:
                    natacion = self.choque(c, coordAncho, 246)
                    if natacion == False or coordAncho == 1100:
                        break
                if natacion == False:
                    coordAncho = coordAncho + velocidad1
                else:
                    salir = False
                    if salir == False:
                        sonidoAgua.play()
                        self.gameover(marco, puntos, disponibles, retroceso, coordAncho, coordAlto, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown)
                        break

            # Meta
            if coordAlto == 36:
                puntos += 500
                ranas.append(coordAncho)
                disponibles -= 1
                coordAlto = 576
                sonidoVida.play()
                coordAncho = 1038

            retroceso -= 0.35
            if retroceso == 0:
                self.fin(marco, puntos, disponibles, retroceso)
                break
            if disponibles == 0:
                self.fin(marco, puntos, disponibles, retroceso)
                break

            clock.tick(10)
            pygame.display.flip()

#################################################################################################
    # Métodos.
    def fondo(self, marco, puntos, retroceso, disponibles):
        # Creación del fondo.
        self.marco = marco
        self.marco.fill(BLANCO)

        # Colocación del fondo. Los cálculos están tomados sobre los valores de las imágenes para que queden proporcionados.
        # Se ha dejado la valoración numérica por facilidad a la hora de insertar los elementos en movimiento. En el fichero
        # de comentarios se puede ver cómo lo realicé.
        pygame.draw.rect(marco, NEGRO, (0, 576, ancho, 576))
        self.marco.blit(carretera, (0, 330))
        pygame.draw.rect(marco, MORADO, (0, 514, ancho, 62))
        pygame.draw.rect(marco, MORADO, (0, 278, ancho, 62))
        self.marco.blit(agua, (0, 85))
        self.marco.blit(meta, (0, 20))
        pygame.draw.rect(marco, NEGRO, (0, 0, ancho, 20))
        puntuacion = titulos.render('PUNTOS  ' + str(puntos), True, ROJO)
        self.marco.blit(puntuacion, (10, 638))
        tiempo = titulos.render('Tiempo ', True, BLANCO)
        self.marco.blit(tiempo, (475, 638))
        pygame.draw.rect(marco, BLANCO, (600, 638, retroceso, 30))
        salvadas = textos.render('Salvadas ' + str(len(ranas)), True, ROJO)
        self.marco.blit(salvadas, (10, 0))
        vidas = textos.render('Vidas ' + str(disponibles), True, ROJO)
        self.marco.blit(vidas, (1020, 0))

    def carretera(self, marco):
        self.marco = marco

        for c in carril1:
            self.marco.blit(cocheAmI, (c, carril1Loc))

        for c in carril2:
            self.marco.blit(camion2, (c, carril2Loc))

        for c in carril3:
            self.marco.blit(cocheBlI, (c, carril3Loc))

    def lago(self, marco):
        self.marco = marco

        for c in canal1:
            self.marco.blit(tronco2, (c, canal1Loc))

        for c in canal2:
            self.marco.blit(tortuga, (c, canal2Loc))

        for c in canal3:
            self.marco.blit(tronco1, (c, canal3Loc))

    def choque(self, c, coordAncho, tamAvatar):
        # c será la posición del ítem en la lista, si colisiona
        # con el avatar lo habrá atropellado o se montará en el
        # mismo si es en la parte del agua.
        if coordAncho >= c and coordAncho <= c + tamAvatar:
            return False
        elif coordAncho + 58 >= c and coordAncho + 58 <= c + tamAvatar:
            return False
        return True

    def gameover(self, marco, punto, disponibles, retroceso, x, y, izquierda, derecha, arriba, abajo, pulsadoI, pulsadoD, pulsadoUp, pulsadoDown):
        pygame.display.flip()

        self.marco.blit(vidaPerdida, (x, y))

        # izquierda = False
        # derecha = False
        # arriba = False
        # abajo = False
        # pulsadoI = False
        # pulsadoD = False
        # pulsadoUp = False
        # pulsadoDown = False
        #
        # if(izquierda == False and derecha == False and arriba == False and abajo == False and pulsadoI == False and pulsadoD == False and pulsadoUp == False and pulsadoDown == False):
        #     self.marco.blit(vidaPerdida, (x, y))

        self.fin(marco, punto, disponibles, retroceso)

    def fin(self, marco, puntos, disponibles, retroceso):
        self.marco = marco
        marco.fill(NEGRO)

        if disponibles == 0:
            sonidoGanador.play
            salvadas = inicios.render('Todas las ranas salvadas', True, VERDEFROG)
            ganador = inicios.render('Enhorabuena', True, ROJO)
            puntuacion = titulos.render('PUNTOS  ' + str(puntos), True, ROJO)
            comenzar = recomenzar.render('pulsa espacio para volver a comenzar', True, VERDEFROG)
            self.marco.blit(ganador, (ancho//3, alto//3))
            self.marco.blit(puntuacion, (ancho//3, 350))
            self.marco.blit(salvadas, (ancho//3, 100))
            self.marco.blit(comenzar, (25, 576))
        elif disponibles < 5:
            ganador = inicios.render('Game Over', True, ROJO)
            salvadas = textos.render(str(5-disponibles) + ' ranas salvadas', True, BLANCO)
            puntuacion = titulos.render('PUNTOS  ' + str(puntos), True, BLANCO)
            self.marco.blit(ganador, (ancho//3, alto//3))
            self.marco.blit(puntuacion, (ancho//3, 350))
            self.marco.blit(salvadas, (ancho//3, 100))
            comenzar = recomenzar.render('pulsa espacio para volver a comenzar', True, VERDEFROG)
            self.marco.blit(comenzar, (25, 576))
        elif retroceso <= 0:
            if disponibles < 5:
                salvadas = textos.render(str(5-disponibles) + ' ranas salvadas', True, BLANCO)
                self.marco.blit(salvadas, (ancho//3, 100))

            sonidoTiempo.play()
            ganador = inicios.render('Game Over', True, ROJO)
            tiempo = textos.render('Se acabo el tiempo', True, BLANCO)
            puntuacion = titulos.render('PUNTOS  ' + str(puntos), True, BLANCO)
            self.marco.blit(ganador, (ancho // 3, alto // 3))
            self.marco.blit(puntuacion, (ancho // 3, 350))
            self.marco.blit(tiempo, (ancho // 3, 50))
            comenzar = recomenzar.render('pulsa espacio para volver comenzar', True, VERDEFROG)
            self.marco.blit(comenzar, (25, 576))
        else:
            ganador = inicios.render('Game Over', True, ROJO)
            puntuacion = titulos.render('PUNTOS  ' + str(puntos), True, BLANCO)
            self.marco.blit(ganador, (ancho//3, alto//3))
            self.marco.blit(puntuacion, (ancho//3, 350))
            comenzar = recomenzar.render('pulsa espacio para volver a comenzar', True, VERDEFROG)
            self.marco.blit(comenzar, (25, 576))

        # Contador para ir quitando segundos al tiempo
        retroceso = 480
        # Control de vidas.
        disponibles = 5
        puntos = 0
        ranas.clear()