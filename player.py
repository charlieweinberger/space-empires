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

    def get_ships_by_type(self, type_name):
        return list(filter(lambda x: x.name == type_name, self.ships))

    def choose_translation(self, players, board, choices, ship):
        return self.strategy.choose_translation(players, board, choices, ship)

    def choose_target(self, opponent_ships):
        return self.strategy.choose_target(opponent_ships)