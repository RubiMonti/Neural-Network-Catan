import random
import pygame
import math
import utils
from constants import *
from NN import *
from table import *
from pygame.locals import *

class Building:
    def __init__(self, building, player):
        self.building = building
        self.player = player

class Edge:
    def __init__(self, coords, orientation, adjacents):
        self.x = coords[0]
        self.y = coords[1]
        self.orientation = orientation
        self.adjacents = adjacents
        self.road = -1
    
    def add_road(self, player):
        self.road = player

class Corner:
    def __init__(self, coords, adjacents, adjacents_edges, adjacents_tiles, port):
        self.x = coords[0]
        self.y = coords[1]
        self.adjacents = adjacents
        self.adjacents_edges = adjacents_edges
        self.adjacents_tiles = adjacents_tiles
        self.building = Building(-1,-1)
        self.port = port
    
    def add_settlement(self, player):
        self.building = Building(SETTLEMENT,player)
        return self.port
    
    def upgrade_settlement(self):
        self.building.building = CITY

class Player:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.roads_left = 13
        self.settlements_left = 5
        self.cities_left = 4    
        self.lumber = 0
        self.wool = 0
        self.brick = 0
        self.grain = 0
        self.ore = 0
        self.resource_cards = 0
        self.vp = 0
        self.knights = 0
        self.vp_cards = 0
        self.road_building = 0
        self.year_of_plenty = 0
        self.monopoly = 0
        self.active_knights = 0
        self.longest_path = 0
        self.ports = [False,False,False,False,False,False]
        self.knight_bonus = False
        self.road_bonus = False

    def possible_actions(self, game):
        actions = []
        if game.building_phase:
            for i in range(54):
                if game.settlement_is_buildable(game.player_in_turn, i):
                    for road in game.corners[i].adjacents_edges:
                        actions += [(PLACE_SETTLEMENT_THEN_ROAD,i,road)]
        else:
            actions += [(SKIP_TURN)]
            if (self.brick > 0 and self.lumber > 0 and self.roads_left > 0):
                for i in range(72):
                    if game.road_is_buildable(game.player_in_turn, i):
                        actions += [(PLACE_ROAD,i)]
            if (self.wool > 0 and self.grain > 0 and self.brick > 0 and self.lumber > 0 and self.settlements_left > 0):
                for i in range(54):
                    if game.settlement_is_buildable(game.player_in_turn, i):
                        actions += [(PLACE_SETTLEMENT,i)]
            if (self.ore > 2 and self.grain > 1 and self.cities_left > 0):
                for i in range(54):
                    if (game.corners[i].building != 0 and game.corners[i].building.player == game.player_in_turn and game.corners[i].building.building == SETTLEMENT):
                        actions += [(PLACE_CITY,i)]
            if (self.ore > 0 and self.grain > 0 and self.wool > 0 and len(game.development_cards_left) > 0):
                actions += [(BUY_RESOURCE_CARD)]
            if (self.knights > 0):
                actions += [(PLAY_KNIGHT)]
            if (self.road_building > 0 and self.roads_left > 1):
                for i in range(72):
                    if game.road_is_buildable(game.player_in_turn, i):
                        actions += [(PLAY_ROADS)]
                        break
            if (self.monopoly > 0):
                for i in [FOREST, HILLS, PASTURE, FIELDS, MOUNTAINS]:
                    actions += [(PLAY_MONOPOLY, i)]
            all_resources = [FOREST, HILLS, PASTURE, FIELDS, MOUNTAINS]
            if (self.year_of_plenty > 0):
                for i in range(len(all_resources)):
                    for j in range(i,len(all_resources)):
                        actions += [(PLAY_YEAR_OF_PLENTY, all_resources[i], all_resources[j])]
            for i in all_resources:
                count = 4
                if self.ports[i] == True:
                    count = 2
                elif self.ports[0] == True:
                    count = 3
                if i == FOREST:
                    maritime_available = self.lumber >= count
                    domestic_available_1 = self.lumber >= 1
                    domestic_available_2 = self.lumber >= 2 and count > 2
                    domestic_available_3 = self.lumber >= 3 and count > 3
                elif i == MOUNTAINS:
                    maritime_available = self.ore >= count
                    domestic_available_1 = self.ore >= 1
                    domestic_available_2 = self.ore >= 2 and count > 2
                    domestic_available_3 = self.ore >= 3 and count > 3
                elif i == HILLS:
                    maritime_available = self.brick >= count
                    domestic_available_1 = self.brick >= 1
                    domestic_available_2 = self.brick >= 2 and count > 2
                    domestic_available_3 = self.brick >= 3 and count > 3
                elif i == PASTURE:
                    maritime_available = self.wool >= count
                    domestic_available_1 = self.wool >= 1
                    domestic_available_2 = self.wool >= 2 and count > 2
                    domestic_available_3 = self.wool >= 3 and count > 3
                else:
                    maritime_available = self.grain >= count
                    domestic_available_1 = self.grain >= 1
                    domestic_available_2 = self.grain >= 2 and count > 2
                    domestic_available_3 = self.grain >= 3 and count > 3
                if maritime_available:
                    for j in [res for res in all_resources if res != i]:
                        actions += [(MARITIME_TRADE, i, j)]
                if domestic_available_1:
                    for j in [res for res in all_resources if res != i]:
                        actions += [(DOMESTIC_TRADE, i, 1, j, 1)]
                if domestic_available_2:
                    for j in [res for res in all_resources if res != i]:
                        actions += [(DOMESTIC_TRADE, i, 2, j, 2)]
                if domestic_available_3:
                    for j in [res for res in all_resources if res != i]:
                        actions += [(DOMESTIC_TRADE, i, 3, j, 3)]

        return actions
    
    def able_to_trade(self,element,ammount):
        return ((element == FOREST and self.lumber > ammount) or
                (element == HILLS and self.brick > ammount) or
                (element == PASTURE and self.wool > ammount) or
                (element == FIELDS and self.grain > ammount) or
                (element == MOUNTAINS and self.ore > ammount))

