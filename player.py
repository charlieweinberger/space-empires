from ships import *
from colony import *
from ship_data import *

class Player:
    def __init__(self, strategy):
        
        self.player_num = None
        self.player_id = None
        self.home_colony = None
        
        self.strategy = strategy
        self.strategy.player = self

        self.ship_counter = {ship_name:0 for ship_name in ship_objects}
        self.ships = []
        self.cp = 0

    def set_player_num(self, i):
        self.player_num = i
        self.player_id = f'PLAYER {i}'

    def get_opponent_player_number(self):
        map_to = {None: None, 1: 2, 2: 1}
        return map_to[self.player_num]