import random
import pygame
from constants import *
from pygame.locals import *

class Tile:
    def __init__(self, resource, number, corners, corners_index, edges, edges_index):
        self.corners = [corners[corners_index[0]],corners[corners_index[1]],corners[corners_index[2]],corners[corners_index[3]],corners[corners_index[4]],corners[corners_index[5]]]
        self.edges = [edges[edges_index[0]],edges[edges_index[1]],edges[edges_index[2]],edges[edges_index[3]],edges[edges_index[4]],edges[edges_index[5]]]
        self.resource = resource
        self.number = number
        self.robber = False

    def add_building(self, building):
        self.corners = building

    def add_road(self, player):
        self.edges = player

class Table:
    def __init__(self,corners,edges):
        self.tiles = []
        designed_numbers = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
        available_resources = [FOREST]*4 + [HILLS]*3 + [MOUNTAINS]*3 + [PASTURE]*4 + [FIELDS]*4 + [DESERT]
        j = 0
        for i in range(19):
            if (i == 18):
                r = 0
            else:
                r = random.randint(0, 18 - i)
            resource = available_resources.pop(r)
            if (resource == DESERT):
                tile = Tile(resource,0, corners, TILE_CORNERS_INDEX[i], edges, TILE_EDGES_INDEX[i])
                tile.robber = True
                j = 1
            else:
                tile = Tile(resource,designed_numbers[i-j], corners, TILE_CORNERS_INDEX[i], edges, TILE_EDGES_INDEX[i])
            self.tiles += [tile]
