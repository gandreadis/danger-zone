import os

from PIL import Image

from danger_zone.parameters import IMAGE_HEIGHT, IMAGE_WIDTH
from danger_zone.tile import Tile


class Scenario:
    def __init__(self, name):
        self.name = name
        self.pixels = ''

    def read_from_file(self):
        img = Image.open(os.path.join('maps', self.name + '.png'))
        img = img.convert('RGB')

        width, height = img.size
        assert width == IMAGE_WIDTH and height == IMAGE_HEIGHT, 'Image should have standard map dimensions'

        pixel_data = list(img.getdata())
        for pixel in pixel_data:
            self.pixels += Tile.from_rgb(pixel)

        img.close()

    def get_tile(self, x, y):
        return self.pixels[y * IMAGE_WIDTH + x]
