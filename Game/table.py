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

    def print_tile(self,screen,font,x,y):
        h=HEX_H/4
        w=HEX_W/2
        corners = ((x+w,y), (x,y+h), (x,y+3*h), (x+w,y+4*h), (x+2*w,y+3*h), (x+2*w,y+h))
        if(self.resource == MOUNTAINS):
            color = COLOR_MOUNTAINS
        elif(self.resource == FIELDS):
            color = COLOR_FIELDS
        elif(self.resource == HILLS):
            color = COLOR_HILLS
        elif(self.resource == FOREST):
            color = COLOR_FOREST
        elif(self.resource == PASTURE):
            color = COLOR_PASTURE
        else:
            color = COLOR_DESERT
        pygame.draw.polygon(screen, color, corners)
        if (self.robber == True):
            pygame.draw.circle(screen, (0,0,0), (x+w,y+2*h), h/2)
        else:
            if (self.number != 0):
                screen.blit(font.render(str(self.number),True,(0,0,0)), (x+w-4, y+2*h-3))


class Table:
    def __init__(self,screen,font,corners,edges):
        self.screen = screen
        self.font = font
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

    def print_table(self):
        coord = 0
        for tile in self.tiles:
            tile.print_tile(self.screen,self.font,HEX_COORDS[coord][0], HEX_COORDS[coord][1])
            coord += 1
        port_type = 0
        for coords in PORT_COORDS:
            color = (232, 210, 190)
            pygame.draw.polygon(self.screen, color, coords)
            if (PORT_TYPES[port_type] == 1):
                color = COLOR_FOREST
            elif (PORT_TYPES[port_type] == 2):
                color = COLOR_HILLS
            elif (PORT_TYPES[port_type] == 3):
                color = COLOR_PASTURE
            elif (PORT_TYPES[port_type] == 4):
                color = COLOR_FIELDS
            elif (PORT_TYPES[port_type] == 5):
                color = COLOR_MOUNTAINS
            pygame.draw.circle(self.screen, color, coords[0], PORT_RADIUS)
            port_type += 1
