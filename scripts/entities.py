import pygame

from .velocity import Velocity, velocity_factory
from .constants import PLAYER_SIZE

class Entity(pygame.sprite.Sprite):
    def __init__(self, game_manager, entity_type:str, pos:tuple[float, float], size:tuple[float, float], velocity:Velocity|None, *groups) -> None:
        super().__init__(*groups)
        self.game_manager = game_manager
        self.entity_type = entity_type
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        if velocity is None:
            self.velocity = Velocity()
        else:
            self.velocity = velocity
    
    def handle_event(self, event:pygame.Event):...
    
    def update(self, dt:float):
        assert self.rect is not None
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
    
    def draw(self, screen:pygame.Surface):
        assert self.rect is not None
        screen.blit(self.game_manager.assets[self.entity_type], self.rect)

PlayerGroup = pygame.sprite.Group()
class Player(Entity):
    def __init__(self, game_manager, pos: tuple[float, float], velocity: Velocity|None = None) -> None:
        super().__init__(game_manager, "player", pos, PLAYER_SIZE, velocity, PlayerGroup)
    
    def update(self, dt: float):
        #Gravity velocity update
        self.velocity.y = min(self.velocity.y + 1000*dt, 1000)
        
        super().update(dt)
    
    # def draw(self, screen: pygame.Surface):
    #     assert self.rect is not None
    #     pygame.draw.rect(screen, (255, 0, 0), self.rect)
        


















