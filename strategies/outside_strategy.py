import random, math
from ships import *
from colony import *

class OutsideStrategy:
    def __init__(self):
        self.player = None
    
    def get_ships_by_type(self, type_name):
        return filter(ship.name == type_name, self.player.ships)

    def choose_translation(self, board, choices, ship):
        return (0, -1)
        
    def choose_target(self, opponent_ships):
        random_idx = math.floor(len(opponent_ships) * random.random())
        return opponent_ships[random_idx]