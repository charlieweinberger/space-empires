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

    def choose_translation(self, board, choices, ship):
        return self.strategy.choose_translation(board, choices, ship)

    def choose_target(self, opponent_ships):
        return self.strategy.choose_target(opponent_ships)