

import pygame

from .entities import Player
from .tilemap import TileMap
from .tile import Tile
from .utils import load_image


class GameManager:
    def __init__(self) -> None:
        
        self.assets = {
            "dirt":load_image("tiles/dirt_tile.png"),
            "grass":load_image("tiles/grass_tile.png"),
            "player":load_image("entities/player.png", (0, 0, 0))
        }
        
        
        self.player = Player(self, (0, 0))
        tiles:dict[tuple[int, int], Tile] = {
            (0, 8):Tile("dirt", (0, 8), solid=True),
            (0, 6):Tile("grass", (0, 6), solid=True),
            (0, 7):Tile("dirt", (0, 7), solid=True),
            (1, 8):Tile("dirt", (1, 8), solid=True),
            (1, 7):Tile("dirt", (1, 7), solid=True),
            (1, 6):Tile("grass", (1, 6), solid=True)
        }
        for i in range(10):
            tiles[(i+5, 10)] = Tile("dirt", (i+5, 10), solid=True)
            tiles[(15, i)] = Tile("grass", (15, i), solid=True)
        
        for i in range(3):
            tiles[(i+7, 8)] = Tile("grass", (i+7, 8), jump_thru=True)
        self.tilemap = TileMap(self, (100, 100), tiles)
        
    
    def handle_event(self, event:pygame.Event):
        self.player.handle_event(event)
        self.tilemap.handle_event(event)
    
    def update(self, dt:float):
        self.player.update(dt)
        self.tilemap.update(dt)
    
    def draw(self, screen:pygame.Surface):
        self.tilemap.draw(screen)
        self.player.draw(screen)