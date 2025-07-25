"""
Alien Invasion
John Mead
This program is a recreated version of space invaders with the orientation flipped.
7-20-25
"""

import sys
import pygame
import random
from settings import Settings
from game_stats import Gamestats
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from time import sleep 
from button import Button
from hud import HUD
from powerup import PowerUp


class AlienInvasion:
    """Game loop class that manages games assets, resources, and logic.
    """
    def __init__(self):
        """Initializes the game and manages all of the game resources.
        """
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)
        
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
            )
        
        self.game_stats = Gamestats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.powerups = pygame.sprite.Group()

        self.play_button = Button(self, 'Play')
        self.game_active = False
    

    def run_game(self):
        """Starts the main game loop.
        """
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.powerups.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)


    def _check_collisions(self):
        """Checks for collisions with aliens or powerups, plays a sound, and resets the level if the fleet is destroyed.
        """
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
        
        if self.alien_fleet.check_fleet_left():
            self._check_game_status()

        self._check_powerup_collisions()

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    if random.random() < 0.2:
                        self._create_powerup(alien.rect.center)
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            self.game_stats.update_level()
            self.HUD._update_level()


    def _create_powerup(self, center):
        """Create a power-up at the given location.
        """
        new_powerup = PowerUp(self, center)
        self.powerups.add(new_powerup)


    def _check_powerup_collisions(self):
        """Check for collisions between the ship and power-ups.
        """
        collided_powerup = pygame.sprite.spritecollideany(self.ship, self.powerups)
        if collided_powerup:
            self.ship.activate_powerup()
            collided_powerup.kill()


    def _check_game_status(self):
        """Resets the game if a ship is lost and ends the game on a game over.
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False


    def _reset_level(self):
        """Resets the game by clearing bullets and creating a new alien fleet.
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
        self.powerups.empty()


    def restart_game(self):
        """Resets the game stats, mouse vision, and recenters the ship.
        """
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)


    def _update_screen(self):
        """Updates the surfaces displayed.
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.powerups.draw(self.screen)
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()


    def _check_events(self):
        """Checks for keypresses and exit sequences.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()


    def _check_button_clicked(self):
        """Confirms if the "Play" button is clicked.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()


    def _check_keyup_events(self, event):
        """Checks for the up or down key being released.

        Args:
            event (key): Up key or Down key.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _check_keydown_events(self, event):
        """Checks for the Up or Down key being released for movement. The Q key to quit the program.
        The space key to fire the laser and play a sound. Or the player closing the window to quit.

        Args:
            event (key): The Up key, Down key, Q key, or Space key.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
