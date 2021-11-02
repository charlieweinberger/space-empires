import sys
from game import *
from player import *

sys.path.append('strategies')
from move_to_opponent_strat import * # MoveToOpponent()
from same_move_strat import * # SameMove(move)
from wait_strat import * # Wait()

from justin  import * # MoveToClosestCol()
from cayden  import * # MoveToEnemyHomeColony()
from maia    import * # StraightToEnemyColony()
from anton   import * # CustomStrategy()
from william import * # Custom(), MoveOffBoard(), MoveOnce()

winners = {1: 0, 2: 0, 'Tie': 0}
num_iterations = 500

for _ in range(num_iterations):
    
    move = (1, 0)
    strategies = [
        MoveToOpponent(),
        MoveToOpponent()
    ]

    players = [Player(strategy) for strategy in strategies]
    game = Game(players, show_game=False)
    game.run()
    winners[game.winner] += 1

print({k:f'{100*v/num_iterations}%' for k, v in winners.items()})