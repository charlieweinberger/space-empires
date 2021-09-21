import random, sys
sys.path.append('logs')
from ships import *
from colony import *
from logger import *

class Game:
    def __init__(self, players, board_size=[7,7]):
        
        self.players = {i+1: players[i] for i in range(len(players))}
        self.board_size = board_size
        self.board_len = self.board_size[0]

        self.logger = Logger('/home/runner/space-empires-new/logs/logs.txt')

        self.board = {(x, y): [] for x in range(1, self.board_len + 1) for y in range(1, self.board_len + 1)}
        self.turn = 1
        self.winner = None
        self.combat_coords = []

        self.start_game()

    def set_player_numbers(self):
        for i, player in self.players.items():
            player.player_num = i

    def get_in_bounds_translations(self, coords):

        if coords == None:
            return []

        all_translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []

        for translation in all_translations:
            
            x, y = coords
            dx, dy = translation
            new_x, new_y = x + dx, x + dy
        
            if (new_x, new_y) != None and 1 <= new_x <= self.board_len and 1 <= new_y <= self.board_len:
                in_bounds_translations.append(translation)
        
        return in_bounds_translations

    def set_ships(self):
        
        mid_x = (self.board_len + 1) // 2
        ship_coords = {1: (mid_x, 1),
                       2: (mid_x, self.board_len)}

        for i in [1, 2]:

            ships = [Scout(i, ship_coords[i]) for _ in range(3)] + [Battlecruiser(i, ship_coords[i]) for _ in range(3)]
            self.board[ship_coords[i]] = ships.copy()
            self.players[i].ships = ships.copy()
            self.players[i].home_colony = HomeColony(i, ship_coords[i])

    def start_game(self):
        
        self.set_player_numbers()
        self.logger.clear_log()
        self.set_ships()

    def get_all_ships_on_space(self, coords):
        return list(filter(lambda x: isinstance(x, Ship), self.board[coords]))
    
    def get_alive_ships(self, ship_list):
        return list(filter(lambda x: x.hp > 0, ship_list))

    def get_opponent_ships(self, ship, combat_order):
        return list(filter(lambda x: x.player_num != ship.player_num, self.get_alive_ships(combat_order)))

    def all_same_team(self, ship_list):
        return len(set([ship.player_num for ship in ship_list])) == 1

    def there_are_opponent_ships(self, input_ship):
        return any(input_ship.player_num != ship.player_num for ship in self.get_all_ships_on_space(input_ship.coords))
    
    def update_ship_coords(self, ship, new_coords):
        self.board[ship.coords].remove(ship)
        ship.coords = new_coords
        self.board[ship.coords].append(ship)

    def delete_ship(self, ship):
        self.board[ship.coords].remove(ship)
        self.players[ship.player_num].ships.remove(ship)
        
    def hit(self, attacker, defender):
        role = attacker.atk - defender.df
        threshold = attacker.atk - defender.df
        return role <= threshold

    def complete_movement_phase(self):

        self.logger.write('\nBEGINNING OF TURN {} MOVEMENT PHASE\n\n'.format(self.turn))
        
        for player in self.players.values():
            for ship in player.ships:

                if self.there_are_opponent_ships(ship):
                    continue

                current_coords = ship.coords
                in_bounds_translations = self.get_in_bounds_translations(current_coords)
                translation = player.choose_translation(self.board, in_bounds_translations, ship)
                new_coords = (current_coords[0] + translation[0], current_coords[1] + translation[1])

                if new_coords not in self.board.keys():
                    self.logger.write('\tPlayer {} {} tried to make an invalid move: {}\n'.format(ship.player_num, ship.name, translation))
                    new_coords = current_coords

                self.update_ship_coords(ship, new_coords)

                if self.there_are_opponent_ships(ship) and ship.coords not in self.combat_coords:
                    self.combat_coords.append(ship.coords)
                
                self.logger.write('\tPlayer {} {}: {} -> {}\n'.format(ship.player_num, ship.name, current_coords, ship.coords))
        
        self.print_board()
        self.logger.write('\nEND OF TURN {} MOVEMENT PHASE\n'.format(self.turn))
    
    def complete_combat_phase(self):
        
        self.logger.write('\nBEGINNING OF TURN {} COMBAT PHASE\n'.format(self.turn))

        if self.winner != None: return
        
        coords_to_delete = []
        
        for coords in self.combat_coords:
            
            self.logger.write('\n\t Combat at: {}\n'.format(coords))

            combat_order = sorted(self.get_all_ships_on_space(coords), key=lambda x: x.cls)
            for ship in self.get_alive_ships(combat_order):
            
                player = self.players[ship.player_num]
                opponent_ships = self.get_opponent_ships(ship, combat_order) 

                if len(opponent_ships) == 0: continue
                
                target = player.choose_target(opponent_ships)
                
                self.logger.write('\n\t\tAttacker: Player {} {}\n'.format(ship.player_num, ship.name))
                self.logger.write('\t\tDefender: Player {} {}\n'.format(target.player_num, target.name))

                if self.hit(ship, target):
                    
                    self.logger.write('\t\tHit!\n')
                    
                    target.hp -= 1
                    
                    self.logger.write('\n\t\tPlayer {} {} dealt 1 dmg to Player {} {}\n'.format(ship.player_num, ship.name, target.player_num, target.name))

                    if target.hp <= 0:
                        self.delete_ship(target)
                        self.logger.write('\t\tPlayer {} {} was destroyed\n'.format(target.player_num, target.name))

                else:
                    self.logger.write('\t\t(Miss)\n')

            if self.all_same_team(self.get_alive_ships(combat_order)):
                coords_to_delete.append(coords)
        
        for coords in coords_to_delete:
            self.combat_coords.remove(coords)

        self.logger.write('\nEND OF TURN {} COMBAT PHASE\n'.format(self.turn))

    def run_to_completion(self):
        while self.winner == None:        
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.winner = self.check_for_winner()
            print(self.winner)
            self.turn += 1

    def check_for_winner(self):

        p1, p2 = list(self.players.values())
        p1_wins = any(ship.coords == p2.home_colony.coords for ship in p1.ships)
        p2_wins = any(ship.coords == p1.home_colony.coords for ship in p2.ships)

        if p1_wins and p2_wins:
            self.logger.write('\nTIE GAME')
            return 'Tie' 
        elif p1_wins:
            self.logger.write('\nWINNER: PLAYER 1')
            return 1
        elif p2_wins:
            self.logger.write('\nWINNER: PLAYER 2')
            return 2
        return None
    
    def print_board(self):
        
        print('')
        for y in range(1, self.board_len + 1):
            
            row_string = ''
            for x in range(1, self.board_len + 1):
                coord = (x, y)

                if self.board[coord] == []:
                    row_string += '[ ]'
                
                elif coord in self.combat_coords:
                    row_string += '[*]'
                
                elif self.board[coord][0].player_num == 1:
                    row_string += '[v]'
                
                elif self.board[coord][0].player_num == 2:
                    row_string += '[^]'
            
            print(row_string)
        print('\n')