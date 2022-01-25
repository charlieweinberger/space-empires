import random, sys
sys.path.append('logs')
from ship_data import *
from ships import *
from colony import *
from logger import *

class Game:

    def __init__(self, players, board_len=7, max_turns=100, initial_cp=150, cp_increment=10):

        self.players = {i+1: player for i, player in enumerate(players)}
        
        self.board_len = board_len
        self.max_turns = max_turns
        self.initial_cp = initial_cp
        self.cp_increment = cp_increment

        self.logger = Logger('/workspace/space-empires/logs/logs.txt')
        self.logger.clear_log()

        self.board = {(x, y): [] for x in range(self.board_len) for y in range(self.board_len)}
        self.turn = 1
        self.winner = None
        self.combat_coords = []

        self.set_up_game()

    def get_in_bounds_translations(self, coords):

        if coords == None: return []

        in_bounds_translations = []
        possible_translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]

        for translation in possible_translations:

            new_x, new_y = self.translate(coords, translation)
            if 0 <= new_x <= self.board_len-1 and 0 <= new_y <= self.board_len-1:
                in_bounds_translations.append(translation)
        
        return in_bounds_translations
    
    def cost(self, player_ships):
        total = 0
        for name, num_of_ships in player_ships.items():
            for ship_info in all_ships:
                if name == ship_info['name']:
                    total += num_of_ships * ship_info['cp_cost']
        return total
    
    def set_up_game(self):

        for i, player in self.players.items():
            player.set_player_num(i)

        mid = self.board_len // 2
        ship_coords = {1: (mid, 0),
                       2: (mid, self.board_len-1)}

        self.logger.write('SETTING UP GAME...')

        for i, coords in ship_coords.items():
 
            self.logger.write(f'\n\tPLAYER {i} STARTING AT {coords}')

            home_colony = Colony(i, coords, True)
            self.add_to_board(home_colony, coords)
            self.players[i].home_colony = home_colony

            self.players[i].cp = self.initial_cp
            player_ships = self.players[i].strategy.buy_ships(self.players[i].cp)
            player_ships_cost = self.cost(player_ships)
            
            if player_ships_cost > self.players[i].cp:
                print(f'Player {i} went over budget')
                continue
            
            self.players[i].cp -= player_ships_cost

            for ship_name, num_of_ships in player_ships.items():
                for j in range(num_of_ships):
            
                    ship = ship_objects[ship_name](i, j+1, coords)

                    if ship == None: continue

                    self.add_to_board(ship, coords)
                    self.players[i].ships.append(ship)
                    self.players[i].ship_counter[ship.name] += 1

        self.logger.write('\n')

        self.update_simple_boards()

    def add_to_board(self, obj, coords):
        self.board[coords].append(obj)

    def update_simple_boards(self):
        for player in self.players.values():
            player.strategy.simple_board = {key:[obj.__dict__ for obj in value] for key, value in self.board.items()}
            player.strategy.turn = int(self.turn)

    def get_ships(self, coords):
        return [obj for obj in self.board[coords] if obj.obj_type == 'Ship']

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
        self.logger.write(f'\t\t{ship.ship_id()}: {ship.coords} -> {new_coords}\n')
        self.board[ship.coords].remove(ship)
        ship.coords = new_coords
        self.board[ship.coords].append(ship)

    def remove_ship(self, ship):
        self.board[ship.coords].remove(ship)
        self.players[ship.player_num].ships.remove(ship)
    
    def get_ship_num(self, player, input_ship_name):
        for ship_name, num_of_ship in player.ship_counter.items():
            if ship_name == input_ship_name:
                return num_of_ship + 1

    def hit(self, attacker, defender):

        self.logger.write(f'\n\t\tAttacker: {attacker.ship_id()}\n')
        self.logger.write(f'\t\tDefender: {defender.ship_id()}\n')

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
                self.logger.write(f'\t{player.player_id} HAS NO SHIPS\n\n')
                continue

            self.logger.write(f'\t{player.player_id} MOVING:\n')

            for ship in player.ships:

                if self.there_are_opponent_ships(ship): continue

                current_coords = ship.coords
                in_bounds_translations = self.get_in_bounds_translations(current_coords)
                translation = player.strategy.choose_translation(ship.__dict__, in_bounds_translations)
                new_coords = self.translate(current_coords, translation)

                if new_coords not in self.board.keys():
                    self.logger.write(f'\t\t{ship.ship_id()} tried to make an invalid move: {translation}\n')
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

                self.logger.write('\n\t\tCOMBAT ORDER:\n\n')
                for ship in combat_order:
                    self.logger.write(f'\t\t\t{ship.ship_id()} \n')

                for ship in combat_order:
                
                    if ship.hp <= 0: continue
                
                    player = self.players[ship.player_num]
                    opponent_ships = self.get_opponent_ships(ship, combat_order) 
                    opponent_ships_info = [obj.__dict__ for obj in opponent_ships]
                
                    if len(opponent_ships) == 0: continue
                    
                    target_info = player.strategy.choose_target(ship.__dict__, [ship.__dict__ for ship in combat_order])
                    target = self.obj_from_info(target_info)
                
                    if target not in opponent_ships: continue
                        
                    if self.hit(ship, target):
                                        
                        target.hp -= 1
                
                        self.logger.write(f'\n\t\t{ship.ship_id()} dealt 1 dmg to {target.ship_id()}\n')
                        
                        if target.hp <= 0:
                
                            self.remove_ship(target)
                            self.logger.write(f'\t\t{target.ship_id()} was destroyed\n')
                    
                    self.update_simple_boards()

                combat_order = [ship for ship in combat_order if ship.hp > 0]
                if self.all_same_team(combat_order) or len(combat_order) == 0:
                    coords_to_delete.append(coords)
                    
            self.combat_coords = [coords for coords in self.combat_coords if coords not in coords_to_delete]

        self.logger.write(f'\nEND OF TURN {self.turn} COMBAT PHASE\n')

    def complete_economic_phase(self):

        self.logger.write(f'\nSTART OF TURN {self.turn} ECONOMIC PHASE\n')

        for player in self.players.values():

            self.logger.write(f'\n\t{player.player_id}:\n')

            # income
            self.logger.write(f'\n\t\tINCOME:')
            player.cp += 10
            self.logger.write(f'\n\t\t{player.cp = }\n')

            # maintenance

            self.logger.write(f'\n\t\tMAINTENANCE:')

            player_ships = sorted(player.ships, key=lambda x: x.maint_cost, reverse=True)
            
            total_maint_cost = 0
            for ship in player_ships:
                self.logger.write(f'\n\t\t{ship.ship_id()} maint cost: {ship.maint_cost}')
                total_maint_cost += ship.maint_cost

            self.logger.write(f'\n\t\t{total_maint_cost = }\n')

            if player.cp >= total_maint_cost:
                player.cp -= total_maint_cost

            else:
                while player.cp < total_maint_cost:
                    ship_to_delete = player_ships.pop()
                    total_maint_cost -= ship_to_delete.maint_cost                   
                    self.logger.write(f'\n\t\t{ship_to_delete.ship_id()} HAS BEEN REMOVED')
                    self.remove_ship(ship_to_delete)

            self.logger.write(f'\n\t\tplayer.cp after maintenance: {player.cp} \n')

            # purchase

            self.logger.write(f'\n\t\tPURCHASES:\n')

            wanted_ships = player.strategy.buy_ships(player.cp)
            wanted_ships_cp = 0
            ships_to_add = []

            for wanted_ship_name, num_of_wanted_ship in wanted_ships.items():
                for _ in range(num_of_wanted_ship):
                    wanted_ship_num = self.get_ship_num(player, wanted_ship_name)
                    wanted_ship = ship_objects[wanted_ship_name](player.player_num, wanted_ship_num, player.home_colony.coords)
                    ships_to_add.append(wanted_ship)
                    wanted_ships_cp += wanted_ship.cp_cost

            if player.cp >= wanted_ships_cp:

                for ship in ships_to_add:
                    player.ships.append(ship)
                    player.ship_counter[ship.name] += 1
                    self.add_to_board(ship, player.home_colony.coords)
                    self.logger.write(f'\t\t{player.player_id} BOUGHT A {ship.name}\n')

                player.cp -= wanted_ships_cp


            self.logger.write(f'\n\t\tPLAYER HAS {player.cp} LEFTOVER\n')

        self.logger.write(f'\nEND OF TURN {self.turn} ECONOMIC PHASE\n')

    def run_to_completion(self):

        while self.winner == None and self.turn < self.max_turns:
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.complete_economic_phase()
            self.check_for_winner()
            self.turn += 1
        
        if self.winner == None:
            self.logger.write('\nTIE GAME')
            self.winner = 'Tie'

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