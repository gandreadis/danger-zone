from danger_zone.map.map import MAP_SIZE

CAR_LENGTH = 3
CAR_WIDTH = 2


class Car:
    def __init__(self, position, is_horizontal):
        self.position = position
        self.spawn_position = position[:]
        self.is_horizontal = is_horizontal

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
                and (self.spawn_position[1] >= MAP_SIZE or y != self.spawn_position[1]) \
                and self.is_horizontal:
            return True
        elif x >= MAP_SIZE \
                and (self.spawn_position[1] < 0 or y != self.spawn_position[1]) \
                and self.is_horizontal:
            return True
        elif y <= -CAR_LENGTH \
                and (self.spawn_position[0] >= MAP_SIZE or x != self.spawn_position[0]) \
                and not self.is_horizontal:
            return True
        elif y >= MAP_SIZE \
                and (self.spawn_position[0] < 0 or x != self.spawn_position[0]) \
                and not self.is_horizontal:
            return True
        else:
            return False
