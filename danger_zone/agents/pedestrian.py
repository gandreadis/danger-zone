import math

import numpy as np

from danger_zone.agents.pedestrian_pathfinder import PedestrianPathfinder
from danger_zone.map.tile_types import Tile, PEDESTRIAN_ZONES


class Pedestrian:
    """Class representing a pedestrian agent."""

    def __init__(self, position, target, map_state):
        """
        Constructs a new instance of this class.

        :param position: The initial (spawn) position.
        :param target: The target position of this agent.
        :param map_state: The current MapState instance.
        """

        self.position = position
        self.target = target
        self.map_state = map_state

    def move(self):
        """
        Evaluates the current map tick state and tries to make a move.

        Instructs a pathfinding algorithm to find a good path to its target. If that algorithm finds no path (due to
        other agents being in the way), it falls back on a best-effort basis, making an arbitrary move (in the general
        direction of the target).
        """

        pathfinder = PedestrianPathfinder(self.map_state, self)
        path = pathfinder.astar(self.position, self.target)

        if path is not None:
            path = list(path)
            if len(path) > 1:
                self.move_to_position(list(path)[1])
        else:
            # Choose neighbour that goes roughly into direction of the goal if A* finds no path, to avoid deadlock
            self.move_to_best_effort_neighbour()

    def move_to_best_effort_neighbour(self):
        """Moves to a neighbour that is either arbitrarily chosen or moves closest to the target."""

        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        neighbour_tile_positions = [(self.position[0] + dir[0], self.position[1] + dir[1]) for dir in directions]

        if np.random.randint(0, 2) == 0:
            # Sort by closeness to target (pick best-effort first)
            neighbour_tile_positions = sorted(neighbour_tile_positions,
                                              key=lambda tile: math.hypot(self.target[0] - tile[0],
                                                                          self.target[1] - tile[1]))
        neighbour_tiles = [self.map_state.get_dynamic_tile(*pos) for pos in neighbour_tile_positions]

        for i in range(len(neighbour_tiles)):
            if neighbour_tiles[i] in PEDESTRIAN_ZONES:
                self.move_to_position(neighbour_tile_positions[i])
                return

    def move_to_position(self, new_position):
        """
        Moves to the given position and updates the MapState cache appropriately.

        :param new_position: The position to move to.
        """

        self.map_state.set_tile_in_cache(*self.position, Tile.EMPTY)
        self.map_state.set_tile_in_cache(*new_position, Tile.PEDESTRIAN)
        self.position = new_position

        assert self.map_state.map.is_on_main_map(*new_position) \
               or self.map_state.map.get_tile(*new_position) == Tile.PEDESTRIAN_SPAWN, \
            "Pedestrian has left the board"

    def is_done(self):
        """
        Determines whether the agent has reached its target.

        :return: `True` iff. the agent has reached its target (and can thus be removed from the map).
        """

        return self.position == self.target
