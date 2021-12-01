import sys
sys.path.append('strategies')
from move_to_opponent_strat import * # MoveToOpponent()
from game import *
from player import *

winners = {1: 0, 2: 0, 'Tie': 0}

for _ in range(100):

    strategies = [MoveToOpponent(), MoveToOpponent()]

    players = [Player(strategy) for strategy in strategies]
    game = Game(players)
    game.run()
    winners[game.winner] += 1

print({k:f'{v}%' for k, v in winners.items()})