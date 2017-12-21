class IterationData:
    LABELS = [
        "pedestrians_that_reached_target",
        "cars_that_reached_target",
        "collisions",
        "failed_pedestrian_spawns",
        "failed_car_spawns",
    ]

    def __init__(self, pedestrians_that_reached_target, cars_that_reached_target, collisions, failed_pedestrian_spawns,
                 failed_car_spawns):
        self.pedestrians_that_reached_target = pedestrians_that_reached_target
        self.cars_that_reached_target = cars_that_reached_target
        self.collisions = collisions
        self.failed_pedestrian_spawns = failed_pedestrian_spawns
        self.failed_car_spawns = failed_car_spawns

    def to_list(self):
        return [getattr(self, column) for column in IterationData.LABELS]

    def update_target_reach_counts(self, pedestrians, cars):
        self.pedestrians_that_reached_target += pedestrians
        self.cars_that_reached_target += cars
