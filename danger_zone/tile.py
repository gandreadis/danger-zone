class Tile:
    SPAWN_AREA = '-'
    PEDESTRIAN = 'P'
    BICYCLE = 'B'
    CAR = 'C'
    NEUTRAL = 'N'

    @staticmethod
    def from_rgb(rgb):
        if rgb == [255, 0, 255]:
            return Tile.SPAWN_AREA
        elif rgb == [255, 0, 0]:
            return Tile.PEDESTRIAN
        elif rgb == [0, 255, 0]:
            return Tile.BICYCLE
        elif rgb == [0, 0, 255]:
            return Tile.CAR
        elif rgb == [255, 255, 0]:
            return Tile.NEUTRAL
        else:
            return ' '
