import os

import numpy as np
from PIL import Image

from danger_zone.parameters import IMAGE_HEIGHT, IMAGE_WIDTH, SPAWN_AREA_WIDTH
from danger_zone.tile import Tile


class Scenario:
    SEARCH_AREAS = [
        [SPAWN_AREA_WIDTH, 0, IMAGE_WIDTH - SPAWN_AREA_WIDTH, SPAWN_AREA_WIDTH],  # N
        [0, SPAWN_AREA_WIDTH, SPAWN_AREA_WIDTH, IMAGE_HEIGHT - SPAWN_AREA_WIDTH],  # E
        [SPAWN_AREA_WIDTH, IMAGE_HEIGHT - SPAWN_AREA_WIDTH, IMAGE_WIDTH - SPAWN_AREA_WIDTH, IMAGE_HEIGHT],  # S
        [IMAGE_WIDTH - SPAWN_AREA_WIDTH, SPAWN_AREA_WIDTH, IMAGE_WIDTH, IMAGE_HEIGHT - SPAWN_AREA_WIDTH],  # W
    ]

    def __init__(self, name):
        self.name = name
        self.image_file_name = os.path.join('maps', self.name + '.png')
        self.image_data = None
        self.areas = {
            "car": [[], [], [], []],
            "bicycle": [[], [], [], []],
            "pedestrian": [[], [], [], []],
        }

    def read_from_file(self):
        img = Image.open(os.path.join('maps', self.name + '.png'))
        img = img.convert('RGB')

        width, height = img.size
        assert width == IMAGE_WIDTH and height == IMAGE_HEIGHT, 'Image should have standard map dimensions'

        image_data_raw = np.array(list(img.getdata()))
        self.image_data = np.reshape(image_data_raw, (-1, IMAGE_WIDTH, 3))

        img.close()

    def get_tile(self, x, y):
        return Tile.from_rgb(self.image_data[y + SPAWN_AREA_WIDTH, x + SPAWN_AREA_WIDTH])

    def detect_areas(self):
        for search_area_index in range(len(Scenario.SEARCH_AREAS)):
            search_area = Scenario.SEARCH_AREAS[search_area_index]

            for x in range(search_area[0], search_area[2]):
                for y in range(search_area[1], search_area[3]):

                    tile = self.get_tile(x - SPAWN_AREA_WIDTH, y - SPAWN_AREA_WIDTH)
                    if tile in (Tile.CAR, Tile.BICYCLE, Tile.PEDESTRIAN):
                        self.areas[Tile.to_type_string(tile)][search_area_index].append(
                            np.array([float(x) - SPAWN_AREA_WIDTH, float(y) - SPAWN_AREA_WIDTH]))

        for agent_type in self.areas.keys():
            self.areas[agent_type] = list(filter(lambda x: x != [], self.areas[agent_type]))
