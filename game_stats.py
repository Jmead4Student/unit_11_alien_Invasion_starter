import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Gamestats():
    """Class to track statistics for the Alien Invasion game. Score, high score, level, and lives.
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        """Initializes the game statistics and hi score.

        Args:
            game (AlienInvasion): The main game object.
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()


    def init_saved_scores(self):
        """Loads the saved hi score or creates a json file to savew to if it doesn't exist.
        """
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()


    def save_scores(self):
        """Saves the high score to a json file.
        """
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent = 4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")


    def reset_stats(self):
        """Resets the game's stats to start a new game.
        """
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1


    def update(self, collisions):
        """Updates the score, hiscore, and max score as needed when collisions happen.

        Args:
            collisions (int): Score gathered when an alien is destroyed.
        """
        self._update_score(collisions)
        self._update_hi_score()
        self._update_max_score()


    def _update_max_score(self):
        """Updates the highest score achieved in the current session.
        """
        if self.score > self.max_score:
            self.max_score = self.score


    def _update_hi_score(self):
        """Updates the hi score if the current score is higher.
        """
        if self.score > self.hi_score:
            self.hi_score = self.score


    def _update_score(self, collisions):
        """Updates the score as aliens are hit with lasers.

        Args:
            collisions (list): Aliens destroyed by lasers.
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points

    
    def update_level(self):
        """Increments the game level by 1.
        """
        self.level += 1

