import pygame
import sys
import socket
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
        game.print_game()
        pygame.display.update()
    game.late_building_phase = True    
    for i in range(4):
        game.player_in_turn = 3 - i
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            return
        game.make_decision(possible_actions_list[int(decision)])
        game.print_game()
        pygame.display.update()
    game.building_phase = False

def game_of_catan(red,red_1,red_2,red_16,red_3,red_5,red_7,red_8,red_10,red_11,red_12):
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    font = pygame.font.Font(pygame.font.get_default_font(),12)
    pygame.display.set_caption("Game of Catan")
    game = Game(screen,font,red,red_1,red_2,red_16,red_3,red_5,red_7,red_8,red_10,red_11,red_12)

    game.print_game()
    pygame.display.update()
    complete_building_phase(game)
    while not game.game_finished():
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            continue
        game.make_decision(possible_actions_list[int(decision)])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True
                    while paused:
                        #time.sleep(0.05)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p or event.key == pygame.K_c:
                                    paused = False
        time.sleep(0.05)
        game.print_game()
        pygame.display.update()

    for i in range(len(game.players)):
    while True:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    if (len(sys.argv) == 2):
        args_file = sys.argv[1]
    elif (len(sys.argv) > 2):
        print("Bad input. Usage: python3 catan.py [File with Neural Weights]")
    else:
        args_file = "TrainedNetArguments.txt"
    arguments = []
    try:
        with open(args_file) as file:
            for line in file:
                arguments += [float(line)]
        print(arguments)
    except:
        print("Algo ha salido mal")
        sys.exit(-1)
    red = CreateNN.CreateNN(arguments, [4,10],279,17)
    game_of_catan(red,0,0,0,0,0,0,0,0,0,0)
