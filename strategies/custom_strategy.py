import random, math
from ships import *
from colony import *

class CustomStrategy:
    def __init__(self):
        self.player = None
    
    def get_ships_by_type(self, type_name):
        return filter(ship.name == type_name, self.player.ships)

    def find_home_colonies(self, board):
        board_len = math.sqrt(len(board))
        coords = []
        for y in range(board_len):
            for x in range(board_len):
                for thing in board[(x, y)]:
                    if isinstance(thing, HomeColony) and thing.player_num != self.player.player_num:
                        coords.append((x, y))
        return coords

    def find_min_choice(self, choices, coord):
        
        min_choice = choices[0]
        min_distance = math.dist(min_choice, coord)

        for choice in choices:
            if math.dist(choice, coord) < min_distance:
                min_choice = choice
                min_distance = math.dist(choice, coord)
        
        return min_choice

    def min_distance_translation(self, choices, ship, target_coords):
        
        if choices != []:
            
            min_choice = choices[0]
            min_distance = math.dist((ship.coords[0] + min_choice[0], ship.coords[1] + min_choice[1]), target_coords)
            
            for choice in choices:
                
                current_coords = (ship.coords[0] + choice[0], ship.coords[1] + choice[1])
                current_distance = math.dist(current_coords, target_coords)

                if current_distance < min_distance:
                    min_distance = current_distance
                    min_choice = choice

            return min_choice

    def choose_translation(self, board, choices, ship):
        target_coords = self.find_min_choice(self.find_home_colonies(board), ship.coords)
        return self.min_distance_translation(choices, ship, target_coords)
        
    def choose_target(self, opponent_ships):
        random_idx = math.floor(len(opponent_ships) * random.random())
        return opponent_ships[random_idx]