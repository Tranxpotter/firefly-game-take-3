import PIL
from PIL import Image

with Image.open("data/images/entities/player.png") as img:
    resized = img.resize((80, 80))
    resized.save("data/images/entities/player_resized.png")