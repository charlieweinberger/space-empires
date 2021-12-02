import sys
sys.path.append('strategies')

from game import *
from player import *

from move_to_opponent_strat import * # MoveToOpponent()
from justin  import *
from cayden  import * 
from maia    import * 
from anton   import *
from william import *

winners = {1: 0, 2: 0, 'Tie': 0}
num_iterations = 500

for _ in range(num_iterations):
    
    strategies = [
        JustinStrat(),
        MoveToOpponent()
    ]

    players = [Player(strategy) for strategy in strategies]
    game = Game(players)
    game.run()
    winners[game.winner] += 1

print(winners)
for key, val in winners.items():
    print(f'{key} wins: {100 * val / sum(winners.values())}%')

# works with cayden and maia
# Anton, Justin, William beat me by a little bit