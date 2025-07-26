"""
Alien Invasion
John Mead
This module handles the arsenal class and all it's functions.
7-26-25
"""

import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """Manages the ships arsewnal of bullets.
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        """Initializes the ships loadout.

        Args:
            game (AlienInvasion): The main game object.
        """
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()


    def update_arsenal(self):
        """Updates the bullets positions and removes them if the cross the right boundary.
        """
        self.arsenal.update()
        self._remove_bullets_offscreen()


    def _remove_bullets_offscreen(self):
        """Establishes the boundary for the bullets and removes them.
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.left >= self.game.screen.get_rect().right:
                self.arsenal.remove(bullet)


    def draw(self):
        """Draw the bullets on the screen.
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()


    def fire_bullet(self):
        """Creates bullets and adds them to the arsenal to track.

        Returns:
            bool: True if a bullet is fired, False if not.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False