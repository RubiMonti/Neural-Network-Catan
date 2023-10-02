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
        # game.print_game()
        # pygame.display.update()
    game.late_building_phase = True    
    for i in range(4):
        game.player_in_turn = 3 - i
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            return
        game.make_decision(possible_actions_list[int(decision)])
        # game.print_game()
        # pygame.display.update()
    game.building_phase = False

def game_of_catan(red,red_1,red_2,red_16,red_3,red_5,red_7,red_8,red_10,red_11,red_12):
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    font = pygame.font.Font(pygame.font.get_default_font(),12)
    pygame.display.set_caption("Game of Catan")
    game = Game(screen,font,red,red_1,red_2,red_16,red_3,red_5,red_7,red_8,red_10,red_11,red_12)

    # game.print_game()
    # pygame.display.update()
    complete_building_phase(game)
    print("Le toca al jugador: ", game.player_in_turn)
    while not game.game_finished():
        possible_actions_list = game.players[game.player_in_turn].possible_actions(game)
        decision = game.get_next_action(possible_actions_list, game.player_in_turn)
        if (decision == -1):
            continue
        print("La decisión que se ha tomado es: ", possible_actions_list[int(decision)])
        print("Llevan ", game.trades_made, " tradeos")
        game.make_decision(possible_actions_list[int(decision)])

    for i in range(len(game.players)):
        print("El jugador ", i, " ha acabado con ", game.players[i].vp + game.players[i].vp_cards, " puntos de victoria.")
    return [game.players[0].vp + game.players[0].vp_cards, game.recompensa]

    """
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
        # game.print_game()
        # pygame.display.update()
        # print("Se actualiza el mapa")
    while True:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    """

"""
# TODO: Crear función que cuente el número de parámetros que hacen falta 
# para una red dada su tamaño y sus entradas y salidas
coeficientes = []
for i in range(150000):
    coeficientes +=[i]
red = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_1 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_2 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_3 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_5 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_7 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_8 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_10 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_11 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_12 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
red_16 = CreateNN.CreateNN(coeficientes, [150,80,8],279,1)
game_of_catan(red,red_1,red_2,red_3,red_5,red_7,red_8,red_10,red_11,red_12,red_16)
"""
"""
for i in range(100):
    game_of_catan(0,0,0,0,0,0,0,0,0,0,0,0)
    print("##########\n\tGame ", i, "finished\n##########")
"""