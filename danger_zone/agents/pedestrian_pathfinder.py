import math

from astar import AStar

from danger_zone.map.tile_types import Tile, PEDESTRIAN_ZONES


class PedestrianPathfinder(AStar):
    def __init__(self, map_state, pedestrian):
        self.map_state = map_state
        self.pedestrian = pedestrian

    def heuristic_cost_estimate(self, n1, n2):
        (x1, y1) = n1
        (x2, y2) = n2

        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        return 1

    def neighbors(self, node):
        x, y = node

        tiles = []
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            a = x + dx
            b = y + dy
            tile = self.map_state.get_dynamic_tile(a, b)

            if tile in PEDESTRIAN_ZONES or (tile == Tile.PEDESTRIAN_SPAWN and (a, b) == self.pedestrian.target):
                tiles.append((a, b))

        return tiles
