class Colony():
    
    def __init__(self, player_num, coords, is_home_colony=False):
        self.player_num = player_num
        self.coords = coords
        self.is_home_colony = is_home_colony
        self.obj_type = 'Colony'