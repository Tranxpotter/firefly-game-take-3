import os
import pygame

BASE_IMAGE_PATH = "data/images/"

def load_image(path:str, color_key:tuple[int, int, int]|None = None) -> pygame.Surface:
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    if color_key is not None:
        img.set_colorkey(color_key)
    return img