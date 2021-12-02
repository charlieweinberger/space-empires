import sys
sys.path.append('')
sys.path.append('strategies')
sys.path.append('strategies/comp_2_strategies')

from game import *
from player import *

from move_to_opponent_strat import * # MoveToOpponent()
from justin  import *
from cayden  import * 
from maia    import *
from anton   import *
from william import *

# Me vs Justin : 25-75
# Me vs Cayden : 23-77
# Me vs Maia   : 
# Me vs Anton  : 82-18
# Me vs William: 100-0

# Justin vs Cayden : 0-100
# Justin vs Maia   : 
# Justin vs Anton  : 100-0
# Justin vs William: 100-0

# Cayden vs Maia   : 
# Cayden vs Anton  : 100-0
# Cayden vs William: 0-100

# Maia vs Anton  : 
# Maia vs William: 

# Anton vs William: 100-0

true_player_1 = 'Maia'
true_player_2 = 'Charlie'

winners_1 = {true_player_1: 0, true_player_2: 0, 'Tie': 0}
winners_2 = {true_player_2: 0, true_player_1: 0, 'Tie': 0}

num_iterations = 200

for _ in range(num_iterations//2):

    strategies_1 = [Maia(), Charlie()]
    players_1 = [Player(strategy) for strategy in strategies_1]
    game_1 = Game(players_1)
    game_1.run_to_completion()
    winner_map_1 = {1: true_player_1, 2: true_player_2, 'Tie': 'Tie'}
    winners_1[winner_map_1[game_1.winner]] += 1
    
    strategies_2 = [Charlie(), Maia()]
    players_2 = [Player(strategy) for strategy in strategies_2]
    game_2 = Game(players_2)
    game_2.run_to_completion()
    winner_map_2 = {1: true_player_2, 2: true_player_1, 'Tie': 'Tie'}
    winners_2[winner_map_2[game_2.winner]] += 1

winners_both = {true_player_1: 0, true_player_2: 0, 'Tie': 0}
for key in winners_1.keys():
    print(f'{key} wins: {(winners_1[key] + winners_2[key]) * 100 / num_iterations}')