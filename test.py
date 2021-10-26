
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

move = (0, 1)
strategies = [
    Custom(),
    SameMove(move)
]

players = [Player(strategy) for strategy in strategies]
game = Game(players, show_game=False)
game.run()
print(game.winner)

# works with everyone