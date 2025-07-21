import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien (Sprite):
    """Class for the single aliens in the fleet.

    Args:
        Sprite (pygame.sprite.Sprite): The image of the alien scaled.
    """
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initializes the alien and sets its starting position.

        Args:
            fleet (AlienFleet): The fleet object this alien belongs to.
            x (float): The initial x-coordinate of the alien.
            y (float): The initial y-coordinate of the alien.
        """
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_h, self.settings.alien_w)                            
            )
        
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


    def update(self):
        """Updates the alien's horizontal and vertical position.
        """
        self.x += self.settings.fleet_speed * self.fleet.fleet_x_direction
        self.y += self.settings.fleet_speed * self.fleet.fleet_y_direction
        self.rect.x = self.x
        self.rect.y = self.y


    def check_edges(self):
        """Checks if the alien is at the top or bottom edge of the screen.

        Returns:
            bool: True if the alien is at an edge, False otherwise.
        """
        return (self.rect.bottom >= self.boundaries.bottom or self.rect.top <= self.boundaries.top)


    def draw_alien(self):
        """Draws the alien.
        """
        self.screen.blit(self.image, self.rect)
