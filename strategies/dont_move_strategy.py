import random, math
from ships import *
from colony import *

class DontMove:
    def __init__(self):
        self.player = None

    def choose_translation(self, board, choices, ship):
        return (0, 0)
        
    def choose_target(self, opponent_ships):
        random_idx = math.floor(len(opponent_ships) * random.random())
        return opponent_ships[random_idx]