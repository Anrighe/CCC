import pygame


class Door:
    def __init__(self, x, y):
        self.doorArea = pygame.Rect(x, y, 200, 50)

        self.doorInteraction = 0
        self.doorRingKnockSoundEffects = [pygame.mixer.Sound('assets\\audio\\CCC-doorbell.mp3'),
                                          pygame.mixer.Sound('assets\\audio\\CCC-doorKnocking.mp3')]
        for sound in self.doorRingKnockSoundEffects:
            sound.set_volume(0.1)

        self.doorOpeningSoundEffects = [pygame.mixer.Sound('assets\\audio\\CCC-openingDoor.mp3'),
                                        pygame.mixer.Sound('assets\\audio\\CCC-slammingDoor.mp3')]
        for sound in self.doorOpeningSoundEffects:
            sound.set_volume(0.3)

        self.openDoor = False


