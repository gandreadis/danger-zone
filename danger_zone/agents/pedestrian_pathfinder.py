import math

from astar import AStar

from danger_zone.map.tile_types import Tile, PEDESTRIAN_ZONES


class PedestrianPathfinder(AStar):
    """Instance of an AStar pathfinding implementation, with custom heuristics and neighbour logic."""

    def __init__(self, map_state, pedestrian):
        """
        Constructs an instance of this class.

        :param map_state: The MapState instance to use.
        :param pedestrian: The pedestrian that this pathfinder should find a path for.
        """

        self.map_state = map_state
        self.pedestrian = pedestrian

    def heuristic_cost_estimate(self, location1, location2):
        """
        Returns a estimate of the cost to get from `location1` to `location2`.

        :param location1: The first location.
        :param location2: The second location.
        :return: An estimate of the cost to get from the one to the other (computed as a straight line).
        """

        (x1, y1) = location1
        (x2, y2) = location2

        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, location1, location2):
        """
        Returns the distance between two neighbours.

        As all neighbours are equally spaced and accessible, all tiles have the same distance to all their immediate
        neighbours.

        :param location1: The first location.
        :param location2: The second location.
        :return: `1`.
        """

        return 1

    def neighbors(self, node):
        """
        Determines the reachable neighbors of the given node.

        :param node: The node that the neighbors should be retrieved for.
        :return: All neighboring tiles (in directions NESW).
        """

        x, y = node

        tiles = []
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            a = x + dx
            b = y + dy
            tile = self.map_state.get_dynamic_tile(a, b)

            if tile in PEDESTRIAN_ZONES or (tile == Tile.PEDESTRIAN_SPAWN and (a, b) == self.pedestrian.target):
                tiles.append((a, b))

        return tiles
