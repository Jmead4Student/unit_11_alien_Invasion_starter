import sys
import pygame
from settings import Settings
from game_stats import Gamestats
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from time import sleep


class AlienInvasion:
    """Game loop class that manages games assets and logic.
    """
    def __init__(self):
        
        pygame.init()
        self.settings = Settings()
        self.game_stats = Gamestats(self.settings.starting_ship_count)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
            )

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
        self.game_active = True
    

    def run_game(self):

        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)


    def _check_collisions(self):
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
        
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()


    def _check_game_status(self):

        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False


    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()


    def _update_screen(self):
        """Updates the surfaces displayed.
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        pygame.display.flip()


    def _check_events(self):
        """Checks for keypresses and exit sequences.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


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
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
