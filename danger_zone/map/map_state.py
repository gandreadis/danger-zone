import numpy as np

from danger_zone.agents.car import Car
from danger_zone.agents.pedestrian import Pedestrian
from danger_zone.map.map import FULL_SIZE, SPAWN_MARGIN
from danger_zone.map.tile_types import Tile


class MapState:
    """Class representing a map under simulation."""

    def __init__(self, static_map):
        """
        Constructs a new instance of this class.

        :param static_map: The Map instance to be used, defining the static structure of the map (i.e. the tiles).
        """

        self.map = static_map
        self.pedestrians = []
        self.cars = []
        self.spawn_tiles = {}
        self.tile_cache = None

        self.find_spawn_tiles()

    def move_all_agents(self):
        """Executes the `move()` action on all agents currently in simulation."""

        [pedestrian.move() for pedestrian in self.pedestrians]
        [car.move() for car in self.cars]

    def find_spawn_tiles(self):
        """Identifies all spawn tiles on the map and saves them in the corresponding internal lists."""

        self.spawn_tiles["pedestrian"] = self.map.find_all_occurrences_of_tile(Tile.PEDESTRIAN_SPAWN)
        self.spawn_tiles["car"] = []
        self.spawn_tiles["car"] += [(x, y, False)
                                    for x, y in self.map.find_all_occurrences_of_tile(Tile.CAR_SPAWN_VERTICAL)]
        self.spawn_tiles["car"] += [(x, y, True)
                                    for x, y in self.map.find_all_occurrences_of_tile(Tile.CAR_SPAWN_HORIZONTAL)]

    def spawn_agents(self, tick, pedestrian_spawn_delay, car_spawn_delay):
        """
        Spawns all agents of this tick cycle.

        :param tick: The current tick.
        :param pedestrian_spawn_delay: The delay between two spawns of pedestrians (enforced by a modulo operation).
        :param car_spawn_delay: The delay between two spawns of pedestrians (enforced by a modulo operation).
        :return: The number of failed pedestrian and car spawns.
        """

        failed_pedestrian_spawns = 0
        failed_car_spawns = 0

        if tick % pedestrian_spawn_delay == 0:
            free_spawn_tiles = [i for i in range(len(self.spawn_tiles["pedestrian"]))
                                if self.get_tile_from_cache(*self.spawn_tiles["pedestrian"][i]) == Tile.EMPTY]

            if len(free_spawn_tiles) == 0:
                failed_pedestrian_spawns = 1
            else:
                spawn_index = free_spawn_tiles[np.random.randint(len(free_spawn_tiles))]
                possible_target_indexes = [i for i in range(len(self.spawn_tiles["pedestrian"]))
                                           if not i == spawn_index]
                target_index = possible_target_indexes[np.random.randint(len(possible_target_indexes))]
                spawn_location = self.spawn_tiles["pedestrian"][spawn_index]
                target_location = self.spawn_tiles["pedestrian"][target_index]
                self.pedestrians.append(Pedestrian(spawn_location, target_location, self))

        if tick % car_spawn_delay == 0:
            free_spawn_tiles = [i for i in range(len(self.spawn_tiles["car"]))
                                if self.car_spawn_area_is_empty(*self.spawn_tiles["car"][i][:2])]
            if len(free_spawn_tiles) == 0:
                failed_car_spawns = 1
            else:
                spawn_index = free_spawn_tiles[np.random.randint(len(free_spawn_tiles))]
                spawn_location = self.spawn_tiles["car"][spawn_index][:2]
                self.cars.append(Car(spawn_location, self.spawn_tiles["car"][spawn_index][2], self))

        return failed_pedestrian_spawns, failed_car_spawns

    def remove_finished_agents(self):
        """
        Removes all agents that have reached a target.

        :return: The numbers of pedestrians and cars that have reached their targets.
        """

        pedestrians_that_reached_target = 0
        cars_that_reached_target = 0

        for pedestrian in self.pedestrians:
            if pedestrian.is_done():
                pedestrians_that_reached_target += 1
                self.pedestrians.remove(pedestrian)

        for car in self.cars:
            if car.is_done():
                cars_that_reached_target += 1
                self.cars.remove(car)

        return pedestrians_that_reached_target, cars_that_reached_target

    def rebuild_tile_cache(self):
        """Rebuilds the tile cache from scratch."""

        self.tile_cache = [[Tile.EMPTY for x in range(FULL_SIZE)] for y in range(FULL_SIZE)]

        for pedestrian in self.pedestrians:
            self.set_tile_in_cache(*pedestrian.position, Tile.PEDESTRIAN)
        for car in self.cars:
            for car_tile in car.get_tiles():
                self.set_tile_in_cache(*car_tile, Tile.CAR)

    def get_tile_from_cache(self, x, y):
        """
        Returns the given tile character from the cache.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: The tile character in cache at that location.
        """

        return self.tile_cache[y + SPAWN_MARGIN][x + SPAWN_MARGIN]

    def get_dynamic_tile(self, x, y):
        """
        Gets the effective tile at that location.

        If the dynamic map has an entry at that position, that tile is returned. Else, the static tile is returned.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: The tile at that location.
        """

        dynamic_tile = self.get_tile_from_cache(x, y)
        if dynamic_tile == Tile.EMPTY:
            return self.map.get_tile(x, y)
        else:
            return dynamic_tile

    def set_tile_in_cache(self, x, y, value):
        """
        Sets the given cache location to the given `value`.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :param value: The tile character to be set at that cache location.
        """
        self.tile_cache[y + SPAWN_MARGIN][x + SPAWN_MARGIN] = value

    def car_spawn_area_is_empty(self, x, y):
        """
        Checks whether all tiles of the given car spawn area are empty.

        :param x: The x coordinate.
        :param y: The y coordinate.
        :return: `True` iff. all tiles of the car spawn area are unoccupied.
        """

        is_horizontal = self.get_tile_from_cache(x, y) == Tile.CAR_SPAWN_HORIZONTAL
        dummy_car = Car((x, y), is_horizontal, self)

        for tile in dummy_car.get_tiles():
            if self.get_tile_from_cache(*tile) != Tile.EMPTY:
                return False

        return True
