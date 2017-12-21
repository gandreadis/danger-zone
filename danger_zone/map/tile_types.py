class Tile:
    CAR_ZONE_NORTH = "^"
    CAR_ZONE_EAST = ">"
    CAR_ZONE_SOUTH = "v"
    CAR_ZONE_WEST = "<"
    PEDESTRIAN_ZONE = "o"
    NEUTRAL_ZONE_NORTH = "w"
    NEUTRAL_ZONE_EAST = "d"
    NEUTRAL_ZONE_SOUTH = "s"
    NEUTRAL_ZONE_WEST = "a"
    CAR_SPAWN_VERTICAL = "i"
    CAR_SPAWN_HORIZONTAL = "k"
    PEDESTRIAN_SPAWN = "p"
    CAR = "|"
    CAR_FUTURE = "$"
    PEDESTRIAN = "x"
    PEDESTRIAN_FUTURE = "%"
    EMPTY = "."


TILE_DIRECTIONS = {
    Tile.CAR_ZONE_NORTH: (0, -1),
    Tile.CAR_ZONE_EAST: (-1, 0),
    Tile.CAR_ZONE_SOUTH: (0, 1),
    Tile.CAR_ZONE_WEST: (1, 0),
    Tile.NEUTRAL_ZONE_NORTH: (0, -1),
    Tile.NEUTRAL_ZONE_EAST: (-1, 0),
    Tile.NEUTRAL_ZONE_SOUTH: (0, 1),
    Tile.NEUTRAL_ZONE_WEST: (1, 0),
}
