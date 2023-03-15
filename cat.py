import pygame


class Cat:
    def __init__(self, x, y):
        self.catSoundEffect = pygame.mixer.Sound('assets\\audio\\CCC-cat.mp3')
        self.catSoundEffect.set_volume(0.1)
        self.catArea = pygame.Rect(x, y, 20, 20)
        self.meowDelay = 15000
        self.meowTimer = 0

    def meow(self):
        pygame.mixer.Channel(2).play(self.catSoundEffect)
