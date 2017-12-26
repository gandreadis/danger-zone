import os

from danger_zone.map.tile_types import Tile

MAP_SIZE = 16
SPAWN_MARGIN = 3
FULL_SIZE = MAP_SIZE + SPAWN_MARGIN * 2
MAPS_DIRECTORY = "maps"


class Map:
    """Class representing a static traffic map."""

    @staticmethod
    def read_map_from_file(map_name):
        """
        Reads the map with given name from the corresponding file and returns a Map instance with its contents.

        :param map_name: The name of the map.
        :return: A Map instance loaded with the contents of the map file.
        """

        map_file = open(os.path.join(MAPS_DIRECTORY, map_name + ".dzone"), "r")
        lines = [l.strip() for l in map_file]
        map_file.close()
        return Map(lines[:FULL_SIZE])

    def __init__(self, map_rows):
        """
        Constructs an instance of this class.

        :param map_rows: A list of strings, where each string corresponds to a row of the map.
        """

        self.tiles = map_rows

        assert len(self.tiles) == FULL_SIZE, "Map should be {} tiles high".format(FULL_SIZE)
        for row in self.tiles:
            assert len(row) == FULL_SIZE, "Map should be {} tiles wide".format(FULL_SIZE)

    def get_tile(self, x, y):
        """
        Gets the tile character at the given coordinates.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: The tile character at that position.
        """

        if not self.is_on_map(x, y):
            return Tile.EMPTY

        return self.tiles[y + SPAWN_MARGIN][x + SPAWN_MARGIN]

    def find_all_occurrences_of_tile(self, tile):
        """
        Get all occurrences of the given tile character.

        :param tile: The tile character that this method should search for.
        :return: All occurrences of that tile.
        """

        occurrences = []
        for x in range(-SPAWN_MARGIN, MAP_SIZE + SPAWN_MARGIN):
            for y in range(-SPAWN_MARGIN, MAP_SIZE + SPAWN_MARGIN):
                if self.get_tile(x, y) == tile:
                    occurrences.append((x, y))

        return occurrences

    def is_on_map(self, x, y):
        """
        Checks whether the given coordinate is within the bounds of the map (including spawn margins).

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: `True` iff. the coordinate is on the map.
        """

        return -SPAWN_MARGIN <= x < MAP_SIZE + SPAWN_MARGIN and -SPAWN_MARGIN <= y < MAP_SIZE + SPAWN_MARGIN

    def is_on_main_map(self, x, y):
        """
        Checks whether the given coordinate is within the bounds of the main map (excluding spawn margins).

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: `True` iff. the coordinate is on the main map.
        """

        return 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE
