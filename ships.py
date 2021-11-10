class Ship:
    
    def __init__(self):
        self.obj_type = 'Ship'
    
    def ship_id(self):
        return f'{self.player_num} {self.name} {self.ship_num}'

'''

{
    'Battleship': {'cp_cost': 20, 'attack': 5, 'defense': 2},
    'Battlecruiser': {'cp_cost': 15, 'attack': 5, 'defense': 1},
    'Cruiser': {'cp_cost': 12, 'attack': 4, 'defense': 1},
    'Destroyer': {'cp_cost': 9, 'attack': 4, 'defense': 0},
    'Dreadnaught': {'cp_cost': 24, 'attack': 6, 'defense': 3},
    'Scout': {'cp_cost': 6, 'attack': 3, 'defense': 0},
}

'''

class Scout(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.name = 'Scout'
        self.ship_class = 'E'
        self.atk = 3
        self.df = 0
        self.hp = 1

class BattleCruiser(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.name = 'BattleCruiser'
        self.ship_class = 'B'
        self.atk = 5
        self.df = 1
        self.hp = 2