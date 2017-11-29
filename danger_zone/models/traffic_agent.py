import numpy as np

from danger_zone.parameters import TARGET_DELTA, MAP_WIDTH, MAP_HEIGHT
from danger_zone.util.vector_calculation import normalize, limit_length


class TrafficAgent:
    def __init__(self):
        self.position = np.array([MAP_WIDTH / 2.0, -10.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.has_reached_target = False

        self.max_speed = 2
        self.max_steering_force = 0.1
        self.movement_randomness = 5
        self.width = 10
        self.height = 10
        self.target = np.array([MAP_WIDTH / 2.0, MAP_HEIGHT + 10.0])

    def move(self):
        if self.has_reached_target:
            return

        self.calculate_target_force()

        self.velocity += self.acceleration
        self.velocity = limit_length(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

        self.evaluate_target_distance()

    def calculate_target_force(self):
        # Calculate direction of target
        desired_velocity = self.target - self.position
        # print(self.movement_randomness * np.random.rand(2))
        desired_velocity = normalize(desired_velocity)
        desired_velocity += self.movement_randomness * np.random.randn(2)
        desired_velocity = normalize(desired_velocity)

        desired_velocity *= self.max_speed

        # Calculate steering force
        steering_force = desired_velocity - self.velocity
        steering_force = limit_length(steering_force, self.max_steering_force)
        self.acceleration += steering_force

    def evaluate_target_distance(self):
        target_delta_vector = self.position - self.target
        if np.linalg.norm(target_delta_vector) <= TARGET_DELTA:
            self.has_reached_target = True
