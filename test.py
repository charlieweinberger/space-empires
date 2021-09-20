from game import *
from ships import *
from colony import *
from random_player import *
from custom_player import *

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)
game.complete_movement_phase()
game.complete_movement_phase()
game.complete_movement_phase()
game.complete_combat_phase()