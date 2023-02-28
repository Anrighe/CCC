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
        self.velocity = 500

        self.spriteTimer = 0
        self.walkingInterval = 150

        self.lastMovementLeft = None

    def moveLeft(self, delta):
        self.rect.x -= self.velocity * delta
        self.lastMovementLeft = True  # Temporary
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.sprites)
            self.image = self.sprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.image = pygame.transform.flip(self.image, True, False)
            self.spriteTimer = pygame.time.get_ticks()

    def moveRight(self, delta):
        self.rect.x += self.velocity * delta
        self.lastMovementLeft = False  # Temporary
        if self.spriteTimer + self.walkingInterval < pygame.time.get_ticks():
            self.spritesIndex = (self.spritesIndex + 1) % len(self.sprites)
            self.image = self.sprites[self.spritesIndex]
            self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))
            self.spriteTimer = pygame.time.get_ticks()

    def moveUp(self, delta):
        self.rect.y -= self.velocity * delta

    def moveDown(self, delta):
        self.rect.y += self.velocity * delta

    def standStill(self):
        self.image = pygame.image.load('assets\\player.png')
        self.image = pygame.transform.scale(self.image, (self.playerWidth, self.playerHeight))

        if self.lastMovementLeft:
            self.image = pygame.transform.flip(self.image, True, False)
