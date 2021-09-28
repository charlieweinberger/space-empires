import random, math

class SameMove:
    def __init__(self, move):
        self.player = None
        self.move = move

    def choose_translation(self, players, board, choices, ship):
        return self.move
        
    def choose_target(self, opponent_ships):
        random_idx = math.floor(len(opponent_ships) * random.random())
        return opponent_ships[random_idx]