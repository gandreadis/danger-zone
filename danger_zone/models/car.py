from danger_zone.models.traffic_agent import TrafficAgent
from danger_zone.parameters import CAR_WIDTH, CAR_HEIGHT, CAR_MAX_SPEED, \
    CAR_MAX_STEERING_FORCE, CAR_MOVEMENT_RANDOMNESS, CAR_MAX_ACCELERATION


class Car(TrafficAgent):
    def __init__(self):
        super().__init__()
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.max_speed = CAR_MAX_SPEED
        self.max_steering_force = CAR_MAX_STEERING_FORCE
        self.max_acceleration = CAR_MAX_ACCELERATION
        self.movement_randomness = CAR_MOVEMENT_RANDOMNESS
