

import pygame
pygame.init()
import pygame_gui
import better_pygame

from scenes import GameScene



class Game:
    def __init__(self, screen_size:tuple[int, int] = (1280, 720), frame_rate:float = 60) -> None:
        self.running = True
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self.dt = 0
        self.screen_size = screen_size
        
        self.screen = pygame.display.set_mode(screen_size)
        self.display = pygame.Surface((1920, 1080))
        
        self.scene_manager = better_pygame.SceneManager(self.screen_size)
        self.scenes = {"game":GameScene(self.scene_manager)}
        self.scene_manager.init_scenes(self.scenes, "game")
        
        
    
    def handle_event(self, event:pygame.Event):
        self.scene_manager.handle_event(event)
    
    def update(self, dt:float):
        self.scene_manager.update(dt)
    
    def draw(self):
        self.display.fill((0, 0, 0))
        
        self.scene_manager.draw(self.display)
        
        #Resize self.display to fit the screen
        resized_display = pygame.transform.scale(self.display, self.screen_size)
        self.screen.blit(resized_display, (0, 0))
        
        #Display screen
        pygame.display.update()
    
    
    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)
        
        
            self.update(self.dt)
            self.draw()
            
            self.dt = self.clock.tick(self.frame_rate) / 1000
            
            
            
if __name__ == "__main__":
    Game().run()