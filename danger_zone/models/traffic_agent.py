import numpy as np
import shapely.affinity
import shapely.geometry

from danger_zone.parameters import TARGET_DELTA, MAP_WIDTH, MAP_HEIGHT, MINIMUM_AGENT_DISTANCE, AGENT_VISIBILITY_RANGE
from danger_zone.util.vector_calculation import normalize, limit_length, get_vector_angle


class TrafficAgent:
    def __init__(self):
        self.position = np.array([MAP_WIDTH / 2.0, -10.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.has_reached_target = False
        self.shape = None

        self.max_speed = 2
        self.max_steering_force = 0.1
        self.movement_randomness = 5
        self.max_acceleration = 1
        self.width = 10
        self.height = 10
        self.target = np.array([MAP_WIDTH / 2.0, MAP_HEIGHT + 10.0])

    def cache_shape(self):
        self.shape = shapely.geometry.box(-self.width / 2.0, -self.height / 2.0, self.width / 2.0, self.height / 2.0)
        self.shape = shapely.affinity.rotate(self.shape, get_vector_angle(self.velocity))
        self.shape = shapely.affinity.translate(self.shape, self.position[0], self.position[1])

    def separate_from_other_agents(self, agents, record_collision):
        if self.is_outside_of_viewport():
            return

        separation_sum = np.array([0.0, 0.0])
        num_close_agents = 0

        for agent in agents:
            if self == agent:
                continue

            if agent.shape.intersects(self.shape):
                record_collision()
            elif agent.shape.distance(self.shape) < MINIMUM_AGENT_DISTANCE:
                diff = self.position - agent.position
                diff = normalize(diff)
                separation_sum += diff
                num_close_agents += 1

        if num_close_agents > 0:
            separation_sum /= num_close_agents
            separation_sum = normalize(separation_sum) * self.max_speed
            steering_force = separation_sum - self.velocity
            limit_length(steering_force * 3, self.max_steering_force)
            self.acceleration += steering_force

    def align(self, agents):
        velocity_sum = np.array([0.0, 0.0])
        num_close_agents = 0

        for agent in agents:
            if self == agent:
                continue

            agent_dist = np.linalg.norm(agent.position - self.position)
            if 0 < agent_dist < AGENT_VISIBILITY_RANGE:
                velocity_sum += agent.velocity
                num_close_agents += 1

        if num_close_agents > 0 and velocity_sum[0] > 0 and velocity_sum[1] > 0:
            velocity_sum /= num_close_agents
            velocity_sum = normalize(velocity_sum) * self.max_speed
            steering_force = velocity_sum - self.velocity
            limit_length(steering_force * 0.1, self.max_steering_force)
            self.acceleration += steering_force

    def move(self):
        if self.has_reached_target:
            return

        self.calculate_target_force()

        self.acceleration = limit_length(self.acceleration, self.max_acceleration)
        self.velocity += self.acceleration
        self.velocity = limit_length(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

        self.evaluate_target_distance()
        self.cache_shape()

    def calculate_target_force(self):
        # Calculate direction of target
        desired_velocity = self.target - self.position
        desired_velocity = normalize(desired_velocity)
        desired_velocity += self.movement_randomness * np.random.randn(2)
        desired_velocity = normalize(desired_velocity)

        desired_velocity *= self.max_speed

        # Calculate steering force
        steering_force = desired_velocity - self.velocity
        steering_force = limit_length(steering_force * 2, self.max_steering_force)
        self.acceleration += steering_force

    def evaluate_target_distance(self):
        target_delta_vector = self.position - self.target
        if np.linalg.norm(target_delta_vector) <= TARGET_DELTA:
            self.has_reached_target = True

    def is_outside_of_viewport(self):
        num_points_outside_viewport = 0
        points = list(zip(*self.shape.exterior.coords.xy))

        for point in points:
            if (point[0] < 0 or point[0] > MAP_WIDTH) and (point[1] < 0 or point[1] > MAP_HEIGHT):
                num_points_outside_viewport += 1

        return num_points_outside_viewport > 2
