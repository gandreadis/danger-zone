from enum import Enum


class Tile(Enum):
    CAR_ZONE_NORTH = "^"
    CAR_ZONE_EAST = ">"
    CAR_ZONE_SOUTH = "v"
    CAR_ZONE_WEST = "<"
    PEDESTRIAN_ZONE = "o"
    NEUTRAL_ZONE_NORTH = "w"
    NEUTRAL_ZONE_EAST = "d"
    NEUTRAL_ZONE_SOUTH = "s"
    NEUTRAL_ZONE_WEST = "a"
    CAR_SPAWN_NORTH = "i"
    CAR_SPAWN_EAST = "l"
    CAR_SPAWN_SOUTH = "k"
    CAR_SPAWN_WEST = "j"
    PEDESTRIAN_SPAWN = "p"
    CAR = "|"
    PEDESTRIAN = "x"
    EMPTY = "."
