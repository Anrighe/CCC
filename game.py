import pygame
from player import Player
from PIL import Image
from item import Item
import random
import math


class CCC:
    def __init__(self):
        pygame.init()

        self.screenWidth = 1366
        self.screenHeight = 768

        self.playerStartingX = self.screenWidth/2
        self.playerStartingY = self.screenHeight/2

        self.playerSprite = Image.open('assets\\player.png')
        self.playerSpriteBoost = 3
        self.playerWidth = self.playerSprite.width * self.playerSpriteBoost
        self.playerHeight = self.playerSprite.height * self.playerSpriteBoost

        self.fps = 0
        self.delta = 0

        self.background = pygame.image.load('assets\\background.png')
        self.mapBorder = 50

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.clock = pygame.time.Clock()
        self.player = Player(self.playerStartingX, self.playerStartingY, self.playerWidth, self.playerHeight)
        self.allSprites = pygame.sprite.Group()

        self.item1 = Item(random.randint(self.mapBorder, self.screenWidth-self.mapBorder),
                          random.randint(self.mapBorder, self.screenHeight-self.mapBorder), 40, 40)

        self.item2 = Item(random.randint(self.mapBorder, self.screenWidth-self.mapBorder),
                          random.randint(self.mapBorder, self.screenHeight-self.mapBorder), 40, 40)

        self.item1RespawnTimer = 0
        self.item2RespawnTimer = 0
        self.itemRespawnInterval = 1000
        self.pickedUpItems = 0

        self.wtf = False
        self.wtfEffectTimer = 0
        self.wtfDuration = 10000

        self.allSprites.add(self.item1)
        self.allSprites.add(self.item2)
        self.allSprites.add(self.player)

        self.running = False
        self.keyPressed = None
        self.keys = None

        self.wobbleAmplitude = 4
        self.wobbleFrequency = 0.4
        self.wobbleOffset = 0
        self.wobbleDelta = 0

    def run(self):
        self.running = True
        while self.running:

            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'CCC - {int(self.fps)}')

            self.delta = self.clock.tick(144) / 1000.0  # delta = time required to output a frame

            # Determine and apply wobble to items
            self.wobbleOffset += 0.1
            self.wobbleDelta = math.sin(self.wobbleOffset * self.wobbleFrequency) * self.wobbleAmplitude
            self.item1.rect.y = self.item1.originalY + self.wobbleDelta
            self.item2.rect.y = self.item2.originalY + self.wobbleDelta

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Storing the key pressed in a new variable using key.get_pressed() method
            self.keyPressed = pygame.key.get_pressed()

            self.checkPlayerStatus()

            self.checkCollision()

            self.wtfMode()

            self.allSprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def checkPlayerStatus(self):
        if (self.keyPressed[pygame.K_LEFT] or self.keyPressed[pygame.K_a]) and (self.keyPressed[pygame.K_RIGHT] or self.keyPressed[pygame.K_d]):
            self.player.resetVelocityX()
        else:
            if self.keyPressed[pygame.K_LEFT] or self.keyPressed[pygame.K_a]:
                if self.player.rect.x >= 0 + self.mapBorder:
                    self.player.moveLeft(self.delta)

            if self.keyPressed[pygame.K_RIGHT] or self.keyPressed[pygame.K_d]:
                if self.player.rect.x <= self.screenWidth - self.playerWidth - self.mapBorder:
                    self.player.moveRight(self.delta)

        if (self.keyPressed[pygame.K_UP] or self.keyPressed[pygame.K_w]) and (self.keyPressed[pygame.K_DOWN] or self.keyPressed[pygame.K_s]):
            self.player.resetVelocityY()
        else:
            if self.keyPressed[pygame.K_UP] or self.keyPressed[pygame.K_w]:
                if self.player.rect.y >= 0 + self.mapBorder - self.playerHeight / 4:
                    self.player.moveUp(self.delta)

            if self.keyPressed[pygame.K_DOWN] or self.keyPressed[pygame.K_s]:
                if self.player.rect.y <= self.screenHeight - self.playerHeight - + self.mapBorder:
                    self.player.moveDown(self.delta)

        if not self.player.isPlayerOnAnyBorder(self.screenWidth, self.screenHeight, self.mapBorder):
            self.player.inertia(self.delta)
        else:
            if self.player.isPlayerOnXBorder(self.screenWidth, self.mapBorder):
                self.player.resetVelocityX()
            if self.player.isPlayerOnYBorder(self.screenHeight, self.mapBorder):
                self.player.resetVelocityY()

        if not any(self.keyPressed):
            self.player.standStill()

    def checkCollision(self):
        # Item 1
        if self.player.rect.colliderect(self.item1.rect):
            self.item1.kill()
            self.pickedUpItems += 1
            self.item1 = Item(random.randint(self.mapBorder, self.screenWidth - (self.mapBorder * 2)),
                              random.randint(self.mapBorder, self.screenHeight - (self.mapBorder * 2)), 40, 40)
            self.item1RespawnTimer = pygame.time.get_ticks()

        if self.item1RespawnTimer + self.itemRespawnInterval < pygame.time.get_ticks():
            self.allSprites.add(self.item1)

        # Item 2
        if self.player.rect.colliderect(self.item2.rect):
            self.item2.kill()
            self.pickedUpItems += 1
            self.item2 = Item(random.randint(self.mapBorder, self.screenWidth - (self.mapBorder * 2)),
                              random.randint(self.mapBorder, self.screenHeight - (self.mapBorder * 2)), 40, 40)
            self.item2RespawnTimer = pygame.time.get_ticks()

        if self.item2RespawnTimer + self.itemRespawnInterval < pygame.time.get_ticks():
            self.allSprites.add(self.item2)

    def wtfMode(self):
        if self.pickedUpItems < 10:
            self.screen.blit(self.background, (0, 0))
        else:
            if not self.wtf:
                self.wtfEffectTimer = pygame.time.get_ticks()
            self.wtf = True
            if self.wtf and self.wtfEffectTimer + self.wtfDuration < pygame.time.get_ticks():
                self.pickedUpItems = 0
                self.wtf = False
