import random, math

class Wait:
    def __init__(self):
        self.player = None
        self.turn = 0

    def choose_translation(self, players, board, choices, ship):
        board_len = len(board)
        mid_x = (board_len + 1) // 2
        if ship.coords == (mid_x, board_len):
            return (0, -1)
        return (0, 0)
        
    def choose_target(self, opponent_ships):
        random_idx = math.floor(len(opponent_ships) * random.random())
        return opponent_ships[random_idx]