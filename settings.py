"""
Alien Invasion
John Mead
This module handles the settings class and all it's functions.
7-26-25
"""

from pathlib import Path

class Settings:
    """A class to store all settings for game and assets. 
    """
    def __init__(self):
        """Initializes static game settings like asset paths, screen size, asset sizes and colors.
        """
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 40
        self.ship_h = 60
        
        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'        
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 40
        self.alien_h = 40
        
        self.fleet_x_direction = 0
        self.fleet_y_direction = 1

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 135, 50)
        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

        self.powerup_file = Path.cwd() / 'Assets' / 'images' / 'powerup.png'
        #https://opengameart.org/content/powerups Author: rrcaseyr
        self.powerup_w = 25
        self.powerup_h = 25
        self.powerup_duration = 5000


    def initialize_dynamic_settings(self):
        """Initializes settings that get modified by difficulty or get reset when a new game starts.
        """
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_speed = 7
        self.bullet_amount = 5
        self.bullet_w = 25
        self.bullet_h = 80

        self.fleet_speed = 2
        self.fleet_drop_speed = 40
        self.alien_points = 50

        self.powerup_speed = 3
        self.base_bullet_amount = 5
        self.bullet_amount = self.base_bullet_amount
  
        
    def increase_difficulty(self):
        """Increases the speed of assets to increase difficulty 
        """
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale