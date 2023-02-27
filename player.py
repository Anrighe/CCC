import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.image.load('assets\\playerDebug.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.velocity = 500

        self.isFlipped = False

    def moveLeft(self, delta):
        self.rect.x -= self.velocity * delta
        if not self.isFlipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.isFlipped = True

    def moveRight(self, delta):
        self.rect.x += self.velocity * delta
        if self.isFlipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.isFlipped = False

    def moveUp(self, delta):
        self.rect.y -= self.velocity * delta

    def moveDown(self, delta):
        self.rect.y += self.velocity * delta
