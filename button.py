import pygame.font

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """A class to handle the game's 'start' button.
    """
    
    def __init__(self, game: 'AlienInvasion', msg) -> None:
        """Initializes the button's attributes.

        Args:
            game (AlienInvasion): The main game object.
            msg (str): The text displayed on the button.
        """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file,
            self.settings.button_font_size)
        self.rect = pygame.Rect(0,0,self.settings.button_w,
            self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)

    
    def _prep_msg (self, msg):
        """Renders the button's message and centers it.

        Args:
            msg (str): The text to render
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    
    def draw(self):
        """Draws the button color and text onto the screen.
        """
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)


    def check_clicked(self, mouse_pos):
        """Checks if the mouse clicks the button.

        Args:
            mouse_pos (tuple): The coordinates of the mouse position. (x, y)

        Returns:
            Bool: True if the click was on the button, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)