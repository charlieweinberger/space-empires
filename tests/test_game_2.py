import sys
sys.path.append('strategies')
from move_to_opponent_strat import * # MoveToOpponent()
from game import *
from player import *

winners = {1: 0, 2: 0, 'Tie': 0}
num_iterations = 1

for _ in range(num_iterations):

    strategies = [MoveToOpponent(), MoveToOpponent()]

    players = [Player(strategy) for strategy in strategies]
    game = Game(players)
    game.run_to_completion()
    winners[game.winner] += 1

print({k:f'{v*100/num_iterations}%' for k, v in winners.items()})