import random, math

class SameMove:
    def __init__(self, move):
        self.player = None
        self.move = move
        self.simple_board = None

    def choose_translation(self, ship_info, choices):
        return self.move

    def choose_target(self, ship_info, simplified_combat_order):
        for info in simplified_combat_order:
            if info['player_num'] != ship_info['player_num']:
                return info