from danger_zone.models.traffic_agent import TrafficAgent
from danger_zone.parameters import PEDESTRIAN_WIDTH, PEDESTRIAN_HEIGHT, PEDESTRIAN_MAX_SPEED, \
    PEDESTRIAN_MAX_STEERING_FORCE, PEDESTRIAN_MOVEMENT_RANDOMNESS


class Pedestrian(TrafficAgent):
    def __init__(self):
        super().__init__()
        self.width = PEDESTRIAN_WIDTH
        self.height = PEDESTRIAN_HEIGHT
        self.max_speed = PEDESTRIAN_MAX_SPEED
        self.max_steering_force = PEDESTRIAN_MAX_STEERING_FORCE
        self.movement_randomness = PEDESTRIAN_MOVEMENT_RANDOMNESS