class Game:
    def __init__(self,red):
        self.red = red
        self.recompensa = 0
        self.decision_failed = False
        self.corners = []
        self.edges = []
        for i in range(54):
            self.corners += [Corner(CORNERS_COORDS[i],CORNERS_ADJACENTS[i],CORNERS_ADJACENTS_EDGES[i],CORNERS_ADJACENTS_TILES[i],CORNERS_PORTS[i])]
        for i in range(72):
            self.edges += [Edge(EDGES_COORDS[i], EDGES_ORIENTATIONS[i], EDGES_ADJACENTS[i])]
        self.table = Table(self.corners,self.edges)
        self.players = []
        self.turn = 0
        self.player_in_turn = 0
        self.trades_made = 0
        self.development_cards_left = [KNIGHT]*14 + [MONOPOLY]*2 + [YEAR_OF_PLENTY]*2 + [ROAD_BUILDING]*2 + [VP_CARD]*5
        for i in range(4):
            self.players += [Player(PLAYER_COLORS[i], PLAYER_COORDS[i])]
        self.building_phase = True
        self.late_building_phase = False
        self.die_1 = 0
        self.die_2 = 0
    
    def add_player_sockets(self,players_sockets):
        self.players_sockets = players_sockets

    def game_finished(self):
        if self.decision_failed or self.turn > 1000:
            return True
        is_win = False
        for player in self.players:
            if (player.vp + player.vp_cards) > 9:
                is_win = True
        return is_win

    def deal_cards(self, result):
        for tile in self.table.tiles:
            if (tile.number == result and tile.robber == False):
                for corner in tile.corners:
                    if corner.building.building != -1 and self.players[corner.building.player].resource_cards < 20:
                        if corner.building.building == CITY:
                            if tile.resource == FOREST:
                                self.players[corner.building.player].lumber += 2
                            elif tile.resource == HILLS:
                                self.players[corner.building.player].brick += 2
                            elif tile.resource == MOUNTAINS:
                                self.players[corner.building.player].ore += 2
                            elif tile.resource == PASTURE:
                                self.players[corner.building.player].wool += 2
                            else:
                                self.players[corner.building.player].grain += 2
                            self.players[corner.building.player].resource_cards += 2
                        elif corner.building.building == SETTLEMENT:
                            if tile.resource == FOREST:
                                self.players[corner.building.player].lumber += 1
                            elif tile.resource == HILLS:
                                self.players[corner.building.player].brick += 1
                            elif tile.resource == MOUNTAINS:
                                self.players[corner.building.player].ore += 1
                            elif tile.resource == PASTURE:
                                self.players[corner.building.player].wool += 1
                            else:
                                self.players[corner.building.player].grain += 1
                            self.players[corner.building.player].resource_cards += 1

    def find_robber(self):
        for i in range(19):
            if self.table.tiles[i].robber == True:
                return i
        return -1

    def get_robber_options(self):
        total_options = []
        for i in range(len(self.table.tiles)):
            if (self.table.tiles[i].robber == False):
                tile_in = False
                for corner in self.table.tiles[i].corners:
                    if corner.building.building != -1 and corner.building.building != self.player_in_turn and self.players[corner.building.player].resource_cards > 0:
                        option = (PLACE_ROBBER, i, corner.building.player)
                        if (option not in total_options):
                            total_options += [option]
                        tile_in = True
                if tile_in == False:
                    option = (PLACE_ROBBER, i)
                    total_options += [option]
        return(total_options)

    def roll_dice(self):
        self.die_1 = random.randint(1,6)
        self.die_2 = random.randint(1,6)
        result = self.die_1 + self.die_2
        if result == 7:
            for i in range(len(self.players)):
                if self.players[i].resource_cards > 7:
                    all_possibilites = self.get_all_discards(i)
                    all_discards = []
                    for j in range(len(all_possibilites)):
                        all_discards += [(DISCARD, all_possibilites[j])]
                    chosen = self.get_next_action(all_discards, self.player_in_turn)
                    if (chosen == -1):
                        return
                    for card in all_discards[chosen][1]:
                        if card == FOREST:
                            self.players[i].lumber -= 1
                        elif card == HILLS:
                            self.players[i].brick -= 1
                        elif card == PASTURE:
                            self.players[i].wool -= 1
                        elif card == MOUNTAINS:
                            self.players[i].ore -= 1
                        else:
                            self.players[i].grain -= 1
                        self.players[i].resource_cards -= 1
            possible_actions_list = self.get_robber_options()
            option = self.get_next_action(possible_actions_list, self.player_in_turn)
            if (option == -1):
                return
            self.make_decision(possible_actions_list[option])
        else:
            self.deal_cards(result)

    def road_is_buildable(self, player, index):
        if self.edges[index].road != -1:
            return False
        for road in self.edges[index].adjacents:
            if self.edges[road].road == player:
                return True
        return False

    def place_road(self, index):
        self.edges[index].add_road(self.player_in_turn)
        self.players[self.player_in_turn].roads_left -= 1
        max_roads = self.depthFirstSearch(index)
        self.players[self.player_in_turn].longest_path = max_roads if max_roads > self.players[self.player_in_turn].longest_path else self.players[self.player_in_turn].longest_path
        is_longest = True
        if self.players[self.player_in_turn].longest_path > 4:
            for player in [s for s in self.players if s != self.players[self.player_in_turn]]:
                if player.longest_path >= self.players[self.player_in_turn].longest_path:
                    is_longest = False
                    break
            if (is_longest):
                for player in self.players:
                    if player.road_bonus == True:
                        player.road_bonus = False
                        player.vp -= 2
                self.players[self.player_in_turn].road_bonus = True
                self.players[self.player_in_turn].vp += 2


    def search_expand(self,node):
        if node[1] == []:
            return [s for s in self.edges[node[0]].adjacents if self.edges[s].road == self.player_in_turn]
        roads = []
        for i in self.edges[node[0]].adjacents:
            if i not in self.edges[node[1][-1]].adjacents and self.edges[i].road == self.player_in_turn:
                roads += [i]
        return roads

    def depthFirstSearch(self, start):
        STATE = 0
        EXPANDED = 1
        COST = 2
        start_node = [start, [], 1]
        frontier = utils.Stack()
        frontier.push(start_node)
        max_number = 0

        while (not(frontier.isEmpty())):
            node = frontier.pop()
            if ((node[STATE] not in node[EXPANDED])):
                max_number = node[COST] if node[COST] > max_number else max_number
                children = self.search_expand(node)
                node[EXPANDED] += [node[STATE]]
                for child in children:
                    new_node = [child, node[EXPANDED], node[COST] + 1]
                    frontier.push(new_node)
        return max_number
    
    def settlement_is_buildable(self, player, index):
        if self.corners[index].building.building != -1:
            return False
        for building in self.corners[index].adjacents:
            if self.corners[building].building.building != -1:
                return False
        if self.building_phase:
            return True
        for road in self.corners[index].adjacents_edges:
            if self.edges[road].road == player:
                return True
        return False

    def place_settlement(self, index):
        is_port = self.corners[index].add_settlement(self.player_in_turn)
        if is_port != -1:
            self.players[self.player_in_turn].ports[is_port] = True
        self.players[self.player_in_turn].vp += 1
        self.players[self.player_in_turn].settlements_left -= 1
        if self.late_building_phase:
            for tile in self.corners[index].adjacents_tiles:
                if self.table.tiles[tile].resource == FOREST:
                    self.players[self.player_in_turn].lumber += 1
                elif self.table.tiles[tile].resource == HILLS:
                    self.players[self.player_in_turn].brick += 1
                elif self.table.tiles[tile].resource == MOUNTAINS:
                    self.players[self.player_in_turn].ore += 1
                elif self.table.tiles[tile].resource == PASTURE:
                    self.players[self.player_in_turn].wool += 1
                elif self.table.tiles[tile].resource == FIELDS:
                    self.players[self.player_in_turn].grain += 1
                if self.table.tiles[tile].resource != DESERT:
                    self.players[self.player_in_turn].resource_cards += 1
    
    def upgrade_settlement(self, index):
        self.corners[index].upgrade_settlement()
        self.players[self.player_in_turn].vp += 1
        self.players[self.player_in_turn].settlements_left += 1
        self.players[self.player_in_turn].cities_left -= 1

    def place_settlement_and_road(self, settlement_index, road_index):
        place_settlement(settlement_index)
        place_road(road_index)
    
    def next_turn(self):
        self.turn += 1
        self.player_in_turn = self.turn % 4
        self.trades_made = 0
     
    def get_development_card(self, development_cards_left):
        rand_numb = random.randint(0,len(development_cards_left) - 1)
        return(development_cards_left.pop(rand_numb))

    def conjunto_potencia(c):
        if len(c) == 0:
            return [[]]
        r = Game.conjunto_potencia(c[:-1])
        return r + [s + [c[-1]] for s in r]

    def total_combinaciones(c, n):
        return [s for s in Game.conjunto_potencia(c) if len(s) == n]

    def get_all_discards(self,player_dest):
        all_resources = [FOREST]*self.players[player_dest].lumber + [HILLS]*self.players[player_dest].brick + [PASTURE]*self.players[player_dest].wool + [FIELDS]*self.players[player_dest].grain + [MOUNTAINS]*self.players[player_dest].ore
        return Game.total_combinaciones(all_resources, len(all_resources)//2)

    def NNdecision(self, possible_actions_list, actiontypes, player):
        common_inputs = [self.players[player].lumber, self.players[player].brick, self.players[player].ore, self.players[player].wool, self.players[player].grain]
        common_inputs += [self.players[player].knights, self.players[player].road_building, self.players[player].year_of_plenty, self.players[player].monopoly]
        for index in range(4):
            common_inputs += [self.players[index].resource_cards]
        for tile in self.table.tiles:
            common_inputs += [tile.resource, tile.number, 1 if tile.robber else 0]
        for corner in self.corners:
            common_inputs += [corner.building.building, corner.port]
        for edge in self.edges:
            common_inputs += [edge.road]
        for index in range(4):
            common_inputs += [self.players[index].longest_path, self.players[index].active_knights]
        for index in range(4):
            common_inputs += [self.players[index].vp]
        red_inputs = []
        for i in range(17):
            if i in actiontypes:
                red_inputs += [1]
            else:
                red_inputs += [0]
        type_probabilities = NN(self.red, common_inputs + red_inputs)
        type_possible = []
        while (len(type_possible) == 0):
            type_chosen = -1
            list_max = -1
            for i in range(len(type_probabilities)):
                if (type_probabilities[i] > list_max):
                    list_max = type_probabilities[i]
            for i in range(len(type_probabilities)):
                if (type_probabilities[i] == list_max):
                    type_probabilities[i] = -1
                    type_chosen = i
                    break
            if (type_chosen == -1):
                self.decision_failed = True
                return -1
            for action in possible_actions_list:
                if type(action) == type(0) and type_chosen == action:
                    type_possible += [action]
                elif type(action) == type(tuple()) and type_chosen == action[0]:
                    type_possible += [action]
            if (type_chosen == DOMESTIC_TRADE):
                if (self.trades_made > 4):
                    type_possible = []

        action_chosen = type_possible[random.randint(0,len(type_possible)-1)]
        for i in range(0,len(possible_actions_list)):
            if action_chosen == possible_actions_list[i]:
                return i
        return -1

    def AlmostRandomDecision(self, possible_actions_list, actiontypes, player):
        prob_sum = []
        for i in actiontypes:
            if i == SKIP_TURN:
                if self.players[player].resource_cards < 12:
                    prob_sum += [SKIP_TURN]*PROB_SKIP_TURN
            elif i == PLACE_ROAD:
                prob_sum += [PLACE_ROAD]*PROB_PLACE_ROAD
            elif i == PLACE_SETTLEMENT:
                prob_sum += [PLACE_SETTLEMENT]*PROB_PLACE_SETTLEMENT
            elif i == PLACE_CITY:
                prob_sum += [PLACE_CITY]*PROB_PLACE_CITY
            elif i == BUY_RESOURCE_CARD:
                prob_sum += [BUY_RESOURCE_CARD]*PROB_BUY_RESOURCE_CARD
            elif i == PLAY_ROADS:
                prob_sum += [PLAY_ROADS]*PROB_PLAY_ROADS
            elif i == PLAY_KNIGHT:
                prob_sum += [PLAY_KNIGHT]*PROB_PLAY_KNIGHT
            elif i == PLAY_YEAR_OF_PLENTY:
                prob_sum += [PLAY_YEAR_OF_PLENTY]*PROB_PLAY_YEAR_OF_PLENTY
            elif i == PLAY_MONOPOLY:
                prob_sum += [PLAY_MONOPOLY]*PROB_PLAY_MONOPOLY
            elif i == MARITIME_TRADE:
                prob_sum += [MARITIME_TRADE]*PROB_MARITIME_TRADE
            elif i == DOMESTIC_TRADE:
                prob_sum += [DOMESTIC_TRADE]*PROB_DOMESTIC_TRADE
        if len(prob_sum) == 0:
            return 0 if len(possible_actions_list) == 1 else random.randint(0,len(possible_actions_list)-1)
        type_chosen = prob_sum.pop(random.randint(0,len(prob_sum)-1))
        type_possible = []
        for action in possible_actions_list:
            if type(action) == type(0) and type_chosen == action:
                type_possible += [action]
            elif type(action) == type(tuple()) and type_chosen == action[0]:
                type_possible += [action]
        action_chosen = type_possible[random.randint(0,len(type_possible)-1)]
        for i in range(0,len(possible_actions_list)):
            if action_chosen == possible_actions_list[i]:
                return i
        return -1

    def get_next_action(self, possible_actions_list, player):
        if len(possible_actions_list) == 2 and type(possible_actions_list[0]) == type([]) and possible_actions_list[0][0] == ACCEPT_TRADE:
            if possible_actions_list[0][3] == FOREST:
                if self.players[player].lumber < possible_actions_list[0][4]: return 1
            elif possible_actions_list[0][3] == HILLS:
                if self.players[player].brick < possible_actions_list[0][4]: return 1
            elif possible_actions_list[0][3] == MOUNTAINS:
                if self.players[player].ore < possible_actions_list[0][4]: return 1
            elif possible_actions_list[0][3] == PASTURE:
                if self.players[player].wool < possible_actions_list[0][4]: return 1
            else:
                if self.players[player].grain < possible_actions_list[0][4]: return 1
        chosen = 0
        actiontypes = set()
        for action in possible_actions_list:
            if type(action) == type(0):
                actiontypes.update([action])
            else:
                if not (action[0] == DOMESTIC_TRADE and self.trades_made > 4):
                    actiontypes.update([action[0]])
        if player == 0:
            return self.NNdecision(possible_actions_list, actiontypes, player)
        else:
            return self.AlmostRandomDecision(possible_actions_list, actiontypes, player)

    def steal_card(self, player_dest):
        all_resources = [FOREST]*self.players[player_dest].lumber + [HILLS]*self.players[player_dest].brick + [PASTURE]*self.players[player_dest].wool + [FIELDS]*self.players[player_dest].grain + [MOUNTAINS]*self.players[player_dest].ore
        if len(all_resources) < 1:
            return
        chosen = 0 if len(all_resources) < 2 else random.randint(0,len(all_resources)-1)
        if all_resources[chosen] == FOREST:
            self.players[self.player_in_turn].lumber += 1
            self.players[player_dest].lumber -= 1
        elif all_resources[chosen] == HILLS:
            self.players[self.player_in_turn].brick += 1
            self.players[player_dest].brick -= 1
        elif all_resources[chosen] == MOUNTAINS:
            self.players[self.player_in_turn].ore += 1
            self.players[player_dest].ore -= 1
        elif all_resources[chosen] == PASTURE:
            self.players[self.player_in_turn].wool += 1
            self.players[player_dest].wool -= 1
        else:
            self.players[self.player_in_turn].grain += 1
            self.players[player_dest].grain -= 1
        self.players[self.player_in_turn].resource_cards += 1
        self.players[player_dest].resource_cards -= 1

    def check_knight_bonus(self):
        if (self.players[self.player_in_turn].active_knights > 2):
            highest = True
            for player in [s for s in self.players if s != self.players[self.player_in_turn]]:
                if player.active_knights >= self.players[self.player_in_turn].active_knights:
                    highest = False
                    break
            if (highest):
                for player in self.players:
                    if player.knight_bonus == True:
                        player.knight_bonus = False
                        player.vp -= 2
                self.players[self.player_in_turn].knight_bonus = True
                self.players[self.player_in_turn].vp += 2

    def make_decision(self, decision):
        if (decision == SKIP_TURN):
            self.next_turn()
            self.roll_dice()
        elif(decision == BUY_RESOURCE_CARD):
            self.players[self.player_in_turn].ore -= 1
            self.players[self.player_in_turn].grain -= 1
            self.players[self.player_in_turn].wool -= 1
            self.players[self.player_in_turn].resource_cards -= 3
            card_type = self.get_development_card(self.development_cards_left)
            if card_type == 0:
                self.players[self.player_in_turn].knights += 1    
            elif card_type == 1:
                self.players[self.player_in_turn].monopoly += 1
            elif card_type == 2:
                self.players[self.player_in_turn].road_building += 1    
            elif card_type == 3:
                self.players[self.player_in_turn].year_of_plenty += 1
            elif card_type == 4:
                self.players[self.player_in_turn].vp_cards += 1
        elif(decision == PLAY_KNIGHT):
            self.players[self.player_in_turn].knights -= 1    
            self.players[self.player_in_turn].active_knights += 1
            self.check_knight_bonus()
            possible_actions_list = self.get_robber_options()
            option = self.get_next_action(possible_actions_list, self.player_in_turn)
            if (option == -1):
                return
            self.make_decision(possible_actions_list[option])
        elif(decision == PLAY_ROADS):
            possible_roads = []
            for j in range(2):
                for i in range(72):
                    if self.road_is_buildable(self.player_in_turn, i):
                        possible_roads += [(PLACE_FREE_ROAD,i)]
                option = self.get_next_action(possible_roads, self.player_in_turn)
                if (option == -1):
                    return
                self.make_decision(possible_roads[option])
            self.players[self.player_in_turn].road_building -= 1
        elif(decision[0] == PLACE_ROAD):
            self.players[self.player_in_turn].brick -= 1
            self.players[self.player_in_turn].lumber -= 1
            self.players[self.player_in_turn].resource_cards -= 2
            self.place_road(decision[1])
        elif(decision[0] == PLACE_FREE_ROAD):
            self.place_road(decision[1])
        elif(decision[0] == PLACE_SETTLEMENT):
            self.players[self.player_in_turn].brick -= 1
            self.players[self.player_in_turn].lumber -= 1
            self.players[self.player_in_turn].wool -= 1
            self.players[self.player_in_turn].grain -= 1
            self.players[self.player_in_turn].resource_cards -= 4
            self.place_settlement(decision[1])
        elif(decision[0] == PLACE_CITY):
            self.players[self.player_in_turn].ore -= 3
            self.players[self.player_in_turn].grain -= 2
            self.players[self.player_in_turn].resource_cards -= 5
            self.upgrade_settlement(decision[1])
        elif(decision[0] == PLACE_SETTLEMENT_THEN_ROAD):
            self.place_settlement(decision[1])
            self.place_road(decision[2])
        elif(decision[0] == PLACE_ROBBER):
            self.table.tiles[self.find_robber()].robber = False
            self.table.tiles[decision[1]].robber = True
            if len(decision) > 2:
                self.steal_card(decision[2])
        elif(decision[0] == PLAY_MONOPOLY):
            total_resource = 0
            for player in self.players:
                if player != self.players[self.player_in_turn]:
                    if decision[1] == FOREST:
                        self.players[self.player_in_turn].lumber += player.lumber
                        self.players[self.player_in_turn].resource_cards += player.lumber
                        player.resource_cards -= player.lumber
                        player.lumber = 0
                    elif decision[1] == MOUNTAINS:
                        self.players[self.player_in_turn].ore += player.ore
                        self.players[self.player_in_turn].resource_cards += player.ore
                        player.resource_cards -= player.ore
                        player.ore = 0
                    elif decision[1] == HILLS:
                        self.players[self.player_in_turn].brick += player.brick
                        self.players[self.player_in_turn].resource_cards += player.brick
                        player.resource_cards -= player.brick
                        player.brick = 0
                    elif decision[1] == PASTURE:
                        self.players[self.player_in_turn].wool += player.wool
                        self.players[self.player_in_turn].resource_cards += player.wool
                        player.resource_cards -= player.wool
                        player.wool = 0
                    else:
                        self.players[self.player_in_turn].grain += player.grain
                        self.players[self.player_in_turn].resource_cards += player.grain
                        player.resource_cards -= player.grain
                        player.grain = 0
            self.players[self.player_in_turn].monopoly -= 1
        elif(decision[0] == PLAY_YEAR_OF_PLENTY):
            for resource in decision[1:]:
                if decision[1] == FOREST:
                    self.players[self.player_in_turn].lumber += 1
                elif decision[1] == MOUNTAINS:
                    self.players[self.player_in_turn].ore += 1
                elif decision[1] == HILLS:
                    self.players[self.player_in_turn].brick += 1
                elif decision[1] == PASTURE:
                    self.players[self.player_in_turn].wool += 1
                else:
                    self.players[self.player_in_turn].grain += 1
            self.players[self.player_in_turn].resource_cards += 2
            self.players[self.player_in_turn].year_of_plenty -= 1
        elif(decision[0] == MARITIME_TRADE):
            count = 4
            if self.players[self.player_in_turn].ports[0] == True:
                count = 3
            if self.players[self.player_in_turn].ports[decision[1]] == True:
                    count = 2
            if decision[1] == FOREST:
                self.players[self.player_in_turn].lumber -= count
            elif decision[1] == MOUNTAINS:
                self.players[self.player_in_turn].ore -= count
            elif decision[1] == HILLS:
                self.players[self.player_in_turn].brick -= count
            elif decision[1] == PASTURE:
                self.players[self.player_in_turn].wool -= count
            else:
                self.players[self.player_in_turn].grain -= count
            
            if decision[2] == FOREST:
                self.players[self.player_in_turn].lumber += 1
            elif decision[2] == MOUNTAINS:
                self.players[self.player_in_turn].ore += 1
            elif decision[2] == HILLS:
                self.players[self.player_in_turn].brick += 1
            elif decision[2] == PASTURE:
                self.players[self.player_in_turn].wool += 1
            else:
                self.players[self.player_in_turn].grain += 1
            self.players[self.player_in_turn].resource_cards -= count - 1
        
        elif(decision[0] == DOMESTIC_TRADE):
            possible_options = [tuple([DENY_TRADE] + list(decision[1:]))]
            accepted = -1
            self.trades_made += 1
            for index in range(self.player_in_turn + 1,self.player_in_turn + 4):
                player_dest = index % 4
                if self.players[player_dest].able_to_trade(decision[3],decision[4]):
                    possible_options += [tuple([ACCEPT_TRADE] + list(decision[1:]))]
                trading_decision = self.get_next_action(possible_options, player_dest)
                if (trading_decision == -1):
                    return
                is_accepted = possible_options[trading_decision]
                if is_accepted[0] == ACCEPT_TRADE:
                    accepted = player_dest
                    break
                possible_options = [tuple([DENY_TRADE] + list(decision[1:]))]
            if accepted != -1:
                if decision[1] == FOREST:
                    self.players[self.player_in_turn].lumber -= decision[2]
                    self.players[accepted].lumber += decision[2]
                elif decision[1] == MOUNTAINS:
                    self.players[self.player_in_turn].ore -= decision[2]
                    self.players[accepted].ore += decision[2]
                elif decision[1] == HILLS:
                    self.players[self.player_in_turn].brick -= decision[2]
                    self.players[accepted].brick += decision[2]
                elif decision[1] == PASTURE:
                    self.players[self.player_in_turn].wool -= decision[2]
                    self.players[accepted].wool += decision[2]
                else:
                    self.players[self.player_in_turn].grain -= decision[2]
                    self.players[accepted].grain += decision[2]

                if decision[3] == FOREST:
                    self.players[self.player_in_turn].lumber += decision[4]
                    self.players[accepted].lumber -= decision[4]
                elif decision[3] == MOUNTAINS:
                    self.players[self.player_in_turn].ore += decision[4]
                    self.players[accepted].ore -= decision[4]
                elif decision[3] == HILLS:
                    self.players[self.player_in_turn].brick += decision[4]
                    self.players[accepted].brick -= decision[4]
                elif decision[3] == PASTURE:
                    self.players[self.player_in_turn].wool += decision[4]
                    self.players[accepted].wool -= decision[4]
                else:
                    self.players[self.player_in_turn].grain += decision[4]
                    self.players[accepted].grain -= decision[4]
                