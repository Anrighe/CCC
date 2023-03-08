import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.playerWidth = width
        self.playerHeight = height

        self.walkFrontSprites = []
        self.walkBackSprites = []
        self.walkLeftSprites = []
        self.walkRightSprites = []

        self.spriteLoader()
        self.spritesIndex = 0

        self.image = pygame.image.load('assets\\player.png')
        self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.velocityX = 0
        self.velocityY = 0
        self.standardSpeed = 400
        self.inertiaCoefficient = 6

        self.spriteTimer = 0
        self.walkingInterval = 150

        self.lastMovementLeft = None

    # In each movement calculation the truncation of floating-point (velocity * delta) will be avoided
    # by converting it to an integer before adding it to the integer variable self.rect.x

    def moveLeft(self, delta):
        self.velocityX = - self.standardSpeed
        self.rect.x += int(self.velocityX * delta)
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.walkLeftSprites)
            self.image = self.walkLeftSprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.spriteTimer = pygame.time.get_ticks()

    def moveRight(self, delta):
        self.velocityX = self.standardSpeed
        self.rect.x += int(self.velocityX * delta)
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.walkRightSprites)
            self.image = self.walkRightSprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.spriteTimer = pygame.time.get_ticks()

    def moveUp(self, delta):
        self.velocityY = - self.standardSpeed
        self.rect.y += int(self.velocityY * delta)
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.walkBackSprites)
            self.image = self.walkBackSprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.spriteTimer = pygame.time.get_ticks()

    def moveDown(self, delta):
        self.velocityY = self.standardSpeed
        self.rect.y += int(self.velocityY * delta)
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.walkFrontSprites)
            self.image = self.walkFrontSprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.spriteTimer = pygame.time.get_ticks()

    def inertia(self, delta, borderLeft, borderRight, borderUp, borderDown):

        # X-axis inertia
        if self.rect.x < borderLeft or self.rect.x > borderRight:
            self.resetVelocityX()

        if self.velocityX > self.inertiaCoefficient:
            self.velocityX -= self.inertiaCoefficient
        elif self.velocityX < -self.inertiaCoefficient:
            self.velocityX += self.inertiaCoefficient
        else:
            self.resetVelocityX()

        # Y-axis inertia
        if self.rect.y < borderUp or self.rect.y > borderDown:
            self.resetVelocityY()

        if self.velocityY > self.inertiaCoefficient:
            self.velocityY -= self.inertiaCoefficient
        elif self.velocityY < -self.inertiaCoefficient:
            self.velocityY += self.inertiaCoefficient
        else:
            self.resetVelocityY()

        self.rect.x += int(self.velocityX * delta)
        self.rect.y += int(self.velocityY * delta)

    def standStill(self):
        self.image = pygame.image.load('assets\\sprites\\CCC-walkFront1.png')
        self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))

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
            return True
        else:
            return False

    def resetVelocityX(self):
        self.velocityX = 0

    def resetVelocityY(self):
        self.velocityY = 0

    def spriteLoader(self):
        for i in range(1,7):
            self.walkFrontSprites.append(pygame.image.load(f'assets\\sprites\\CCC-walkFront{i}.png'))
            self.walkBackSprites.append(pygame.image.load(f'assets\\sprites\\CCC-walkBack{i}.png'))
            self.walkLeftSprites.append(pygame.image.load(f'assets\\sprites\\CCC-walkLeft{i}.png'))
            self.walkRightSprites.append(pygame.image.load(f'assets\\sprites\\CCC-walkRight{i}.png'))
