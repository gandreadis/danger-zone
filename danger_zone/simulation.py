from danger_zone.models.traffic_agent import TrafficAgent


class Simulation:
    def __init__(self):
        self.agents = [TrafficAgent()]
        self.tick = 0

    def on_tick(self):
        for agent in self.agents:
            agent.move()

        self.tick += 1
