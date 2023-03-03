import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.playerWidth = width
        self.playerHeight = height

        self.sprites = [pygame.image.load('assets\\player.png'),
                        pygame.image.load('assets\\playerWalk1.png')]
        self.spritesIndex = 0

        self.image = pygame.image.load('assets\\player.png')
        self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.velocityX = 0
        self.velocityY = 0
        self.standardSpeed = 400

        self.spriteTimer = 0
        self.walkingInterval = 150

        self.lastMovementLeft = None

    def moveLeft(self, delta):
        self.velocityX = - self.standardSpeed
        self.rect.x += self.velocityX * delta
        self.lastMovementLeft = True  # Temporary
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.sprites)
            self.image = self.sprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.image = pygame.transform.flip(self.image, True, False)
            self.spriteTimer = pygame.time.get_ticks()

    def moveRight(self, delta):
        self.velocityX = self.standardSpeed
        self.rect.x += self.velocityX * delta
        self.lastMovementLeft = False  # Temporary
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.sprites)
            self.image = self.sprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.spriteTimer = pygame.time.get_ticks()

    def moveUp(self, delta):
        self.velocityY = - self.standardSpeed
        self.rect.y += self.velocityY * delta

    def moveDown(self, delta):
        self.velocityY = self.standardSpeed
        self.rect.y += self.velocityY * delta

    def inertia(self, delta):
        if self.velocityX > 1:
            self.velocityX -= 20
        elif self.velocityX < -1:
            self.velocityX += 20
        else:
            self.velocityX = 0

        if self.velocityY > 1:
            self.velocityY -= 20
        elif self.velocityY < -1:
            self.velocityY += 20
        else:
            self.velocityY = 0

        self.rect.x += self.velocityX * delta
        self.rect.y += self.velocityY * delta

    def standStill(self):
        self.image = pygame.image.load('assets\\player.png')
        self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))

        if self.lastMovementLeft:
            self.image = pygame.transform.flip(self.image, True, False)

    def isPlayerOnAnyBorder(self, width, height, border):
        if self.rect.x <= border or self.rect.x >= width-border or self.rect.y <= border or self.rect.y >= height-border:
            return True
        else:
            return False

    def isPlayerOnXBorder(self, width, border):
        if self.rect.x <= border or self.rect.x >= width - border:
            return True
        else:
            return False

    def isPlayerOnYBorder(self, height, border):
        if self.rect.y <= border or self.rect.y >= height-border:
            print("in TOP border", self.rect.y)
            return True
        else:
            return False

    def resetVelocityX(self):
        self.velocityX = 0

    def resetVelocityY(self):
        self.velocityY = 0
