import sys
sys.path.append('')
sys.path.append('strategies')
sys.path.append('strategies/comp_strategies')
from game import *
from player import *
from move_to_opponent_strat import * # MoveToOpponent()
from justin import JustinStrat
from cayden import CaydenStrat
from anton import AntonStrat
from william import WilliamStrat

# Cayden  v William: 91-9
# Cayden  v Justin : 68-32
# Cayden  v Anton  : 67-33
# Cayden  v Charlie: 83-17

# William v Justin : 37-60
# William v Anton  : 27-73
# William v Charlie: 

# Justin  v Anton  :
# Justin  v Charlie:

# Anton   v Charlie:

true_player_1 = 'William'
true_player_2 = 'Justin'

winners_1 = {true_player_1: 0, true_player_2: 0, 'Tie': 0}
winners_2 = {true_player_2: 0, true_player_1: 0, 'Tie': 0}

num_iterations = 100

for _ in range(num_iterations//2):

    strategies_1 = [WilliamStrat(), JustinStrat()]
    strategies_2 = [JustinStrat(), WilliamStrat()]

    players_1 = [Player(strategy) for strategy in strategies_1]
    game_1 = Game(players_1)
    game_1.run_to_completion()
    winner_map_1 = {1: true_player_1, 2: true_player_2, 'Tie': 'Tie'}
    winners_1[winner_map_1[game_1.winner]] += 1
    
    players_2 = [Player(strategy) for strategy in strategies_2]
    game_2 = Game(players_2)
    game_2.run_to_completion()
    winner_map_2 = {1: true_player_2, 2: true_player_1, 'Tie': 'Tie'}
    winners_2[winner_map_2[game_2.winner]] += 1

for key in winners_1.keys():
    print(f'{key} wins: {(winners_1[key] + winners_2[key]) * 100 / num_iterations}')