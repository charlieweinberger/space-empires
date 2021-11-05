class Ship:
    def __init__(self):
        pass

class Scout(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.coords = initial_coords

        self.ship_num = ship_num
        self.obj_type = 'Ship'
        self.name = 'Scout'
        
        self.ship_class = 'E'
        self.atk = 3
        self.df = 0
        self.hp = 1
    
    def ship_id(self):
        return f'{self.player_num} {self.name} {self.ship_num}'

class BattleCruiser(Ship):
    
    def __init__(self, player_num, ship_num, initial_coords):
        
        self.player_num = player_num
        self.coords = initial_coords
        
        self.ship_num = ship_num
        self.obj_type = 'Ship'
        self.name = 'BattleCruiser'
        
        self.ship_class = 'B'
        self.atk = 5
        self.df = 1
        self.hp = 2
    
    def ship_id(self):
        return f'{self.player_num} {self.name} {self.ship_num}'