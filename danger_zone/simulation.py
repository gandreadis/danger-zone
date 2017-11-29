from danger_zone.models.bicycle import Bicycle
from danger_zone.models.pedestrian import Pedestrian


class Simulation:
    def __init__(self):
        self.agents = [Pedestrian(), Pedestrian(), Bicycle()]
        self.tick = 0

    def on_tick(self):
        for agent in self.agents:
            agent.move()

        self.tick += 1
