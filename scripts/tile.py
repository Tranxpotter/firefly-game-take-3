import pygame

from .constants import TILE_SIZE
from .utils import load_image

class Tile:
    def __init__(self, tile_type:str, pos:tuple[int, int], *, solid:bool = False, jump_thru:bool = False) -> None:
        self.solid = solid
        self.jump_thru = jump_thru
        self.tile_type = tile_type
        self.pos = pos
    
    
    def handle_event(self, event:pygame.Event):
        ...
    
    
    def update(self, dt:float):
        ...














