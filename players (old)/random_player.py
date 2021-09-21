import random
import math

class RandomPlayer():
    
    def __init__(self):
        self.player_num = None
        self.ships = []
        self.home_colony = None

    def get_opponent_player_number(self):
        map_to = {None: None, 1: 2, 2: 1}
        return map_to[self.player_num]

    def all_ships_coords(self):
        return [ship.coords for ship in self.ships]

    def choose_translation(self, players, choices):
        random_idx = math.floor(len(choices) * random.random())
        return choices[random_idx]