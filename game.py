import pygame
from player import Player
from PIL import Image
from item import Item
import random
import math
from cat import Cat
from door import Door
from inspector import Inspector

GAME_PHASE_1 = 1  # Collecting items
GAME_PHASE_2 = 2  # Avoiding items


class CCC:
    def __init__(self):
        pygame.init()
        pygame.mixer.set_num_channels(10)

        self.screenWidth = 1366
        self.screenHeight = 768
        self.mapBorder = 60

        self.playerStartingX = self.screenWidth/2
        self.playerStartingY = self.screenHeight/2

        self.playerSprite = Image.open('assets\\sprites\\CCC-walkFront1.png')
        self.playerSpriteBoost = 1.5
        self.playerWidth = self.playerSprite.width * self.playerSpriteBoost
        self.playerHeight = self.playerSprite.height * self.playerSpriteBoost
        self.isPlayerMoving = False

        self.running = True
        self.fps = 0
        self.delta = 0

        self.level = 0

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.clock = pygame.time.Clock()
        self.player = Player(self.playerStartingX, self.playerStartingY, self.playerWidth, self.playerHeight)
        self.allSprites = pygame.sprite.Group()

        self.backgroundSprites = [pygame.image.load('assets\\sprites\\CCC-backgroundClosedDoor.png').convert_alpha(),
                                  pygame.image.load('assets\\sprites\\CCC-backgroundOpenDoor.png').convert_alpha()]
        self.background = self.backgroundSprites[0]

        self.soundtrack = pygame.mixer.Sound('assets\\audio\\CCC-Sountrack1.mp3')
        self.soundtrack.set_volume(0.03)
        self.soundtrackEndEvent = pygame.USEREVENT + 1
        pygame.mixer.Channel(9).set_endevent(self.soundtrackEndEvent)
        pygame.mixer.Channel(9).play(self.soundtrack)

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

        self.keyPressed = None
        self.keys = None

        self.wobbleAmplitude = 4
        self.wobbleFrequency = 0.4
        self.wobbleOffset = 0
        self.wobbleDelta = 0

        self.cat = Cat(self.screenWidth - self.mapBorder, self.screenHeight//2 + 40)

        self.score = 0
        self.scoreSurface = pygame.font.Font(None, 36).render("Score: {}".format(self.score), True, (255, 255, 255))

        self.gameStatus = GAME_PHASE_1
        self.phase1Timer = 0
        self.phase2Timer = 0
        self.phase1Duration = 5000  # milliseconds
        self.phase2Duration = 20000  # milliseconds
        self.inspectorActionInterval = 1000  # milliseconds
        self.inspectorStepTimer = 0
        self.inspectorDoorInteractionTimer = 0
        self.inspectorApproaching = False

        self.inspectorTransformDimension = 100
        self.inspectorSpawnPositionX = (self.screenWidth / 2) - (self.inspectorTransformDimension / 2)
        self.inspectorSpawnPositionY = -25
        self.inspector = Inspector(self.inspectorSpawnPositionX, self.inspectorSpawnPositionY, self.inspectorTransformDimension)
        self.inspectorWalkingInsideSoundEffects = [pygame.mixer.Sound(f'assets\\audio\\CCC-inspectorWalkingInside{i}.mp3')
                                                   for i in range(1, 4)]
        self.inspectorWalkingOutsideSoundEffect = pygame.mixer.Sound('assets\\audio\\CCC-inspectorWalkingOutside.mp3')
        self.inspectorWalkingOutsideSoundEffect.set_volume(0.2)

        self.door = Door(self.screenWidth / 2, 0)

        self.gameOver = False
        self.gameOverFont = pygame.font.Font(None, 36)
        self.gameOverText = self.gameOverFont.render("Game Over", True, (255, 0, 0))
        self.gameOverRect = self.gameOverText.get_rect(center=(320, 240))
        self.gameOverTextRect = None

    def run(self):
        while self.running:

            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'CCC - {int(self.fps)}')

            # For some reason to me unknown, by specifying the desired frame rate one more time before calculating
            # the delta it will solve a movement bug which was causing the player to not inconstantly over time
            self.clock.tick(144)
            self.delta = self.clock.tick(144) / 1000.0  # delta = time required to output a frame

            # Determine and apply wobble to items
            if self.gameStatus == GAME_PHASE_1:
                self.wobbleOffset += 0.1
                self.wobbleDelta = math.sin(self.wobbleOffset * self.wobbleFrequency) * self.wobbleAmplitude
                for item in self.items:
                    item.rect.y = item.originalY + self.wobbleDelta

            for event in pygame.event.get():
                if event.type == self.soundtrackEndEvent:
                    pygame.mixer.Channel(9).play(self.soundtrack)

                if event.type == pygame.QUIT:
                    pygame.quit()

            # Storing the key pressed in a new variable using key.get_pressed() method
            self.keyPressed = pygame.key.get_pressed()

            if self.gameOver:
                self.drawGameOver()
            else:

                self.updateGamePhase()

                self.updateItemsPosition(self.delta, self.screenWidth, self.screenHeight, self.mapBorder)

                self.checkPlayerStatus()

                self.checkCollision()

                self.updateBackground()

                self.drawBackground()

                self.allSprites.draw(self.screen)

                pygame.display.flip()

        pygame.quit()

    def checkPlayerStatus(self):
        if any(self.keyPressed):
            if self.player.walkingSoundEffectTimer + self.player.walkingSoundEffectInterval < pygame.time.get_ticks():
                if self.player.velocityX != 0 or self.player.velocityY != 0:
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
                self.pickupItem()
                if self.door.openDoor:
                    self.inspector.seenPickup = True
            if item.respawnTimer + self.itemRespawnInterval < pygame.time.get_ticks():
                self.allSprites.add(item)

        if self.player.rect.colliderect(self.cat.catArea) or self.inspector.rect.colliderect(self.cat.catArea) \
                and self.cat.meowTimer + self.cat.meowDelay < pygame.time.get_ticks():
            self.cat.meow()
            self.cat.meowTimer = pygame.time.get_ticks()

        if self.inspector.seenPickup and self.player.rect.colliderect(self.inspector.rect) and self.inspector.inside:
            self.gameOver = True

    def pickupItem(self):
        self.score += 100
        self.scoreSurface = pygame.font.Font(None, 36).render("Score: {}".format(self.score), True, (255, 255, 255))

    def updateItemsPosition(self, delta, screenWidth, screenHeight, mapBorder):
        if self.gameStatus == GAME_PHASE_2:
            for item in self.items:
                item.move(delta, screenWidth, screenHeight, mapBorder)

    def updateGamePhase(self):
        if self.gameStatus == GAME_PHASE_1 and self.phase1Timer + self.phase1Duration < pygame.time.get_ticks():
            print("PHASE 2")  # Debug
            self.gameStatus = GAME_PHASE_2
            self.phase2Timer = pygame.time.get_ticks()

        elif self.gameStatus == GAME_PHASE_2 and self.phase2Timer + self.phase2Duration < pygame.time.get_ticks():
            print("PHASE 1")  # Debug
            self.gameStatus = GAME_PHASE_1
            self.phase1Timer = pygame.time.get_ticks()

    def updateBackground(self):
        if self.gameStatus == GAME_PHASE_1:
            self.inspector.inside = False
            self.inspector.seenPickup = False
            self.inspectorApproaching = False
            self.door.openDoor = False
            self.door.doorInteractionCount = 0
            if self.background == self.backgroundSprites[1]:
                pygame.mixer.Channel(2).play(self.door.doorOpeningSoundEffects[1])

            self.background = self.backgroundSprites[0]
            self.allSprites.remove(self.inspector)
            self.inspector.resetPosition()
            self.gameStatus = GAME_PHASE_1

        elif not self.door.openDoor:
            if not self.inspectorApproaching:
                self.inspectorApproaching = True
                pygame.mixer.Channel(1).play(self.inspectorWalkingOutsideSoundEffect)
                self.inspectorStepTimer = self.inspectorDoorInteractionTimer = pygame.time.get_ticks()

            if self.inspectorDoorInteractionTimer + 5000 < pygame.time.get_ticks():
                self.door.doorInteractionCount += 1

                self.inspectorDoorInteractionTimer = pygame.time.get_ticks()
                pygame.mixer.Channel(2).play(random.choice(self.door.doorRingKnockSoundEffects))

            # If the player doesn't open the door in time, it will be slammed open
            if self.door.doorInteractionCount >= 3 and self.inspectorDoorInteractionTimer + 3000 < pygame.time.get_ticks():
                pygame.mixer.Channel(2).play(self.door.doorOpeningSoundEffects[1])
                self.phase2Timer += self.phase2Duration//2
                self.background = self.backgroundSprites[1]
                self.allSprites.add(self.inspector)
                self.door.openDoor = True
            else:
                if self.player.rect.colliderect(self.door.doorArea) and self.inspectorStepTimer + 3000 < pygame.time.get_ticks():
                    self.phase2Timer += self.phase2Duration // 4
                    pygame.mixer.Channel(2).play(self.door.doorOpeningSoundEffects[0])
                    self.background = self.backgroundSprites[1]
                    self.allSprites.add(self.inspector)
                    self.door.openDoor = True
        elif not self.inspector.inside:
            self.inspector.enter()
        elif self.inspector.seenPickup:  # the door is open and the inspector has seen the player picking up an item
            if not self.inspector.isMoving():
                self.inspector.scanPlayerPosition(self.player.rect.x + (self.player.playerWidth / 2),
                                                  self.player.rect.y + (self.player.playerHeight / 2))
            self.inspector.chasePlayer(self.delta, self.screenWidth, self.screenHeight, self.mapBorder)
            self.inspector.inertia()


        #OLD WTF MODE
        #if self.pickedUpItems < 10:
            #self.screen.blit(self.background, (0, 0))
            #self.screen.blit(self.scoreSurface, (10, 10))
        #else:
            #if not self.wtf:
                #self.wtfEffectTimer = pygame.time.get_ticks()
            #self.wtf = True
            #if self.wtf and self.wtfEffectTimer + self.wtfDuration < pygame.time.get_ticks():
                #self.pickedUpItems = 0
                #self.wtf = False

    def drawBackground(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.scoreSurface, (10, 10))

    def drawGameOver(self):
        self.screen.fill((0, 0, 0))
        self.gameOverTextRect = self.gameOverText.get_rect(center=(self.screenWidth / 2, self.screenHeight / 2))
        self.screen.blit(self.gameOverText, self.gameOverTextRect)
        pygame.display.update()

        if any(self.keyPressed):
            self.__init__()


