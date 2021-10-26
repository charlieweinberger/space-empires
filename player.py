from ships import *
from colony import *

class Player:
    def __init__(self, strategy):
        
        self.player_number = None
        self.home_colony = None
        self.ships = []
        self.strategy = strategy
        
        self.strategy.player = self

    def get_opponent_player_number(self):
        map_to = {None: None, 1: 2, 2: 1}
        return map_to[self.player_num]

    def choose_translation(self, ship, choices):
        return self.strategy.choose_translation(ship.__dict__, choices)

    def choose_target(self, ship_info, combat_order):
        simplified_combat_order = [ship.__dict__ for ship in combat_order]
        return self.strategy.choose_target(ship_info, simplified_combat_order)