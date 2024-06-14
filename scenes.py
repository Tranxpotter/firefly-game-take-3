from pygame import Event, Surface
from better_pygame import Scene

from scripts.game_manager import GameManager


class GameScene(Scene):
    def __init__(self, scene_manager) -> None:
        super().__init__(scene_manager)
        self.game_manager = GameManager()
    
    def handle_event(self, event: Event):
        self.game_manager.handle_event(event)
    
    def update(self, dt: float):
        self.game_manager.update(dt)
    
    def draw(self, screen: Surface):
        self.game_manager.draw(screen)