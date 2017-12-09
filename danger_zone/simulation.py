import numpy as np

from danger_zone.parameters import MAP_HEIGHT, PERCEPTION_DELAY
from danger_zone.util.traffic_agent_types import TRAFFIC_AGENT_TYPES

SCENARIOS = {
    "simple": {
        "spawn-delay": {
            "pedestrian": 15,
            "bicycle": 25,
            "car": 50,
        },
        "spawn-area": {
            "pedestrian": {"x": 0, "y": -50, "width": 120, "height": 50},
            "bicycle": {"x": 170, "y": -200, "width": 130, "height": 100},
            "car": {"x": 320, "y": -300, "width": 180, "height": 150},
        },
        "target-area": {
            "pedestrian": {"x": 0, "y": MAP_HEIGHT + 20, "width": 150, "height": 50},
            "bicycle": {"x": 170, "y": MAP_HEIGHT + 20, "width": 130, "height": 100},
            "car": {"x": 320, "y": MAP_HEIGHT + 20, "width": 180, "height": 150},
        },
    }
}


class Simulation:
    def __init__(self, scenario,limit) :
        self.scenario = scenario
        self.agents = []
        self.tick = 0
        self.collision_counter = 0
        self.maxtick = limit

    def on_tick(self):
        self.tick += 1
        #print(self.tick)
        self.spawn_agents("pedestrian")
        self.spawn_agents("bicycle")
        self.spawn_agents("car")

        for agent in self.agents:
            if self.tick % PERCEPTION_DELAY == 0:
                agent.separate_from_other_agents(self.agents, self.record_collision)
                agent.align(self.agents)

            agent.move()

            if agent.has_reached_target:
                self.agents.remove(agent)

    def record_collision(self):
        self.collision_counter += 1

    # noinspection PyTypeChecker
    def spawn_agents(self, type):
        if self.tick % SCENARIOS[self.scenario]["spawn-delay"][type] == 0:
            agent = TRAFFIC_AGENT_TYPES[type]()
            agent.position = self.select_random_point_in_rectangle(
                SCENARIOS[self.scenario]["spawn-area"][type])
            agent.target = self.select_random_point_in_rectangle(
                SCENARIOS[self.scenario]["target-area"][type])
            agent.cache_shape()
            self.agents.append(agent)

    def select_random_point_in_rectangle(self, rect):
        random_point = np.random.rand(2)
        random_point *= np.array([rect["width"], rect["height"]])
        random_point += np.array([rect["x"], rect["y"]])
        return random_point
