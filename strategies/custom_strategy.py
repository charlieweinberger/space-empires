import random, math
from ships import *
from colony import *

class MoveToOpponent:
    def __init__(self):
        self.player = None

    def min_distance_translation(self, choices, ship, target_coords):

        if choices != []:
            
            min_choice = choices[0]
            new_point = (ship.coords[0] + min_choice[0], ship.coords[1] + min_choice[1])
            min_distance = math.dist(new_point, target_coords)

            for choice in choices:
                current_coords = (ship.coords[0] + choice[0], ship.coords[1] + choice[1])
                current_distance = math.dist(current_coords, target_coords)

                if current_distance < min_distance:
                    min_distance = current_distance
                    min_choice = choice

            return min_choice

    def choose_translation(self, players, board, choices, ship):
        home_colony_coords = players[self.player.get_opponent_player_number()].home_colony.coords
        return self.min_distance_translation(choices, ship, home_colony_coords)
        
    def choose_target(self, opponent_ships):
        random_idx = math.floor(len(opponent_ships) * random.random())
        return opponent_ships[random_idx]