import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """A class to manage the creation and behavior of the alien fleet.
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        """Inizializes the alien fleet.

        Args:
            game (AlienInvasion): The main game object.
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_x_direction = self.settings.fleet_x_direction
        self.fleet_y_direction = self.settings.fleet_y_direction

        self.create_fleet()


    def create_fleet(self):
        """Creates a fleet of aliens at the right of the screen.
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, alien_h, screen_w, screen_h)

        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, screen_h, fleet_w, fleet_h)
        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)


    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """Creates a grid for the aliens to be organized in based on dimensions and offsets.

        Args:
            alien_w (int): Width of an alien.
            alien_h (int): Height of an alien.
            fleet_w (int): Number of columns in the fleet.
            fleet_h (int): Numberv of rows in the fleet.
            x_offset (float): The starting horizontal position of the fleet.
            y_offset (float): The starting vertical position of the fleet.
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)


    def calculate_offsets(self, alien_w, alien_h, screen_w, screen_h, fleet_w, fleet_h):
        """Calculates the starting x and y offset position of the fleet.

        Args:
            alien_w (int): Width of a single alien.
            alien_h (int): Height of a single alien.
            screen_w (int): Width of the screen.
            screen_h (int): Height of the screen.
            fleet_w (int): Number of columns in the fleet.
            fleet_h (int): Number of rows in the fleet.

        Returns:
            tuple[int, int]: The caculated x and y offsets.
        """
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h

        right_half_width = screen_w / 2
        horizontal_margin = (right_half_width - fleet_horizontal_space) / 2

        x_offset = int(right_half_width + horizontal_margin)
        y_offset = int((screen_h - fleet_vertical_space) // 2)
        return x_offset, y_offset


    def calculate_fleet_size(self, alien_w, alien_h, screen_w, screen_h):
        """Calculates how many ships can fit in the fleet.
        
        Args:
            alien_w (int): Width of a single alien.
            alien_h (int): Height of a single alien.
            screen_w (int): Width of the screen.
            screen_h (int): Height of the screen.

        Returns:
            tuple[int, int]: The calculated fleet height and width
        """
        fleet_w = (screen_w // 2) // alien_w
        fleet_h = screen_h // alien_h

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)


    def _create_alien(self, current_x: int, current_y: int):
        """Creates a single alien and adds it to the fleet.

        Args:
            current_x (int): The x coordinate of the alien.
            current_y (int): The y coordinate of the alien.
        """
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)


    def _check_fleet_edges(self):
        """Checks if the fleet has reached the top or bottom edge of the screen.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Shifts the entire fleet left and changes its vertical direction."""
        alien: 'Alien'
        for alien in self.fleet.sprites():
            alien.x -= self.settings.fleet_drop_speed

        self.fleet_y_direction *= -1

    def update_fleet(self):
        """Updates the position of aliens in the fleet.
        """
        self._check_fleet_edges()
        self.fleet.update()


    def draw(self):
        """Draws the aliens in the fleet on the screen.
        """
        alien:'Alien'
        for alien in self.fleet:
            alien.draw_alien()


    def check_collisions(self, other_group):
        """Checks for collisions between the fleet and other groups.

        Args:
            other_group (pygame.sprite.Group): The group to check for collisions against.

        Returns:
            dict: A dictonary of colliding sprites.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    

    def check_fleet_left(self):
        """Checks if any aliens have reached the Left side of the screen.

        Returns:
            bool: True if an alien reached the left edge, False otherwise.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False
    
    def check_destroyed_status(self):
        """Checks if the alien fleet has been destroyed.

        Returns:
            bool: True if the fleet is empty, False otherwise.
        """
        return not self.fleet