import sys
sys.path.append('strategies')
sys.path.append('strategies/comp_strategies')

from game import *
from player import *

from move_to_opponent_strat import * # MoveToOpponent()
from justin_comp  import *
from cayden_comp  import * 
from maia_comp    import * 
from anton_comp   import *
from william_comp import *

# Me vs Justin : 25-75
# Me vs Cayden : 23-77
# Me vs Maia   : 52-48
# Me vs Anton  : 37-63
# Me vs William: 35-65

# Justin vs Cayden : 0-0-100
# Justin vs Maia   : 71-29
# Justin vs Anton  : 62-38
# Justin vs William: 64-36

# Cayden vs Maia   : 80-20
# Cayden vs Anton  : 69-31
# Cayden vs William: 81-19

# Maia vs Anton  : 30-70
# Maia vs William: 35-65

# Anton vs William: 64-36

true_player_1 = 'Maia'
true_player_2 = 'William'

winners_1 = {true_player_1: 0, true_player_2: 0, 'Tie': 0}
winners_2 = {true_player_2: 0, true_player_1: 0, 'Tie': 0}

for _ in range(50):

    players_1 = [Player(MaiaCompStrat()), Player(WilliamCompStrat())]
    game_1 = Game(players_1)
    game_1.run(lambda x: x.turn < 100)
    winner_map_1 = {1: true_player_1, 2: true_player_2, 'Tie': 'Tie', None: 'Tie'}
    winners_1[winner_map_1[game_1.winner]] += 1
    
    players_2 = [Player(WilliamCompStrat()), Player(MaiaCompStrat())]
    game_2 = Game(players_2)
    game_2.run(lambda x: x.turn < 100)
    winner_map_2 = {1: true_player_2, 2: true_player_1, 'Tie': 'Tie', None: 'Tie'}
    winners_2[winner_map_2[game_2.winner]] += 1

winners_both = {true_player_1: 0, true_player_2: 0, 'Tie': 0}
for key in winners_1.keys():
    print(f'{key} wins: {winners_1[key] + winners_2[key]}%')