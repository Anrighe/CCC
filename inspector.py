import pygame
import math
import random


class Inspector(pygame.sprite.Sprite):
    def __init__(self, x, y, transformTargetDimension):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load('assets\\sprites\\CCC-inspector.png').convert_alpha(),
                                            (transformTargetDimension, transformTargetDimension))

        self.transformTargetDimension = transformTargetDimension
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spawnX = x
        self.spawnY = y
        self.readyPositionY = 30
        self.standardSpeed = 1000
        self.inertiaCoefficient = 7
        self.velocityX = 0
        self.velocityY = 0
        
        self.seenPickup = False
        self.inside = False
        self.sprintTimer = 0
        self.sprintInterval = 1500  # milliseconds

        self.lastPlayerPositionX = 0
        self.lastPlayerPositionY = 0
        self.movementDirectionX = None
        self.movementDirectionY = None

    def enter(self):
        if self.rect.y < self.readyPositionY:
            self.rect.y += 1
        else:
            self.inside = True

    def resetPosition(self):
        self.rect.x = self.spawnX
        self.rect.y = self.spawnY

    def isMoving(self):
        if self.velocityX == 0 and self.velocityY == 0:
            return False
        else:
            return True

    def scanPlayerPosition(self, playerX, playerY):
        self.lastPlayerPositionX = playerX
        self.lastPlayerPositionY = playerY

        if self.lastPlayerPositionX < self.rect.x:
            self.movementDirectionX = False
        else:
            self.movementDirectionX = True

        if self.lastPlayerPositionY < self.rect.y:
            self.movementDirectionY = False
        else:
            self.movementDirectionY = True

    def chasePlayer(self, delta, screenWidth, screenHeight, mapBorder):
        if self.movementDirectionX:
            self.rect.x += int(self.velocityX * delta)
            if self.rect.x >= screenWidth - mapBorder - (self.transformTargetDimension / 2):
                self.movementDirectionX = False

        else:
            self.rect.x -= int(self.velocityX * delta)
            if self.rect.x <= 0 + mapBorder:
                self.movementDirectionX = True

        if self.movementDirectionY:
            self.rect.y += int(self.velocityY * delta)
            if self.rect.y >= screenHeight - mapBorder - (self.transformTargetDimension / 2):
                self.movementDirectionY = False
        else:
            self.rect.y -= int(self.velocityY * delta)
            if self.rect.y <= 0 + mapBorder - (self.transformTargetDimension / 2):
                self.movementDirectionY = True

        if self.velocityX == 0 and self.velocityY == 0:
            self.velocityX = int(math.fabs((self.rect.x - self.lastPlayerPositionX)) * 2 + random.randint(0, self.standardSpeed))
            self.velocityY = int(math.fabs((self.rect.y - self.lastPlayerPositionY)) * 2 + random.randint(0, self.standardSpeed))
            
    def inertia(self):
        if self.rect.x and self.velocityX >= 1:
            self.velocityX = max(self.velocityX - self.inertiaCoefficient, 0)

        if self.velocityY >= 1:
            self.velocityY = max(self.velocityY - self.inertiaCoefficient, 0)





