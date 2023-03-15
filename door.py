import pygame


class Door:
    def __init__(self, x, y):
        self.doorArea = pygame.Rect(x, y, 200, 50)

