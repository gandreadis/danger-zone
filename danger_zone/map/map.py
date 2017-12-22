import os

MAP_SIZE = 16
SPAWN_MARGIN = 3
FULL_SIZE = MAP_SIZE + SPAWN_MARGIN * 2
MAPS_DIRECTORY = "maps"


class Map:
    @staticmethod
    def read_map_from_file(map_name):
        map_file = open(os.path.join(MAPS_DIRECTORY, map_name + ".txt"), "r")
        lines = [l.strip() for l in map_file]
        return Map(lines[:FULL_SIZE])

    def __init__(self, map_rows):
        self.tiles = map_rows

        assert len(self.tiles) == FULL_SIZE, "Map should be {} tiles high".format(FULL_SIZE)
        for row in self.tiles:
            assert len(row) == FULL_SIZE, "Map should be {} tiles wide".format(FULL_SIZE)

    def get_tile(self, x, y):
        return self.tiles[y + SPAWN_MARGIN][x + SPAWN_MARGIN]

    def find_all_occurrences_of_tile(self, tile):
        occurrences = []
        for x in range(-SPAWN_MARGIN, MAP_SIZE + SPAWN_MARGIN):
            for y in range(-SPAWN_MARGIN, MAP_SIZE + SPAWN_MARGIN):
                if self.get_tile(x, y) == tile:
                    occurrences.append((x, y))

        return occurrences

    def is_on_map(self, x, y):
        return -SPAWN_MARGIN <= x < MAP_SIZE + SPAWN_MARGIN and -SPAWN_MARGIN <= y < MAP_SIZE + SPAWN_MARGIN

    def is_on_main_map(self, x, y):
        return 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE
