import sys
import pygame
from game import CCC


class Menu:
    def __init__(self):
        pygame.init()

        self.screenWidth = 800
        self.screenHeight = 600

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.surface = pygame.Surface((self.screenWidth, self.screenHeight))

        self.buttonWidth = 200
        self.buttonHeight = 50
        self.buttonPadding = 100
        self.buttonColor = (255, 0, 0)
        self.buttonHoverColor = (0, 0, 255)
        self.buttonTextColor = (255, 255, 255)

        self.startButtonRect = pygame.Rect((self.screenWidth - self.buttonWidth) / 2,
                                           (self.screenHeight - self.buttonHeight) / 2 - self.buttonHeight,
                                           self.buttonWidth, self.buttonHeight)

        self.settingsButtonRect = pygame.Rect((self.screenWidth - self.buttonWidth) / 2,
                                              self.startButtonRect.y + self.buttonPadding,
                                              self.buttonWidth, self.buttonHeight)

        self.exitButtonRect = pygame.Rect((self.screenWidth - self.buttonWidth) / 2,
                                          self.settingsButtonRect.y + self.buttonPadding,
                                          self.buttonWidth, self.buttonHeight)

        pygame.mixer.set_num_channels(10)

        self.menuSoundtrack = pygame.mixer.Sound('assets\\audio\\CCC-mainMenu.wav')
        self.menuSoundtrack.set_volume(0.04)
        self.menuSoundtrack.play(-1)

        self.menuHoverSoundEffect = pygame.mixer.Sound('assets\\audio\\CCC-menuHover.mp3')
        self.menuHoverSoundEffect.set_volume(0.02)

        self.startButtonHovered = False
        self.settingsButtonHovered = False
        self.exitButtonHovered = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.startButtonRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        game = CCC()
                        game.run()
                    elif self.settingsButtonRect.collidepoint(pygame.mouse.get_pos()):
                        print("Settings button clicked!")
                    elif self.exitButtonRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()

            # Check if the mouse is hovering over the "start" button
            if self.startButtonRect.collidepoint(pygame.mouse.get_pos()):
                self.startButtonColor = self.buttonHoverColor
                if not self.startButtonHovered:
                    pygame.mixer.Channel(1).play(self.menuHoverSoundEffect)
                    self.startButtonHovered = True
            else:
                self.startButtonColor = self.buttonColor
                self.startButtonHovered = False

            # Check if the mouse is hovering over the "settings" button
            if self.settingsButtonRect.collidepoint(pygame.mouse.get_pos()):
                self.settingsButtonColor = self.buttonHoverColor
                if not self.settingsButtonHovered:
                    pygame.mixer.Channel(1).play(self.menuHoverSoundEffect)
                    self.settingsButtonHovered = True
            else:
                self.settingsButtonColor = self.buttonColor
                self.settingsButtonHovered = False

            # Check if the mouse is hovering over the "exit" button
            if self.exitButtonRect.collidepoint(pygame.mouse.get_pos()):
                self.exitButtonColor = self.buttonHoverColor
                if not self.exitButtonHovered:
                    pygame.mixer.Channel(1).play(self.menuHoverSoundEffect)
                    self.exitButtonHovered = True
            else:
                self.exitButtonColor = self.buttonColor
                self.exitButtonHovered = False

            # Draw the buttons onto the menu surface
            pygame.draw.rect(self.surface, self.startButtonColor, self.startButtonRect)
            pygame.draw.rect(self.surface, self.settingsButtonColor, self.settingsButtonRect)
            pygame.draw.rect(self.surface, self.exitButtonColor, self.exitButtonRect)

            # Render the button labels
            self.startButtonFont = pygame.font.Font(None, 32)
            self.startButtonText = self.startButtonFont.render("Start", True, self.buttonTextColor)
            self.startButtonTextRect = self.startButtonText.get_rect(center=self.startButtonRect.center)
            self.surface.blit(self.startButtonText, self.startButtonTextRect)

            self.settingsButtonFont = pygame.font.Font(None, 32)
            self.settingsButtonText = self.settingsButtonFont.render("Settings", True, self.buttonTextColor)
            self.settingsButtonTextRect = self.settingsButtonText.get_rect(center=self.settingsButtonRect.center)
            self.surface.blit(self.settingsButtonText, self.settingsButtonTextRect)

            self.exitButtonFont = pygame.font.Font(None, 32)
            self.exitButtonText = self.exitButtonFont.render("Exit", True, self.buttonTextColor)
            self.exitButtonTextRect = self.exitButtonText.get_rect(center=self.exitButtonRect.center)
            self.surface.blit(self.exitButtonText, self.exitButtonTextRect)

            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()
