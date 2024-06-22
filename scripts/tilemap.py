
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
    
    def draw(self, screen:pygame.Surface, offset:tuple[int, int] = (0, 0)):
        
        
        for tile_x in range(int(offset[0] // TILE_SIZE), int((offset[0] + screen.get_width()) // TILE_SIZE) + 1):
            for tile_y in range(int(offset[1] // TILE_SIZE), int((offset[1] + screen.get_height()) // TILE_SIZE) + 1):
                if (tile_x, tile_y) in self.tiles:
                    tile = self.tiles[(tile_x, tile_y)]
                    screen.blit(self.game_manager.assets[tile.tile_type], (tile.pos[0]*TILE_SIZE - offset[0], tile.pos[1]*TILE_SIZE - offset[1]))
        

    
    def entity_pos_to_tile_pos(self, pos:tuple[float, float]) -> tuple[int, int]:
        return int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)
    
    def list_adjacent_tiles(self, pos:tuple[int, int]) -> list[Tile]:
        tiles = []
        for adjacent_offset in _adjacent_offsets:
            adjacent_pos = (pos[0] + adjacent_offset[0], pos[1] + adjacent_offset[1])
            
            adjacent_tile = self.tiles.get(adjacent_pos, None)
            if adjacent_tile is None:
                continue
            tiles.append(adjacent_tile)
        
        return tiles
    
    def list_adjacent_rects(self, pos:tuple[int, int], collidable_only:bool = False) -> list[pygame.Rect]:
        rects = []
        for adjacent_tile in self.list_adjacent_tiles(pos):
            if collidable_only:
                if not adjacent_tile.solid and (adjacent_tile.jump_thru and not adjacent_tile.pos[1] > pos[1]):
                    continue
            
            rects.append(pygame.Rect(adjacent_tile.pos[0] * TILE_SIZE, adjacent_tile.pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects
    
    
    
    def entity_adjacent_tiles(self, entity_pos:tuple[float, float]) -> list[Tile]:
        adjusted_pos = int(entity_pos[0]//TILE_SIZE), int(entity_pos[1]//TILE_SIZE)
        return self.list_adjacent_tiles(adjusted_pos)
    
    def entity_collidable_rects(self, entity_pos:tuple[float, float], entity) -> list[pygame.Rect]:
        pos = self.entity_pos_to_tile_pos(entity_pos)
        adjacent_tiles = self.list_adjacent_tiles(pos)
        
        rects = []
        for tile in adjacent_tiles:
            if tile.solid:
                rects.append(pygame.Rect(tile.pos[0] * TILE_SIZE, tile.pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile.jump_thru and entity.velocity.y >= 0 and tile.pos[1] > pos[1]:
                rects.append(pygame.Rect(tile.pos[0] * TILE_SIZE, tile.pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        return rects