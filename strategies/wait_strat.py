import random, math

class Wait:
    def __init__(self):
        self.player = None
        self.turn = 0
        self.simple_board = None

    def choose_translation(self, ship_info, choices):
        return (0, -1) if ship_info['coords'] == (4, 7) else (0, 0)
        
    def choose_target(self, ship_info, simplified_combat_order):
        for info in simplified_combat_order:
            if info['player_num'] != ship_info['player_num']:
                return info