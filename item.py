import pygame
import random


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.image.load('assets\\genericItemPlaceholder.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.originalY = y
        self.standardSpeed = 1000
        self.velocityX = random.randint(200, 500)
        self.velocityY = 500
        self.movementDirectionX = random.choice([True, False])
        self.movementDirectionY = random.choice([True, False])
        self.respawnTimer = 0

    def move(self, delta, screenWidth, screenHeight, mapBorder):
        if self.movementDirectionX:
            self.rect.x += int(self.velocityX * delta)
            if self.rect.x >= screenWidth - mapBorder - (50 / 2):
                self.movementDirectionX = False
        else:
            self.rect.x -= int(self.velocityX * delta)
            if self.rect.x <= 0 + mapBorder:
                self.movementDirectionX = True

        if self.movementDirectionY:
            self.rect.y += int(self.velocityX * delta)
            if self.rect.y >= screenHeight - mapBorder - (50 / 2):
                self.movementDirectionY = False
        else:
            self.rect.y -= int(self.velocityX * delta)
            if self.rect.y <= 0 + mapBorder - (50 / 2):
                self.movementDirectionY = True

        self.originalY = self.rect.y
