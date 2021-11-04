import sys
sys.path.append('strategies')

from game                   import *
from player                 import *
from move_to_opponent_strat import * # MoveToOpponent()
from justin                 import * # MoveToClosestCol()
from cayden                 import * # MoveToEnemyHomeColony()
from maia                   import * # StraightToEnemyColony()
from anton                  import * # CustomStrategy()
from william                import * # Custom(), MoveOffBoard(), MoveOnce()

winners = {1: 0, 2: 0, 'Tie': 0}
num_iterations = 1

for _ in range(num_iterations):
    
    strategies = [
        MoveToOpponent(),
        MoveToOpponent()
    ]

    players = [Player(strategy) for strategy in strategies]
    game = Game(players)
    game.run()
    winners[game.winner] += 1

print(winners)
for key, val in winners.items():
    print(f'{key} wins: {100 * val / sum(winners.values())}%')