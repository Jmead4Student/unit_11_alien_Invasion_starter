import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal



class Ship:
    """Class to display the ship and update it's location and arsenal.
    """
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal')-> None:
        """Initializes the ship with it's arsenal and sets it's location.

        Args:
            game (AlienInvasion): The main game object.
            arsenal (Arsenal): The bullets the ship can fire.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h)                            
            )
        self.image = pygame.transform.rotate(self.image, -90)
        
        self.rect  = self.image.get_rect()
        self.rect.midleft = self.boundaries.midleft
        self.moving_up = False
        self.moving_down = False
        self.y = float(self.rect.y)
        self.arsenal = arsenal

    def update(self):
        """Updates the ships location and bullet count.
        """   
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Manages the ships vertical ppsition and establishes screen boundaries.
        """
        temp_speed = self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed

        self.rect.y = self.y

    def draw(self):
        """Draws the ship on the screen and gives it arsenal.
        """
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Fires a bullet from the ships arsenal.

        Returns:
            Int: How many bullets have be fired.
        """
        return self.arsenal.fire_bullet()