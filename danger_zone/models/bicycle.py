from danger_zone.models.traffic_agent import TrafficAgent
from danger_zone.parameters import BICYCLE_HEIGHT, BICYCLE_WIDTH, \
    BICYCLE_MOVEMENT_RANDOMNESS, BICYCLE_MAX_STEERING_FORCE, BICYCLE_MAX_SPEED, BICYCLE_MAX_ACCELERATION


class Bicycle(TrafficAgent):
    def __init__(self):
        super().__init__()
        self.name = 'bicycle'
        self.width = BICYCLE_WIDTH
        self.height = BICYCLE_HEIGHT
        self.max_speed = BICYCLE_MAX_SPEED
        self.max_steering_force = BICYCLE_MAX_STEERING_FORCE
        self.max_acceleration = BICYCLE_MAX_ACCELERATION
        self.movement_randomness = BICYCLE_MOVEMENT_RANDOMNESS
