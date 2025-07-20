import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """Manages the bullets fired from the ship.
    """
    def __init__(self, game: 'AlienInvasion'):
        """Initializes the bullets and determines it's location.

        Args:
            game (AlienInvasion): The main game object.
        """
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.bullet_h, self.settings.bullet_w)                            
            )
        
        self.rect  = self.image.get_rect()
        self.rect.midleft = game.ship.rect.midright
        self.x = float(self.rect.x)


    def update(self):
        """Fires the bullet from left to right.
        """
        self.x += self.settings.bullet_speed
        self.rect.x = self.x


    def draw_bullet(self):
        """Draws the bullet onto the screen.
        """
        self.screen.blit(self.image, self.rect)
