
import pygame

from .tile import Tile
from .constants import TILE_SIZE

_adjacent_offsets:list[tuple[int, int]] = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (1, -1), (-1, 1)]

class TileMap:
    def __init__(self, game_manager, map_size:tuple[int, int], tiles:dict[tuple[int, int], Tile] = {}) -> None:
        self.game_manager = game_manager
        self.map_size = map_size
        self.tiles = tiles
    
    def add_tile(self, pos:tuple[int, int], tile:Tile):
        self.tiles[pos] = tile
    
    def remove_tile(self, pos:tuple[int, int]):
        del self.tiles[pos]
    
    def handle_event(self, event:pygame.Event):
        #idk what this is gunna be for but sure lets put it in
        for tile in self.tiles.values():
            tile.handle_event(event)
    
    def update(self, dt:float):
        #Update for animated tiles
        for tile in self.tiles.values():
            tile.update(dt)
    
    def draw(self, screen:pygame.Surface):
        for pos, tile in self.tiles.items():
            screen.blit(self.game_manager.assets[tile.tile_type], (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))
        
    
    def list_adjacent_tiles(self, pos:tuple[int, int]) -> list[Tile]:
        tiles = []
        for adjacent_offset in _adjacent_offsets:
            adjacent_pos = (pos[0] + adjacent_offset[0], pos[1] + adjacent_offset[1])
            
            adjacent_tile = self.tiles.get(adjacent_pos, None)
            if adjacent_tile is None:
                continue
            tiles.append(adjacent_tile)
        
        return tiles
    
    def list_adjacent_rects(self, pos:tuple[int, int]) -> list[pygame.Rect]:
        rects = []
        for adjacent_tile in self.list_adjacent_tiles(pos):
            rects.append(pygame.Rect(adjacent_tile.pos[0] * TILE_SIZE, adjacent_tile.pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects
        
    
    def entity_adjacent_tiles(self, entity_pos:tuple[float, float]) -> list[Tile]:
        adjusted_pos = int(entity_pos[0]/TILE_SIZE), int(entity_pos[1]/TILE_SIZE)
        return self.list_adjacent_tiles(adjusted_pos)
        