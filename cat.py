import pygame


class Cat:
    def __init__(self, x, y):
        self.catSoundEffect = pygame.mixer.Sound('assets\\audio\\CCC-cat.mp3')
        self.catSoundEffect.set_volume(0.2)
        self.catArea = pygame.Rect(x, y, 10, 10)
        #self.rect.x = x
        #self.rect.y = y
        self.meowDelay = 15000
        self.meowTimer = 0

    def meow(self):
        self.catSoundEffect.play()
