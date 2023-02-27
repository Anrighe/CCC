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
        self.playerSpriteBoost = 5
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

        self.item = Item(random.randint(self.mapBorder, self.screenWidth-self.mapBorder),
                         random.randint(self.mapBorder, self.screenHeight-self.mapBorder),
                         40, 40)

        self.allSprites.add(self.item)
        self.allSprites.add(self.player)

        self.running = False
        self.keyPressed = None
        self.keys = None

        self.wobble_amplitude = 4
        self.wobble_frequency = 0.4
        self.wobble_offset = 0
        self.wobble_delta = 0

    def run(self):
        self.running = True
        while self.running:

            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'CCC - {int(self.fps)}')

            self.delta = self.clock.tick(144) / 1000.0

            self.wobble_offset += 0.1
            self.wobble_delta = math.sin(self.wobble_offset * self.wobble_frequency) * self.wobble_amplitude
            self.item.rect.y = self.item.originalY + self.wobble_delta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Storing the key pressed in a new variable using key.get_pressed() method
            self.keyPressed = pygame.key.get_pressed()

            # Changing the coordinates of the player
            if self.keyPressed[pygame.K_LEFT] or self.keyPressed[pygame.K_a]:
                if self.player.rect.x >= 0 + self.mapBorder:
                    self.player.moveLeft(self.delta)

            if self.keyPressed[pygame.K_RIGHT] or self.keyPressed[pygame.K_d]:
                if self.player.rect.x <= self.screenWidth-self.playerWidth - self.mapBorder:
                    self.player.moveRight(self.delta)

            if self.keyPressed[pygame.K_UP] or self.keyPressed[pygame.K_w]:
                if self.player.rect.y >= 0 + self.mapBorder - self.playerHeight/4:
                    self.player.moveUp(self.delta)

            if self.keyPressed[pygame.K_DOWN] or self.keyPressed[pygame.K_s]:
                if self.player.rect.y <= self.screenHeight-self.playerHeight - + self.mapBorder:
                    self.player.moveDown(self.delta)

            self.screen.blit(self.background, (0, 0))
            self.allSprites.draw(self.screen)

            if self.player.rect.colliderect(self.item.rect):
                self.item.kill()
                self.item = Item(random.randint(self.mapBorder, self.screenWidth - (self.mapBorder * 2)),
                                 random.randint(self.mapBorder, self.screenHeight - (self.mapBorder * 2)),
                                 40, 40)

                self.allSprites.add(self.item)
                pygame.display.update()

            pygame.display.flip()

        pygame.quit()
