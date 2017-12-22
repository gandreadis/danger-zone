from danger_zone.map.map import MAP_SIZE
from danger_zone.map.tile_types import TILE_DIRECTIONS, Tile, NEUTRAL_ZONES

CAR_LENGTH = 3
CAR_WIDTH = 2


class Car:
    def __init__(self, position, is_horizontal, map_state):
        self.position = position
        self.spawn_position = position[:]
        self.in_spawn_area = True
        self.is_horizontal = is_horizontal
        self.map_state = map_state
        self.previous_direction = (0, 0)

    def move(self):
        x, y = self.position

        if self.in_spawn_area:
            if 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE:
                self.in_spawn_area = False

        probe_x, probe_y = x, y
        if self.previous_direction == (1, 0):
            probe_x += CAR_LENGTH - 1
        elif self.previous_direction == (0, 1):
            probe_y += CAR_LENGTH - 1

        current_map_tile = self.map_state.map.get_tile(probe_x, probe_y)
        preferred_direction = (0, 0)

        if self.in_spawn_area:
            if x < 0:
                preferred_direction = (1, 0)
            elif x >= MAP_SIZE:
                preferred_direction = (-1, 0)
            elif y < 0:
                preferred_direction = (0, 1)
            elif y >= MAP_SIZE:
                preferred_direction = (0, -1)
        elif current_map_tile in TILE_DIRECTIONS:
            preferred_direction = TILE_DIRECTIONS[current_map_tile]

        if preferred_direction == (0, 0):
            return

        new_tiles = self.calculate_tiles_ahead(preferred_direction)

        if self.can_advance(new_tiles, preferred_direction):
            self.position = self.position[0] + preferred_direction[0], self.position[1] + preferred_direction[1]
            self.update_cache_after_move(preferred_direction, new_tiles)
            self.previous_direction = preferred_direction[:]

    def calculate_tiles_ahead(self, preferred_direction):
        if preferred_direction == (1, 0):
            return (
                (self.position[0] + CAR_LENGTH, self.position[1]),
                (self.position[0] + CAR_LENGTH, self.position[1] + 1))
        elif preferred_direction == (-1, 0):
            return (
                (self.position[0] - 1, self.position[1]),
                (self.position[0] - 1, self.position[1] + 1))
        elif preferred_direction == (0, 1):
            return (
                (self.position[0], self.position[1] + CAR_LENGTH),
                (self.position[0] + 1, self.position[1] + CAR_LENGTH))
        elif preferred_direction == (0, -1):
            return (
                (self.position[0], self.position[1] - 1),
                (self.position[0] + 1, self.position[1] - 1))

    def can_advance(self, new_tiles, preferred_direction):
        # If next tiles are beyond map, don't advance
        if not self.map_state.map.is_on_map(*new_tiles[0]) or not self.map_state.map.is_on_map(*new_tiles[1]):
            return False

        # If next tiles are occupied, don't advance
        if self.map_state.get_tile_from_cache(*new_tiles[0]) != Tile.EMPTY \
                or self.map_state.get_tile_from_cache(*new_tiles[1]) != Tile.EMPTY:
            return False

        # Check two tiles ahead for pedestrians, in case of neutral zone
        two_tiles_ahead = (
            (new_tiles[0][0] + preferred_direction[0], new_tiles[0][1] + preferred_direction[1]),
            (new_tiles[1][0] + preferred_direction[0], new_tiles[1][1] + preferred_direction[1]),
        )

        for x, y in two_tiles_ahead:
            # If there is a pedestrian on a tile that's two steps ahead, don't advance
            if self.map_state.map.is_on_map(x, y) \
                    and self.map_state.map.get_tile(x, y) in NEUTRAL_ZONES \
                    and self.map_state.get_dynamic_tile(x, y) == Tile.PEDESTRIAN:
                return False

        return True

    def update_cache_after_move(self, direction_moved, new_tiles):
        self.map_state.set_tile_in_cache(*new_tiles[0], Tile.CAR)
        self.map_state.set_tile_in_cache(*new_tiles[1], Tile.CAR)

        if direction_moved == (1, 0):
            self.map_state.set_tile_in_cache(self.position[0], self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0], self.position[1] + 1, Tile.EMPTY)
        elif direction_moved == (-1, 0):
            self.map_state.set_tile_in_cache(self.position[0] + CAR_LENGTH - 1, self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + CAR_LENGTH - 1, self.position[1] + 1, Tile.EMPTY)
        elif direction_moved == (0, 1):
            self.map_state.set_tile_in_cache(self.position[0], self.position[1], Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1], Tile.EMPTY)
        elif direction_moved == (0, -1):
            self.map_state.set_tile_in_cache(self.position[0], self.position[1] + CAR_LENGTH - 1, Tile.EMPTY)
            self.map_state.set_tile_in_cache(self.position[0] + 1, self.position[1] + CAR_LENGTH - 1, Tile.EMPTY)

    def get_tiles(self):
        tiles = []
        for x in range(self.position[0],
                       self.position[0] + CAR_LENGTH if self.is_horizontal else self.position[0] + CAR_WIDTH):
            for y in range(self.position[1],
                           self.position[1] + CAR_WIDTH if self.is_horizontal else self.position[1] + CAR_LENGTH):
                tiles.append((x, y))

        return tiles

    def is_done(self):
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
