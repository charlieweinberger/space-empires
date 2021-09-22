import sys
from game import *
from player import *
sys.path.append('strategies')
from custom_strategy import *

players = [Player(MoveToOpponent()), Player(MoveToOpponent())]
game = Game(players)
game.run_to_completion()