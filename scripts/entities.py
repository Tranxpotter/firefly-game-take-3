import pygame

from .velocity import Velocity, velocity_factory
from .constants import PLAYER_SIZE
from .tilemap import TileMap


class Entity(pygame.sprite.Sprite):
    def __init__(self, game_manager, entity_type:str, pos:tuple[float, float], size:tuple[float, float], velocity:Velocity|None, *groups) -> None:
        super().__init__(*groups)
        self.game_manager = game_manager
        self.entity_type = entity_type
        self.x, self.y = pos
        self.width, self.height = size
        
        if velocity is None:
            self.velocity = Velocity()
        else:
            self.velocity = velocity
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, pos:tuple[float, float]):
        self.x, self.y = pos
        
    @property
    def size(self):
        return (self.width, self.height)
    
    @size.setter
    def size(self, size:tuple[float, float]):
        self.width, self.height = size
    
    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    @rect.setter
    def rect(self, value):
        self.x, self.y, self.width, self.height = value.x, value.y, value.width, value.height
    
    
    def handle_event(self, event:pygame.Event):...
    
    def update(self, dt:float):
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt
    
    def draw(self, screen:pygame.Surface):
        screen.blit(self.game_manager.assets[self.entity_type], self.rect)


class SolidEntity(Entity):
    def __init__(self, game_manager, entity_type: str, pos: tuple[float, float], size: tuple[float, float], velocity: Velocity | None, *groups) -> None:
        super().__init__(game_manager, entity_type, pos, size, velocity, *groups)
        self.collisions = {"top":False, "bottom":False, "left":False, "right":False}
    
    def update(self, dt: float):
        self.collisions = {"top":False, "bottom":False, "left":False, "right":False}
        try:
            tilemap:TileMap = self.game_manager.__getattribute__("tilemap")
        except AttributeError as e:
            print("missing tilemap from game_manager")
            return
        
        assert isinstance(tilemap, TileMap)
        
        
        tile_pos = tilemap.entity_pos_to_tile_pos(self.pos)
        collidable_rects = tilemap.list_adjacent_rects(tile_pos, True)
        
        #Check horizontal collisions
        self.x += self.velocity.x * dt
        for collidable_rect in collidable_rects:
            if self.rect.colliderect(collidable_rect):
                if self.velocity.x > 0:
                    self.x = collidable_rect.left - self.width
                    self.collisions["right"] = True
                elif self.velocity.x < 0:
                    self.x = collidable_rect.right
                    self.collisions["left"] = True
                
                self.velocity.x = 0
        
        #Check vertical collisions
        self.y += self.velocity.y * dt
        for collidable_rect in collidable_rects:
            if self.rect.colliderect(collidable_rect):
                if self.velocity.y > 0:
                    self.y = collidable_rect.top - self.height
                    self.collisions["bottom"] = True
                elif self.velocity.y < 0:
                    self.y = collidable_rect.bottom
                    self.collisions["top"] = True
                
                self.velocity.y = 0
        




PlayerGroup = pygame.sprite.Group()
class Player(SolidEntity):
    def __init__(self, game_manager, pos: tuple[float, float], velocity: Velocity|None = None) -> None:
        super().__init__(game_manager, "player", pos, PLAYER_SIZE, velocity, PlayerGroup)
        self.movement_speed = 240
        self.can_jump = False
    
    def handle_event(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.velocity.x = -self.movement_speed
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.velocity.x = self.movement_speed
            
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not self.can_jump:
                    return
                self.velocity.y = -721
                self.can_jump = False
        
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.velocity.x = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.velocity.x = 0
            
    
    def update(self, dt: float):
        #Gravity velocity update
        self.velocity.y = min(self.velocity.y + 1000*dt, 1000)
        
        super().update(dt)
        if self.collisions["bottom"]:
            self.can_jump = True
    
    # def draw(self, screen: pygame.Surface):
    #     assert self.rect is not None
    #     pygame.draw.rect(screen, (255, 0, 0), self.rect)
        


















