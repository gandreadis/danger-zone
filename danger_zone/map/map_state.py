import numpy as np

from danger_zone.agents.car import Car
from danger_zone.agents.pedestrian import Pedestrian
from danger_zone.map.tile_types import Tile


class MapState:
    def __init__(self, map):
        self.map = map
        self.pedestrians = []
        self.cars = []
        self.spawn_tiles = {}

        self.find_spawn_tiles()

    def find_spawn_tiles(self):
        self.spawn_tiles["pedestrian"] = self.map.find_all_occurrences_of_tile(Tile.PEDESTRIAN_SPAWN)
        self.spawn_tiles["car"] = []
        self.spawn_tiles["car"] += [(x, y, False)
                                    for x, y in self.map.find_all_occurrences_of_tile(Tile.CAR_SPAWN_VERTICAL)]
        self.spawn_tiles["car"] += [(x, y, True)
                                    for x, y in self.map.find_all_occurrences_of_tile(Tile.CAR_SPAWN_HORIZONTAL)]

    def spawn_agents(self, tick, pedestrian_spawn_delay, car_spawn_delay):
        if tick % pedestrian_spawn_delay == 0:
            spawn_index = np.random.randint(len(self.spawn_tiles["pedestrian"]))
            possible_target_indexes = [i for i in range(len(self.spawn_tiles["pedestrian"])) if not i == spawn_index]
            target_index = possible_target_indexes[np.random.randint(len(possible_target_indexes))]
            spawn_location = self.spawn_tiles["pedestrian"][spawn_index]
            target_location = self.spawn_tiles["pedestrian"][target_index]
            self.pedestrians.append(Pedestrian(spawn_location, target_location))

        if tick % car_spawn_delay == 0:
            spawn_index = np.random.randint(len(self.spawn_tiles["car"]))
            spawn_location = self.spawn_tiles["car"][spawn_index][:2]
            self.cars.append(Car(spawn_location, self.spawn_tiles["car"][spawn_index][2]))

    def remove_finished_agents(self):
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
