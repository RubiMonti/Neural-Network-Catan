import sys
import select
import queue
import time
import CreateNN
from table import *
from game import *
from pygame.locals import *


def complete_building_phase(game):
    for i in range(4):
        game.player_in_turn = i
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            return
        game.make_decision(possible_actions_list[int(decision)])
    game.late_building_phase = True    
    for i in range(4):
        game.player_in_turn = 3 - i
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            return
        game.make_decision(possible_actions_list[int(decision)])
    game.building_phase = False

def game_of_catan(red,red_1,red_2,red_16,red_3,red_5,red_7,red_8,red_10,red_11,red_12):
    game = Game(red,red_1,red_2,red_16,red_3,red_5,red_7,red_8,red_10,red_11,red_12)

    complete_building_phase(game)
    while not game.game_finished():
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            continue
        game.make_decision(possible_actions_list[int(decision)])

    return game.players[0].vp + game.players[0].vp_cards
