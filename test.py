import sys
from game import *
from player import *
sys.path.append('strategies')
from move_to_opponent_strat import *
from same_move_strat import *
from wait_strat import *

# test number 1
players = [Player(SameMove(move=(0, -1))), Player(SameMove(move=(0, -1)))]
game = Game(players, show_game=False)
game.run_if(lambda x: game.turn <= 3)
old_coords = players[0].ships[0].coords
game.run_if(lambda x: game.turn <= 4)
new_coords = players[0].ships[0].coords

assert old_coords == new_coords

# test number 2
players = [Player(MoveToOpponent()), Player(Wait())]
game = Game(players, show_game=False)
game.run_if(lambda x: game.turn <= 5)
game.complete_movement_phase()

assert game.board[game.combat_coords[0]][0].player_num == 2

# test number 3
# look at game.check_for_winner()