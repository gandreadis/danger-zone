from danger_zone.map.map import MAP_SIZE
from danger_zone.map.tile_types import TILE_DIRECTIONS

CAR_LENGTH = 3
CAR_WIDTH = 2


class Car:
    def __init__(self, position, is_horizontal, map_state):
        self.position = position
        self.spawn_position = position[:]
        self.in_spawn_area = True
        self.is_horizontal = is_horizontal
        self.map_state = map_state

    def move(self):
        x, y = self.position

        if self.in_spawn_area:
            if 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE:
                self.in_spawn_area = False

        current_map_tile = self.map_state.map.get_tile(x, y)
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

        self.position = self.position[0] + preferred_direction[0], self.position[1] + preferred_direction[1]

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
                and (self.spawn_position[1] > 0 or y != self.spawn_position[1]) \
                and self.is_horizontal:
            return True
        elif x >= MAP_SIZE \
                and (self.spawn_position[1] < MAP_SIZE or y != self.spawn_position[1]) \
                and self.is_horizontal:
            return True
        elif y <= -CAR_LENGTH \
                and (self.spawn_position[0] > 0 or x != self.spawn_position[0]) \
                and not self.is_horizontal:
            return True
        elif y >= MAP_SIZE \
                and (self.spawn_position[0] < MAP_SIZE or x != self.spawn_position[0]) \
                and not self.is_horizontal:
            return True
        else:
            return False
