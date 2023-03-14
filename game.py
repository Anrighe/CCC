import pygame
from player import Player
from PIL import Image
from item import Item
import random
import math
from cat import Cat


class CCC:
    def __init__(self):
        pygame.init()

        self.screenWidth = 1366
        self.screenHeight = 768

        self.playerStartingX = self.screenWidth/2
        self.playerStartingY = self.screenHeight/2

        self.playerSprite = Image.open('assets\\sprites\\CCC-walkFront1.png')
        self.playerSpriteBoost = 1.5
        self.playerWidth = self.playerSprite.width * self.playerSpriteBoost
        self.playerHeight = self.playerSprite.height * self.playerSpriteBoost
        self.isPlayerMoving = False

        self.fps = 0
        self.delta = 0

        self.background = pygame.image.load('assets\\sprites\\CCC-backgroundClosedDoor.png')
        self.mapBorder = 60

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.clock = pygame.time.Clock()
        self.player = Player(self.playerStartingX, self.playerStartingY, self.playerWidth, self.playerHeight)
        self.allSprites = pygame.sprite.Group()

        self.itemNumber = 5
        self.maxItemNumber = 8
        self.items = [Item(random.randint(self.mapBorder, self.screenWidth-self.mapBorder),
                      random.randint(self.mapBorder, self.screenHeight-self.mapBorder), 40, 40)
                      for _ in range(self.itemNumber)]

        self.itemRespawnInterval = 1000
        self.pickedUpItems = 0

        self.wtf = False
        self.wtfEffectTimer = 0
        self.wtfDuration = 10000

        for item in self.items:
            self.allSprites.add(item)
        self.allSprites.add(self.player)

        self.running = False
        self.keyPressed = None
        self.keys = None

        self.wobbleAmplitude = 4
        self.wobbleFrequency = 0.4
        self.wobbleOffset = 0
        self.wobbleDelta = 0

        self.cat = Cat(self.screenWidth - self.mapBorder, self.screenHeight//2 + 40)

    def run(self):
        self.running = True
        while self.running:

            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'CCC - {int(self.fps)}')

            # For some reason to me unknown, by specifying the desired frame rate one more time before calculating
            # the delta it will solve a movement bug which was causing the player to not inconstantly over time
            self.clock.tick(144)
            self.delta = self.clock.tick(144) / 1000.0  # delta = time required to output a frame

            # Determine and apply wobble to items
            self.wobbleOffset += 0.1
            self.wobbleDelta = math.sin(self.wobbleOffset * self.wobbleFrequency) * self.wobbleAmplitude
            for item in self.items:
                item.rect.y = item.originalY + self.wobbleDelta

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
        if any(self.keyPressed):
            if self.player.walkingSoundEffectTimer + self.player.walkingSoundEffectInterval < pygame.time.get_ticks():
                if self.player.velocityX != 0 and self.player.velocityY:
                    self.player.playWalkingSound()
                    self.player.walkingSoundEffectTimer = pygame.time.get_ticks()

        if (self.keyPressed[pygame.K_LEFT] or self.keyPressed[pygame.K_a]) and (self.keyPressed[pygame.K_RIGHT] or self.keyPressed[pygame.K_d]):
            self.player.resetVelocityX()
        else:
            if self.keyPressed[pygame.K_LEFT] or self.keyPressed[pygame.K_a]:
                if self.player.rect.x >= self.mapBorder:
                    self.isPlayerMoving = True
                    self.player.moveLeft(self.delta)
                else:
                    self.player.resetVelocityX()

            if self.keyPressed[pygame.K_RIGHT] or self.keyPressed[pygame.K_d]:
                if self.player.rect.x <= self.screenWidth - self.playerWidth - self.mapBorder:
                    self.isPlayerMoving = True
                    self.player.moveRight(self.delta)
                else:
                    self.player.resetVelocityX()

        if (self.keyPressed[pygame.K_UP] or self.keyPressed[pygame.K_w]) and (self.keyPressed[pygame.K_DOWN] or self.keyPressed[pygame.K_s]):
            self.player.resetVelocityY()
        else:
            if self.keyPressed[pygame.K_UP] or self.keyPressed[pygame.K_w]:
                if self.player.rect.y >= self.mapBorder - self.playerHeight / 4:
                    self.isPlayerMoving = True
                    self.player.moveUp(self.delta)
                else:
                    self.player.resetVelocityY()

            if self.keyPressed[pygame.K_DOWN] or self.keyPressed[pygame.K_s]:
                if self.player.rect.y <= self.screenHeight - self.playerHeight - self.mapBorder:
                    self.isPlayerMoving = True
                    self.player.moveDown(self.delta)
                else:
                    self.player.resetVelocityY()

        if self.isPlayerMoving:
            self.player.inertia(self.delta, self.mapBorder, self.screenWidth - self.mapBorder - self.playerWidth,
                                self.mapBorder - self.playerHeight / 4,
                                self.screenHeight - self.playerHeight - self.mapBorder)

        if not any(self.keyPressed) and self.player.velocityX == 0 and self.player.velocityY == 0:
            self.player.standStill()
            self.isPlayerMoving = False

    def checkCollision(self):
        for item in self.items:
            if self.player.rect.colliderect(item):
                item.kill()
                self.items.remove(item)
                self.pickedUpItems += 1
                item = Item(random.randint(self.mapBorder, self.screenWidth - (self.mapBorder * 2)),
                            random.randint(self.mapBorder, self.screenHeight - (self.mapBorder * 2)), 40, 40)
                item.respawnTimer = pygame.time.get_ticks()
                self.items.append(item)
            if item.respawnTimer + self.itemRespawnInterval < pygame.time.get_ticks():
                self.allSprites.add(item)

        if self.player.rect.colliderect(self.cat.catArea) and self.cat.meowTimer + self.cat.meowDelay < pygame.time.get_ticks():
            self.cat.meow()
            self.cat.meowTimer = pygame.time.get_ticks()

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
