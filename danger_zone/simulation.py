import numpy as np

from danger_zone.models.bicycle import Bicycle
from danger_zone.models.car import Car
from danger_zone.models.pedestrian import Pedestrian
from danger_zone.parameters import PERCEPTION_DELAY
from danger_zone.scenario import Scenario
from danger_zone.util.traffic_agent_types import TRAFFIC_AGENT_TYPES


class Simulation:
    def __init__(self, setup, limit):
        self.setup = setup
        self.scenario = Scenario(setup["scenario-name"])
        self.scenario.read_from_file()
        self.scenario.detect_areas()

        self.agents = []
        self.tick = 0
        self.collision_counter = 0
        self.max_tick = limit
        self.pedestrians_through = 0
        self.bicycles_through = 0
        self.cars_through = 0

    def on_tick(self):
        self.tick += 1
        self.spawn_agents("pedestrian")
        self.spawn_agents("bicycle")
        self.spawn_agents("car")

        for agent in self.agents:
            if self.tick % PERCEPTION_DELAY == 0:
                agent.separate_from_other_agents(self.agents, self.record_collision)
                agent.align(self.agents)
                agent.consider_danger_zones(self.scenario)

            agent.move()

            if agent.has_reached_target:
                self.agents.remove(agent)
                if isinstance(agent, Pedestrian):
                    self.pedestrians_through += 1
                if isinstance(agent, Bicycle):
                    self.bicycles_through += 1
                if isinstance(agent, Car):
                    self.cars_through += 1

    def record_collision(self):
        self.collision_counter += 1

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def spawn_agents(self, type):
        if self.tick % self.setup["spawn-delay"][type] == 0:
            agent = TRAFFIC_AGENT_TYPES[type]()
            spawn_index = np.random.randint(0, len(self.scenario.areas[type]))
            target_index = (spawn_index + np.random.randint(1, len(self.scenario.areas[type]))) % len(
                self.scenario.areas[type])

            agent.position = self.select_random_point_in_area(self.scenario.areas[type][spawn_index])
            agent.target = self.select_random_point_in_area(self.scenario.areas[type][target_index])
            agent.cache_shape()
            self.agents.append(agent)

    def select_random_point_in_area(self, area):
        return area[np.random.randint(0, len(area))]
