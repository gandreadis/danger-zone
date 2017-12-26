from danger_zone.map.map import MAP_SIZE
from danger_zone.map.tile_types import TILE_DIRECTIONS, Tile, NEUTRAL_ZONES

CAR_LENGTH = 3
CAR_WIDTH = 2


class Car:
    """Class representing a car agent."""

    def __init__(self, position, is_horizontal, map_state):
        """
        Constructs an instance of this class.

        :param position: The initial position of the agent (spawn-location).
        :param is_horizontal: Whether the car is horizontally oriented.
        :param map_state: The current MapState instance.
        """

        self.position = position
        self.spawn_position = position[:]
        self.in_spawn_area = True
        self.is_horizontal = is_horizontal
        self.map_state = map_state
        self.previous_direction = (0, 0)

    def move(self):
        """
        Evaluates the current tick state and makes a move if the tiles in front of it allow it.

        Looks first at the probe tile underneath it. From this, it derives its preferred direction. After having decided
        which way it wants to go, it checks the tiles immediately in front of it for other agents. If they are occupied,
        the agent does not move. If those are free, the agent checks the tiles two steps in front of it. If those are
        crosswalk (neutral) tiles and if they are occupied by pedestrians, no move is made. Else, the agent proceeds to
        move ahead.
        """

        x, y = self.position

        if self.in_spawn_area:
            if 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE:
                self.in_spawn_area = False

        preferred_direction = self.get_preferred_direction()

        if preferred_direction == (0, 0):
            return

        new_tiles = self.calculate_tiles_ahead(preferred_direction)

        if self.can_advance(new_tiles, preferred_direction):
            self.position = self.position[0] + preferred_direction[0] * 2, self.position[1] + preferred_direction[1] * 2
            self.update_cache_after_move(preferred_direction, new_tiles)
            self.previous_direction = preferred_direction[:]

    def get_preferred_direction(self):
        """
        Decides which direction to go next.

        If the agent is still in the spawn margin, it checks in which of the four margins it is situated. Else, it
        checks the map tile underneath the top-left corner for the tile direction.

        :return: The preferred direction of movement.
        """

        x, y = self.position

        current_map_tile = self.map_state.map.get_tile(*self.get_probe_location())

        if self.in_spawn_area:
            if x < 0:
                return 1, 0
            elif x >= MAP_SIZE:
                return -1, 0
            elif y < 0:
                return 0, 1
            elif y >= MAP_SIZE:
                return 0, -1
        elif current_map_tile in TILE_DIRECTIONS:
            return TILE_DIRECTIONS[current_map_tile]

        return 0, 0

    def get_probe_location(self):
        """
        Determines the coordinates of the probing location.

        This location should always be the front left tile, relative to the cars rotation.

        :return: The coordinates of the direction probing location.
        """

        probe_x, probe_y = self.position

        if self.previous_direction == (1, 0):
            probe_x += CAR_LENGTH - 1
        elif self.previous_direction == (0, 1):
            probe_y += CAR_LENGTH - 1

        return probe_x, probe_y

    def calculate_tiles_ahead(self, preferred_direction):
        """
        Calculates the coordinates of the tiles that lie immediately ahead.

        :param preferred_direction: The direction the car will be moving in.
        :return: The tiles that lie one or two hops ahead.
        """

        if preferred_direction == (1, 0):
            return (
                (self.position[0] + CAR_LENGTH, self.position[1]),
                (self.position[0] + CAR_LENGTH, self.position[1] + 1),
                (self.position[0] + CAR_LENGTH + 1, self.position[1]),
                (self.position[0] + CAR_LENGTH + 1, self.position[1] + 1),
            )
        elif preferred_direction == (-1, 0):
            return (
                (self.position[0] - 1, self.position[1]),
                (self.position[0] - 1, self.position[1] + 1),
                (self.position[0] - 2, self.position[1]),
                (self.position[0] - 2, self.position[1] + 1),
            )
        elif preferred_direction == (0, 1):
            return (
                (self.position[0], self.position[1] + CAR_LENGTH),
                (self.position[0] + 1, self.position[1] + CAR_LENGTH),
                (self.position[0], self.position[1] + CAR_LENGTH + 1),
                (self.position[0] + 1, self.position[1] + CAR_LENGTH + 1),
            )
        elif preferred_direction == (0, -1):
            return (
                (self.position[0], self.position[1] - 1),
                (self.position[0] + 1, self.position[1] - 1),
                (self.position[0], self.position[1] - 2),
                (self.position[0] + 1, self.position[1] - 2),
            )

    def calculate_crosswalk_check_tiles(self, preferred_direction):
        """
        Calculates the coordinates of the tiles that lie to either side of the car, for waiting pedestrians.

        :param preferred_direction: The direction the car will be moving in.
        :return: The tiles that lie to diagonally in front of it.
        """

        if preferred_direction == (1, 0):
            return (
                (self.position[0] + CAR_LENGTH, self.position[1] - 1),
                (self.position[0] + CAR_LENGTH, self.position[1] + 2),
                (self.position[0] + CAR_LENGTH + 1, self.position[1] - 1),
                (self.position[0] + CAR_LENGTH + 1, self.position[1] + 2),
            )
        elif preferred_direction == (-1, 0):
            return (
                (self.position[0] - 1, self.position[1] - 1),
                (self.position[0] - 1, self.position[1] + 2),
                (self.position[0] - 2, self.position[1] - 1),
                (self.position[0] - 2, self.position[1] + 2),
            )
        elif preferred_direction == (0, 1):
            return (
                (self.position[0] - 1, self.position[1] + CAR_LENGTH),
                (self.position[0] + 2, self.position[1] + CAR_LENGTH),
                (self.position[0] - 1, self.position[1] + CAR_LENGTH + 1),
                (self.position[0] + 2, self.position[1] + CAR_LENGTH + 1),
            )
        elif preferred_direction == (0, -1):
            return (
                (self.position[0] - 1, self.position[1] - 1),
                (self.position[0] + 2, self.position[1] - 1),
                (self.position[0] - 1, self.position[1] - 2),
                (self.position[0] + 2, self.position[1] - 2),
            )

    def can_advance(self, new_tiles, preferred_direction):
        """
        Determines whether the car can advance in the direction it wants to (based on occupancy of tiles ahead).

        :param new_tiles: The differential of new tiles that will be occupied.
        :param preferred_direction: The direction that the car should move in.
        :return: Whether the agent is allowed to move in this direction.
        """

        # If next tiles are beyond map, don't advance
        if not self.map_state.map.is_on_map(*new_tiles[0]) or not self.map_state.map.is_on_map(*new_tiles[1]):
            return False

        # If next tiles are occupied, don't advance
        if [self.map_state.get_tile_from_cache(*tile) != Tile.EMPTY for tile in new_tiles].count(True) > 0:
            return False

        # If the tiles are crosswalks and pedestrians are next to them, don't advance
        if [self.map_state.map.get_tile(x, y) in NEUTRAL_ZONES for x, y in new_tiles].count(True) > 0:
            crosswalk_checks = self.calculate_crosswalk_check_tiles(preferred_direction)
            if [self.map_state.get_tile_from_cache(*crosswalk_check) == Tile.PEDESTRIAN
                for crosswalk_check in crosswalk_checks].count(True) > 0:
                return False

        # Check three tiles ahead for pedestrians, in case of neutral zone
        three_tiles_ahead = (
            (new_tiles[2][0] + preferred_direction[0], new_tiles[2][1] + preferred_direction[1]),
            (new_tiles[3][0] + preferred_direction[0], new_tiles[3][1] + preferred_direction[1]),
        )

        for x, y in three_tiles_ahead:
            # If there is a pedestrian on a tile that's two steps ahead, don't advance
            if self.map_state.map.is_on_map(x, y) \
                    and self.map_state.map.get_tile(x, y) in NEUTRAL_ZONES \
                    and self.map_state.get_dynamic_tile(x, y) == Tile.PEDESTRIAN:
                return False

        return True

    def update_cache_after_move(self, direction_moved, new_tiles):
        """
        Updates the dynamic MapState tile cache following a successful move.

        :param direction_moved: The direction that the car has been determined to move in.
        :param new_tiles: The differential of new tiles that will be occupied.
        """

        self.map_state.set_tile_in_cache(*new_tiles[0], Tile.CAR)
        self.map_state.set_tile_in_cache(*new_tiles[1], Tile.CAR)

        if direction_moved == (1, 0):
            self.map_state.set_tile_in_cache(self.position[0], self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0], self.position[1] + 1, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1] + 1, Tile.EMPTY)
        elif direction_moved == (-1, 0):
            self.map_state.set_tile_in_cache(self.position[0] + CAR_LENGTH - 2, self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + CAR_LENGTH - 2, self.position[1] + 1, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + CAR_LENGTH - 2, self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + CAR_LENGTH - 2, self.position[1] + 1, Tile.EMPTY)
        elif direction_moved == (0, 1):
            self.map_state.set_tile_in_cache(self.position[0], self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0], self.position[1] + 1, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1] + 1, Tile.EMPTY)
        elif direction_moved == (0, -1):
            self.map_state.set_tile_in_cache(self.position[0], self.position[1] + CAR_LENGTH - 1, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1] + CAR_LENGTH - 1, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0], self.position[1] + CAR_LENGTH - 2, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1] + CAR_LENGTH - 2, Tile.EMPTY)

    def get_tiles(self):
        """
        Returns the tiles that this car occupies on the map.

        :return: The tiles that the agent occupies.
        """

        tiles = []
        for x in range(self.position[0],
                       self.position[0] + CAR_LENGTH if self.is_horizontal else self.position[0] + CAR_WIDTH):
            for y in range(self.position[1],
                           self.position[1] + CAR_WIDTH if self.is_horizontal else self.position[1] + CAR_LENGTH):
                tiles.append((x, y))

        return tiles

    def is_done(self):
        """
        Determines if the car has reached a spawn area that is not its original spawn area.

        :return: `True` iff. the car has reached another spawn area and can be removed from the map.
        """

        x, y = self.position

        if x <= -CAR_LENGTH \
                and (self.spawn_position[0] > 0 or y != self.spawn_position[1]) \
                and self.is_horizontal:
            return True
        elif x >= MAP_SIZE \
                and (self.spawn_position[0] < MAP_SIZE or y != self.spawn_position[1]) \
                and self.is_horizontal:
            return True
        elif y <= -CAR_LENGTH \
                and (self.spawn_position[1] > 0 or x != self.spawn_position[0]) \
                and not self.is_horizontal:
            return True
        elif y >= MAP_SIZE \
                and (self.spawn_position[1] < MAP_SIZE or x != self.spawn_position[0]) \
                and not self.is_horizontal:
            return True
        else:
            return False
