import math

class CustomPlayer():
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

        opponent_player_number = self.get_opponent_player_number()
        opponent = players[opponent_player_number]

        all_distances = []
        for choice in choices:
            
            new_coords = []
            for coord in self.all_ships_coords():
                new_coord = (coord[0] + choice[0], coord[1] + choice[1])
                new_coords.append(new_coord)

            distance = [math.dist(coord, opponent.home_colony.coords) for coord in new_coords]
            all_distances.append(distance)

        min_index = all_distances.index(min(all_distances))        
        return choices[min_index]