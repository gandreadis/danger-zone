import os

MAP_SIZE = 16
SPAWN_MARGIN = 3
FULL_SIZE = MAP_SIZE + SPAWN_MARGIN * 2
MAPS_DIRECTORY = "maps"


class Map:
    def __init__(self, map_rows):
        self.tiles = map_rows

        assert len(self.tiles) == FULL_SIZE, "Map should be {} tiles high".format(FULL_SIZE)
        for row in self.tiles:
            assert len(row) == FULL_SIZE, "Map should be {} tiles wide".format(FULL_SIZE)

    def get_tile(self, x, y):
        return self.tiles[y + SPAWN_MARGIN][x + SPAWN_MARGIN]

    @staticmethod
    def read_map_from_file(map_name):
        map_file = open(os.path.join(MAPS_DIRECTORY, map_name + ".txt"), "r")
        lines = [l.strip() for l in map_file]
        return Map(lines[:FULL_SIZE])
