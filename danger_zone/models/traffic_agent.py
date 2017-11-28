import numpy as np

from danger_zone.util.vector_calculation import normalize, limit_length


class TrafficAgent:
    def __init__(self):
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

        self.max_speed = 2
        self.max_steering_force = 0.1
        self.width = 10
        self.height = 10
        self.target = np.array([100.0, 100.0])

    def move(self):
        self.calculate_target_force()

        self.velocity += self.acceleration
        self.velocity = limit_length(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

    def calculate_target_force(self):
        desired_velocity = self.target - self.position
        desired_velocity = normalize(desired_velocity)
        desired_velocity *= self.max_speed
        steering_force = desired_velocity - self.velocity
        steering_force = limit_length(steering_force, self.max_steering_force)
        self.acceleration += steering_force
