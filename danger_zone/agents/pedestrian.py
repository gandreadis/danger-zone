from danger_zone.agents.pedestrian_pathfinder import PedestrianPathfinder
from danger_zone.map.tile_types import Tile, PEDESTRIAN_ZONES


class Pedestrian:
    def __init__(self, position, target, map_state):
        self.position = position
        self.target = target
        self.map_state = map_state

    def move(self):
        pathfinder = PedestrianPathfinder(self.map_state, self)
        path = pathfinder.astar(self.position, self.target)

        if path is not None:
            path = list(path)
            if len(path) > 1:
                self.move_to_position(list(path)[1])
        else:
            self.move_to_random_neighbour()

    def move_to_random_neighbour(self):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        neighbour_tiles = [self.map_state.get_dynamic_tile(self.position[0] + dir[0], self.position[1] + dir[1])
                           for dir in directions]

        for i in range(len(neighbour_tiles)):
            if neighbour_tiles[i] in PEDESTRIAN_ZONES:
                self.move_to_position((self.position[0] + directions[i][0], self.position[1] + directions[i][1]))
                return

    def move_to_position(self, new_position):
        self.map_state.set_tile_in_cache(*self.position, Tile.EMPTY)
        self.map_state.set_tile_in_cache(*new_position, Tile.PEDESTRIAN)
        self.position = new_position

    def is_done(self):
        return self.position == self.target
