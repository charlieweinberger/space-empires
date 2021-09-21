import sys
from game import *
from player import *
sys.path.append('strategies')
from outside_strategy import *

players = [Player(OutsideStrategy()), Player(OutsideStrategy())]
game = Game(players)
game.run_to_completion()