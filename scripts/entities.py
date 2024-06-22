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
    
    def get_curr_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def handle_event(self, event:pygame.Event):...
    
    def update(self, dt:float):
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt
    
    def img(self):
        return self.game_manager.assets[self.entity_type]
    
    def draw(self, screen:pygame.Surface, offset:tuple[int, int] = (0, 0)):
        screen.blit(self.img(), (self.rect.x - offset[0], self.rect.y - offset[1]))


class SolidEntity(Entity):
    def __init__(self, game_manager, entity_type: str, pos: tuple[float, float], size: tuple[float, float], velocity: Velocity | None, *groups) -> None:
        super().__init__(game_manager, entity_type, pos, size, velocity, *groups)
        self.collisions = {"top":False, "bottom":False, "left":False, "right":False}
        # self.frame_counter = 0
    
    def update(self, dt: float):
        # self.frame_counter += 1
        self.collisions = {"top":False, "bottom":False, "left":False, "right":False}
        try:
            tilemap:TileMap = self.game_manager.__getattribute__("tilemap")
        except AttributeError as e:
            print("missing tilemap from game_manager")
            return
        
        assert isinstance(tilemap, TileMap)
        
        
        
        
        #Check horizontal collisions
        self.x += self.velocity.x * dt
        entity_rect = self.get_curr_rect()
        
        collidable_rects = tilemap.entity_collidable_rects(self.pos, self)
        for collidable_rect in collidable_rects:
            if entity_rect.colliderect(collidable_rect):
                # print("collide x", entity_rect, collidable_rect, self.frame_counter)
                if self.velocity.x > 0:
                    entity_rect.right = collidable_rect.left
                    self.collisions["right"] = True
                elif self.velocity.x < 0:
                    entity_rect.left = collidable_rect.right
                    self.collisions["left"] = True
                self.x = entity_rect.x
                # self.velocity.x = 0
        
        #Check vertical collisions
        self.y += self.velocity.y * dt
        entity_rect = self.get_curr_rect()
        
        collidable_rects = tilemap.entity_collidable_rects(self.pos, self)
        for collidable_rect in collidable_rects:
            if entity_rect.colliderect(collidable_rect):
                # print("collide y", entity_rect, collidable_rect, self.frame_counter)
                if self.velocity.y > 0:
                    entity_rect.bottom = collidable_rect.top
                    self.collisions["bottom"] = True
                elif self.velocity.y < 0:
                    entity_rect.top = collidable_rect.bottom
                    self.collisions["top"] = True
                self.y = entity_rect.y
                
                self.velocity.y = 0
        




PlayerGroup = pygame.sprite.Group()
class Player(SolidEntity):
    def __init__(self, game_manager, pos: tuple[float, float], velocity: Velocity|None = None) -> None:
        super().__init__(game_manager, "player", pos, PLAYER_SIZE, velocity, PlayerGroup)
        self.movement:list[bool] = [False, False]
        self.movement_speed = 240
        self.can_jump = False
        
        self.flip = False
    
    def handle_event(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.movement[0] = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.movement[1] = True
            
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not self.can_jump:
                    return
                self.velocity.y = -721
                self.can_jump = False
        
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.movement[0] = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.movement[1] = False
            
    
    def update(self, dt: float):
        self.velocity.x = (-self.movement[0] + self.movement[1]) * self.movement_speed
        #Gravity velocity update
        self.velocity.y = min(self.velocity.y + 1000*dt, 1000)
        
        super().update(dt)
        if self.collisions["bottom"]:
            self.can_jump = True
        
        if self.movement[0] and (not self.movement[1]):
            self.flip = False
        elif (not self.movement[0]) and self.movement[1]:
            self.flip = True
        
    
    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        
        
        img = self.img()
        img = pygame.transform.flip(img, self.flip, False)
        screen.blit(img, (self.rect.x - offset[0], self.rect.y - offset[1]))


















