import math

import numpy as np
import shapely.affinity
import shapely.geometry

from danger_zone.parameters import TARGET_DELTA, MAP_WIDTH, MAP_HEIGHT, MINIMUM_AGENT_DISTANCE, AGENT_VISIBILITY_RANGE, \
    DANGER_LEVEL_VIEW_DISTANCE
from danger_zone.tile import Tile
from danger_zone.util.vector_calculation import normalize, limit_length, get_vector_angle


class TrafficAgent:
    def __init__(self):
        self.name = 'agent'
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

    def consider_danger_zones(self, scenario):
        if self.point_outside_of_viewport(self.position):
            return

        current_tile = scenario.get_tile(math.floor(self.position[0]), math.floor(self.position[1]))
        current_danger_level = Tile.get_danger_level(self.name, current_tile)
        if current_danger_level <= 0:
            return

        min_x, min_y = -2, -2
        min_danger_level = 1000

        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                point = self.position + np.array([DANGER_LEVEL_VIEW_DISTANCE * x, DANGER_LEVEL_VIEW_DISTANCE * y])
                if self.point_outside_of_viewport(point):
                    continue

                point_type = scenario.get_tile(math.floor(point[0]), math.floor(point[1]))
                point_level = Tile.get_danger_level(self.name, point_type)

                if point_level < min_danger_level:
                    min_danger_level = point_level
                    min_x, min_y = x, y

        if min_x != -2:
            lower_danger_force = np.array([DANGER_LEVEL_VIEW_DISTANCE * min_x, DANGER_LEVEL_VIEW_DISTANCE * min_y])
            lower_danger_force = normalize(lower_danger_force) * self.max_speed
            steering_force = lower_danger_force - self.velocity
            limit_length(steering_force * 3, self.max_steering_force)
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
            if self.point_outside_of_viewport(point):
                num_points_outside_viewport += 1

        return num_points_outside_viewport > 2

    def point_outside_of_viewport(self, point):
        return (point[0] < 0 or point[0] >= MAP_WIDTH) or (point[1] < 0 or point[1] >= MAP_HEIGHT)
