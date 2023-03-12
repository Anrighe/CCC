import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.image.load('assets\\genericItemPlaceholder.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.originalY = y
        self.velocity = 500
        self.respawnTimer = 0
