class Ship:
    
    def __init__(self):
        self.obj_type = 'Ship'
    
    def ship_id(self):
        return f'{self.player_num} {self.name} {self.ship_num}'

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
        self.cp_cost = 6

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
        self.cp_cost = 15

class Cruiser(Ship):

    def __init__(self, player_num, ship_num, initial_coords):

        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = init_coords

        self.name = "Cruiser"
        self.ship_class = "C"
        self.atk = 4
        self.df = 1
        self.hp = 2
        self.cp_cost = 12

class Destroyer(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = init_coords

        self.name = "Destroyer"
        self.ship_class = "D"
        self.atk = 4
        self.df = 0
        self.hp = 1
        self.cp_cost = 9

class Dreadnaught(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):

        self.player_num = player_num
        self.ship_num = ship_num
        self.coords = initial_coords

        self.name = "Dreadnaught"
        self.ship_class = "A"
        self.atk = 6
        self.df = 3
        self.hp = 3
        self.cp_cost = 24