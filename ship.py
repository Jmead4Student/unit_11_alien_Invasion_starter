"""
Alien Invasion
John Mead
This module handles the ship class and all it's functions.
7-26-25
"""

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
        self._center_ship()
        self.moving_up = False
        self.moving_down = False
        self.arsenal = arsenal

        self.powerup_active = False
        self.powerup_timer = 0


    def _center_ship(self):
        self.rect.midleft = self.boundaries.midleft
        self.y = float(self.rect.y)


    def update(self):
        """Updates the ships location and bullet count.
        """   
        self._update_ship_movement()
        self.arsenal.update_arsenal()
        self._check_powerup_status()


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
    

    def check_collisions(self, other_group):
        """Checks for collisions with the ship and other sprites. Recenters ship if True.

        Args:
            other_group (pygame.sprite.Group): Any sprite group the ship could collide with.

        Returns:
            Bool: True if a collision is detected,False otherwise.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
    

    def activate_powerup(self):
        """Activates powerup to increase bullet amount.
        """
        self.powerup_active = True
        self.settings.bullet_amount = 10  
        self.powerup_timer = pygame.time.get_ticks()


    def _check_powerup_status(self):
        """Checks if power-up is still active.
        """
        if self.powerup_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.powerup_timer > self.settings.powerup_duration:
                self.powerup_active = False
                self.settings.bullet_amount = self.settings.base_bullet_amount