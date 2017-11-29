import numpy as np

from danger_zone.parameters import MAP_HEIGHT
from danger_zone.util.traffic_agent_types import TRAFFIC_AGENT_TYPES

SCENARIOS = {
    "simple": {
        "spawn-delay": {
            "pedestrian": 10,
            "bicycle": 20,
            "car": 40,
        },
        "spawn-area": {
            "pedestrian": {"x": 0, "y": -50, "width": 150, "height": 50},
            "bicycle": {"x": 150, "y": -200, "width": 150, "height": 100},
            "car": {"x": 300, "y": -300, "width": 200, "height": 150},
        },
        "target-area": {
            "pedestrian": {"x": 0, "y": MAP_HEIGHT, "width": 150, "height": 50},
            "bicycle": {"x": 150, "y": MAP_HEIGHT, "width": 150, "height": 100},
            "car": {"x": 300, "y": MAP_HEIGHT, "width": 200, "height": 150},
        },
    }
}


class Simulation:
    def __init__(self, scenario):
        self.scenario = scenario
        self.agents = []
        self.tick = 0
        self.collision_counter = 0

    def on_tick(self):
        self.tick += 1
        self.spawn_agents("pedestrian")
        self.spawn_agents("bicycle")
        self.spawn_agents("car")

        for agent in self.agents:
            agent.separate_from_other_agents(self.agents, self.record_collision)
            agent.align(self.agents)
            agent.move()

            if agent.has_reached_target:
                self.agents.remove(agent)

    def record_collision(self):
        self.collision_counter += 1

    def spawn_agents(self, type):
        # noinspection PyTypeChecker
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
