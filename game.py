import random, sys

sys.path.append('logs')
from ships import *
from colony import *
from logger import *

class Game:

    def __init__(self, players, show_game=True, board_size=[7,7]):

        self.players = {i+1: players[i] for i in range(len(players))}
        self.show_game = show_game
        self.board_size = board_size
        self.board_len = self.board_size[0]

        self.logger = Logger('/workspace/space-empires-new/logs/logs.txt')
        self.logger.clear_log()

        self.board = {(x, y): [] for x in range(1, self.board_len + 1) for y in range(1, self.board_len + 1)}
        self.turn = 1
        self.winner = None
        self.combat_coords = []

        self.set_up_game()

    def get_in_bounds_translations(self, coords):

        if coords == None: return []

        all_translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []

        for translation in all_translations:

            new_x, new_y = self.translate(coords, translation)
            if (new_x, new_y) != None and 1 <= new_x <= self.board_len and 1 <= new_y <= self.board_len:
                in_bounds_translations.append(translation)
        
        return in_bounds_translations

    def set_up_game(self):

        # player numbers
        for i, player in self.players.items():
            player.player_num = i

        mid = (self.board_len + 1) // 2
        ship_coords = {1: (mid, 1),
                       2: (mid, self.board_len)}

        for i, coords in ship_coords.items():

            # add ships
            ships = [Scout(i, j + 1, coords) for j in range(3)] + [BattleCruiser(i, j + 1, coords) for j in range(3)]
            self.board[coords]  += ships.copy()
            self.players[i].ships = ships.copy()

            # add home colonies
            home_colony = Colony(i, coords)
            home_colony.is_home_colony = True
            self.board[coords].append(home_colony)
            self.players[i].home_colony = home_colony
        
        self.update_simple_boards()

    def update_simple_boards(self):
        simple_board = {key:[obj.__dict__ for obj in self.board[key]] for key in self.board}
        for player in self.players.values():
            player.strategy.simple_board = simple_board

    def get_ships(self, coords):
        return [obj for obj in self.board[coords] if isinstance(obj, Ship)]

    def get_opponent_ships(self, ship, combat_order):
        return [obj for obj in combat_order if obj.player_num != ship.player_num and obj.hp > 0]

    def all_same_team(self, ship_list):
        return len(set([ship.player_num for ship in ship_list])) == 1

    def there_are_opponent_ships(self, input_ship):
        return any(input_ship.player_num != ship.player_num for ship in self.get_ships(input_ship.coords))

    def translate(self, x, y):
        return (x[0] + y[0], x[1] + y[1])

    def obj_from_info(self, info):
        for obj in self.board[info['coords']]:
            if obj.__dict__ == info:
                return obj

    def update_ship_coords(self, ship, new_coords):
        self.board[ship.coords].remove(ship)
        ship.coords = new_coords
        self.board[ship.coords].append(ship)

    def delete_ship(self, ship):
        self.board[ship.coords].remove(ship)
        self.players[ship.player_num].ships.remove(ship)
    
    def hit(self, attacker, defender):
        if attacker.hp > 0 and defender.hp > 0 and attacker.player_num != defender.player_num:
            role = random.randint(1, 10)
            threshold = attacker.atk - defender.df
            return role <= threshold

    def complete_movement_phase(self):

        self.logger.write(f'\nBEGINNING OF TURN {self.turn} MOVEMENT PHASE\n\n')
        
        for player in self.players.values():

            if len(player.ships) == 0: continue

            for ship in player.ships:

                if self.there_are_opponent_ships(ship): continue

                current_coords = ship.coords
                in_bounds_translations = self.get_in_bounds_translations(current_coords)
                translation = player.choose_translation(ship, in_bounds_translations)
                new_coords = self.translate(current_coords, translation)

                if new_coords not in self.board.keys():
                    self.logger.write(f'\tPlayer {ship.player_num} {ship.name} tried to make an invalid move: {translation}\n')
                    continue

                self.update_ship_coords(ship, new_coords)
                self.update_simple_boards()

                if self.there_are_opponent_ships(ship) and ship.coords not in self.combat_coords:
                    self.combat_coords.append(ship.coords)
                
                self.logger.write(f'\tPlayer {ship.player_num} {ship.name}: {current_coords} -> {ship.coords}\n')
        
        if self.show_game: self.print_board()
        
        self.logger.write(f'\nEND OF TURN {self.turn} MOVEMENT PHASE\n')

    def complete_combat_phase(self):
        
        self.logger.write(f'\nBEGINNING OF TURN {self.turn} COMBAT PHASE\n')

        if self.winner != None: return
        
        if True:
        # while len(self.combat_coords) > 0:

            coords_to_delete = []
            
            for coords in self.combat_coords:

                self.logger.write(f'\n\t Combat at: {coords}\n')

                combat_order = sorted(self.get_ships(coords), key=lambda x: x.ship_class)
                
                for ship in combat_order:
                
                    if ship.hp <= 0: continue
                
                    player = self.players[ship.player_num]
                    opponent_ships = self.get_opponent_ships(ship, combat_order) 
                    opponent_ships_info = [obj.__dict__ for obj in opponent_ships]
                
                    if len(opponent_ships) == 0: continue
                    
                    target_info = player.choose_target(ship.__dict__, combat_order)
                    target = self.obj_from_info(target_info)
                
                    if target not in opponent_ships: continue
                
                    self.logger.write(f'\n\t\tAttacker: Player {ship.player_num} {ship.name}\n')
                    self.logger.write(f'\t\tDefender: Player {target.player_num} {target.name}\n')
                
                    if self.hit(ship, target):
                
                        self.logger.write('\t\tHit!\n')
                        
                        target.hp -= 1
                
                        self.logger.write(f'\n\t\tPlayer {ship.player_num} {ship.name} dealt 1 dmgto Player {target.player_num} {target.name}\n')
                        
                        if target.hp <= 0:
                
                            self.delete_ship(target)
                            self.logger.write(f'\t\tPlayer {target.player_num} {target.name} wasdestroyed\n')
                                            
                    else:
                        self.logger.write('\t\t(Miss)\n')
                    
                    self.update_simple_boards()
                
                combat_order = [ship for ship in combat_order if ship.hp > 0]
                if self.all_same_team(combat_order) or len(combat_order) == 0:
                    coords_to_delete.append(coords)
                            
            self.combat_coords = [coords for coords in self.combat_coords if coords not in coords_to_delete]

        self.logger.write(f'\nEND OF TURN {self.turn} COMBAT PHASE\n')

    def run(self, f = lambda x: x.winner == None):
        while f(self):
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.check_for_winner()
            self.turn += 1

    def check_for_winner(self):

        p1, p2 = list(self.players.values())

        p1_wins = any(ship.coords == p2.home_colony.coords for ship in p1.ships)
        p2_wins = any(ship.coords == p1.home_colony.coords for ship in p2.ships)

        if p1_wins and p2_wins:
            self.logger.write('\nTIE GAME')
            self.winner = 'Tie' 
        elif p1_wins:
            self.logger.write('\nWINNER: PLAYER 1')
            self.winner = 1
        elif p2_wins:
            self.logger.write('\nWINNER: PLAYER 2')
            self.winner = 2

    def print_board(self):
        
        print('')
        for y in range(1, self.board_len + 1):
            
            row_string = ''
            for x in range(1, self.board_len + 1):
                coords = (x, y)

                if self.board[coords] == []:
                    row_string += '[ ]'
                
                elif coords in self.combat_coords:
                    row_string += '[*]'
                
                elif self.board[coords][0].player_num == 1:
                    row_string += '[v]'
                
                elif self.board[coords][0].player_num == 2:
                    row_string += '[^]'
            
            print(row_string)
        print('\n')