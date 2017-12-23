class Tile:
    """Enum class mapping semantic tile meanings to their characters."""

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
    PEDESTRIAN = "x"
    EMPTY = "."


# All tile types that are neutral crosswalk areas (regardless of their direction)
NEUTRAL_ZONES = (
    Tile.NEUTRAL_ZONE_NORTH,
    Tile.NEUTRAL_ZONE_EAST,
    Tile.NEUTRAL_ZONE_SOUTH,
    Tile.NEUTRAL_ZONE_WEST,
)

# All tiles that pedestrians can walk on
PEDESTRIAN_ZONES = (
    Tile.PEDESTRIAN_ZONE,
    *NEUTRAL_ZONES
)

# Mapping from tiles to their direction vectors
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
