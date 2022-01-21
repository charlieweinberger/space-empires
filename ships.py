class Ship:
    
    def __init__(self):
        pass
    
    def ship_id(self):
        return f'PLAYER {self.player_num} {self.name} {self.ship_num}'

class Scout(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.obj_type = 'Ship'
        self.name = 'Scout'
        self.ship_class = 'E'
        self.atk = 3
        self.df = 0
        self.hp = 1
        self.cp_cost = 6
        self.maint_cost = 1

class Destroyer(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.obj_type = 'Ship'
        self.name = 'Destroyer'
        self.ship_class = 'D'
        self.atk = 4
        self.df = 0
        self.hp = 1
        self.cp_cost = 9
        self.maint_cost = 1

class Cruiser(Ship):

    def __init__(self, player_num, ship_num, initial_coords):

        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.obj_type = 'Ship'
        self.name = 'Cruiser'
        self.ship_class = 'C'
        self.atk = 4
        self.df = 1
        self.hp = 2
        self.cp_cost = 12
        self.maint_cost = 2

class BattleCruiser(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.obj_type = 'Ship'
        self.name = 'BattleCruiser'
        self.ship_class = 'B'
        self.atk = 5
        self.df = 1
        self.hp = 2
        self.cp_cost = 15
        self.maint_cost = 2

class Battleship(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):

        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.obj_type = 'Ship'
        self.name = 'Battleship'
        self.ship_class = 'A'
        self.atk = 5
        self.df = 2
        self.hp = 3
        self.cp_cost = 20
        self.maint_cost = 3

class Dreadnaught(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):

        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.obj_type = 'Ship'
        self.name = 'Dreadnaught'
        self.ship_class = 'A'
        self.atk = 6
        self.df = 3
        self.hp = 3
        self.cp_cost = 24
        self.maint_cost = 3