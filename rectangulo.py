import pygame

class Rectangulo(pygame.sprite.Sprite):
    def __init__(self, COLOR, cord_x, cord_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(COLOR)
        #Obtiene el rectángulo de la clase Sprite.
        self.rect = self.image.get_rect()
        self.incre = 10
        self.rect.x = cord_x
        self.rect.y = cord_y

    def update(self, y_top, y_bottom, anchoPantalla):
        #Cuando acabe la pantalla poner a 0 para volver a empezar.
        if self.rect.right > anchoPantalla:
            self.rect.x = 0
        #Si la y es mayor que el margen de abajo pasado por parámetro o menor que
        #el margen superior decrementar.
        if self.rect.y > y_bottom or self.rect.y < y_top:
            self.incre = -self.incre

        self.rect.x += 10
        self.rect.y += self.incre


