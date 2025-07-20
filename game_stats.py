class Gamestats():
    """Class to tack statistics for the Alien Invasion game.
    """
    def __init__(self, ships_left) -> None:
        """Initializes the game statistics.

        Args:
            ships_left (int): The starting number of ships.
        """
        self.ships_left = ships_left