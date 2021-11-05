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

        self.logger = Logger('/workspace/space-empires-new/logs/logs.txt')
        self.logger.clear_log()

        self.board = {(x, y): [] for x in range(self.board_len) for y in range(self.board_len)}
        self.turn = 1
        self.winner = None
        self.combat_coords = []

        self.set_up_game()

    def get_in_bounds_translations(self, coords):

        if coords == None: return []

        in_bounds_translations = []

        for translation in [(0,0), (0,1), (0,-1), (1,0), (-1,0)]:

            new_x, new_y = self.translate(coords, translation)
            if 0 <= new_x <= self.board_len-1 and 0 <= new_y <= self.board_len-1:
                in_bounds_translations.append(translation)
        
        return in_bounds_translations

    def set_up_game(self):

        for i, player in self.players.items():
            player.player_num = i

        mid = self.board_len // 2
        ship_coords = {1: (0, mid),
                       2: (self.board_len-1, mid)}

        self.logger.write('SETTING UP GAME...')

        for i, coords in ship_coords.items():

            self.logger.write(f'\nPLAYER {i} STARTING AT {coords}')

            ships = [Scout(i, j + 1, coords) for j in range(3)] + [BattleCruiser(i, j + 1, coords) for j in range(3)]
            self.board[coords]  += ships.copy()
            self.players[i].ships = ships.copy()

            home_colony = Colony(i, coords)
            home_colony.is_home_colony = True
            self.board[coords].append(home_colony)
            self.players[i].home_colony = home_colony
        
        self.logger.write('\n')

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

    def move_ship(self, ship, new_coords):
        self.logger.write(f'\t\tPLAYER {ship.ship_id()}: {ship.coords} -> {new_coords}\n')
        self.board[ship.coords].remove(ship)
        ship.coords = new_coords
        self.board[ship.coords].append(ship)

    def delete_ship(self, ship):
        self.board[ship.coords].remove(ship)
        self.players[ship.player_num].ships.remove(ship)
    
    def hit(self, attacker, defender):

        self.logger.write(f'\n\t\tAttacker: Player {attacker.ship_id()}\n')
        self.logger.write(f'\t\tDefender: Player {defender.ship_id()}\n')

        if attacker.hp > 0 and defender.hp > 0 and attacker.player_num != defender.player_num:
            
            role = random.randint(1, 10)
            threshold = attacker.atk - defender.df
            hit = (role <= threshold)
            
            self.logger.write(f'\t\t{"HIT!" if hit else "(MISS)"}\n')
            return hit

    def complete_movement_phase(self):

        self.logger.write(f'\nBEGINNING OF TURN {self.turn} MOVEMENT PHASE\n\n')
        
        for player in self.players.values():

            if len(player.ships) == 0:
                self.logger.write(f'\tPLAYER {player.player_num} HAS NO SHIPS\n\n')
                continue

            self.logger.write(f'\tPLAYER {player.player_num} MOVING:\n')

            for ship in player.ships:

                if self.there_are_opponent_ships(ship): continue

                current_coords = ship.coords
                in_bounds_translations = self.get_in_bounds_translations(current_coords)
                translation = player.choose_translation(ship, in_bounds_translations)
                new_coords = self.translate(current_coords, translation)

                if new_coords not in self.board.keys():
                    self.logger.write(f'\t\tPlayer {ship.ship_id()} tried to make an invalid move: {translation}\n')
                    continue

                self.move_ship(ship, new_coords)
                self.update_simple_boards()

                if self.there_are_opponent_ships(ship) and ship.coords not in self.combat_coords:
                    self.combat_coords.append(ship.coords)
            
            self.logger.write('\n')

        self.logger.write(f'END OF TURN {self.turn} MOVEMENT PHASE\n')

    def complete_combat_phase(self):
        
        self.logger.write(f'\nBEGINNING OF TURN {self.turn} COMBAT PHASE\n')

        if self.winner != None: return
        
        coords_to_delete = []

        for coords in self.combat_coords:
            
            combat_order = sorted(self.get_ships(coords), key=lambda x: x.ship_class)
            
            while not self.all_same_team(combat_order) and len(combat_order) > 0:

                self.logger.write(f'\n\tCOMBAT AT {coords}:\n')

                for ship in combat_order:
                
                    if ship.hp <= 0: continue
                
                    player = self.players[ship.player_num]
                    opponent_ships = self.get_opponent_ships(ship, combat_order) 
                    opponent_ships_info = [obj.__dict__ for obj in opponent_ships]
                
                    if len(opponent_ships) == 0: continue
                    
                    target_info = player.choose_target(ship.__dict__, [ship.__dict__ for ship in combat_order])
                    target = self.obj_from_info(target_info)
                
                    if target not in opponent_ships: continue
                
                    if self.hit(ship, target):
                                        
                        target.hp -= 1
                
                        self.logger.write(f'\n\t\tPlayer {ship.ship_id()} dealt 1 dmg to Player {target.ship_id()}\n')
                        
                        if target.hp <= 0:
                
                            self.delete_ship(target)
                            self.logger.write(f'\t\tPlayer {target.ship_id()} was destroyed\n')
                    
                    self.update_simple_boards()

                combat_order = [ship for ship in combat_order if ship.hp > 0]
                if self.all_same_team(combat_order) or len(combat_order) == 0:
                    coords_to_delete.append(coords)
                    
            self.combat_coords = [coords for coords in self.combat_coords if coords not in coords_to_delete]

        self.logger.write(f'\nEND OF TURN {self.turn} COMBAT PHASE\n')

    def run(self, f = lambda x: True):
        while self.winner == None and f(self):
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