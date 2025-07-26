import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class PowerUp(Sprite):
    """A class to manage the power-up.
    """

    def __init__(self, game: 'AlienInvasion', center):
        """Initialize the power-up and set its starting position.
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.powerup_file)
        self.image = pygame.transform.scale(self.image, (self.settings.powerup_w, self.settings.powerup_h))
        self.rect = self.image.get_rect()

        self.rect.center = center

        self.y = float(self.rect.y)


    def update(self):
        """Move the power-up down the screen.
        """
        self.y += self.settings.powerup_speed
        self.rect.y = self.y


    def draw(self):
        """Draw the power-up to the screen.
        """
        self.screen.blit(self.image, self.rect)