from ships import *
from colony import *

class Player:
    def __init__(self, strategy):
        
        self.player_number = None
        self.home_colony = None
        self.ships = []
        self.strategy = strategy
        self.cp = 0
        self.strategy.player = self

    def get_opponent_player_number(self):
        map_to = {None: None, 1: 2, 2: 1}
        return map_to[self.player_num]