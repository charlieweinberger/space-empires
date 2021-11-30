import sys
sys.path.append('strategies')
from move_to_opponent_strat import * # MoveToOpponent()
from game import *
from player import *

strategies = [MoveToOpponent(), MoveToOpponent()]

players = [Player(strategy) for strategy in strategies]
game = Game(players)
game.run()
print(game.winner)