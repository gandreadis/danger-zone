import numpy as np


class Tile:
    SPAWN_AREA = '-'
    PEDESTRIAN = 'P'
    BICYCLE = 'B'
    CAR = 'C'
    NEUTRAL = 'N'

    @staticmethod
    def from_rgb(rgb):
        if np.array_equal(rgb, [255, 0, 255]):
            return Tile.SPAWN_AREA
        elif np.array_equal(rgb, [255, 0, 0]):
            return Tile.PEDESTRIAN
        elif np.array_equal(rgb, [0, 255, 0]):
            return Tile.BICYCLE
        elif np.array_equal(rgb, [0, 0, 255]):
            return Tile.CAR
        elif np.array_equal(rgb, [255, 255, 0]):
            return Tile.NEUTRAL
        else:
            return ' '

    @staticmethod
    def to_type_string(tile_type):
        if tile_type == Tile.PEDESTRIAN:
            return "pedestrian"
        elif tile_type == Tile.BICYCLE:
            return "bicycle"
        elif tile_type == Tile.CAR:
            return "car"
