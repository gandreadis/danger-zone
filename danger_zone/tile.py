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

    @staticmethod
    def get_danger_level(agent_type, tile_type):
        if agent_type == "pedestrian":
            if tile_type == Tile.NEUTRAL:
                return 0
            elif tile_type == Tile.PEDESTRIAN:
                return 0
            elif tile_type == Tile.BICYCLE:
                return 1
            elif tile_type == Tile.CAR:
                return 2
            else:
                return -1
        elif agent_type == "bicycle":
            if tile_type == Tile.NEUTRAL:
                return 0
            elif tile_type == Tile.PEDESTRIAN:
                return 1
            elif tile_type == Tile.BICYCLE:
                return 0
            elif tile_type == Tile.CAR:
                return 2
            else:
                return -1
        elif agent_type == "car":
            if tile_type == Tile.NEUTRAL:
                return 0
            elif tile_type == Tile.PEDESTRIAN:
                return 2
            elif tile_type == Tile.BICYCLE:
                return 1
            elif tile_type == Tile.CAR:
                return 0
            else:
                return -1
