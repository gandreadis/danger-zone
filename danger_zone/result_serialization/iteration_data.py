class IterationData:
    """Class representing one row of simulation metric data."""

    LABELS = [
        "pedestrians_that_reached_target",
        "cars_that_reached_target",
        "collisions",
        "failed_pedestrian_spawns",
        "failed_car_spawns",
    ]

    def __init__(self, pedestrians_that_reached_target, cars_that_reached_target, collisions, failed_pedestrian_spawns,
                 failed_car_spawns):
        """
        Constructs an instance of this class.

        :param pedestrians_that_reached_target: Number of pedestrians that reached their target.
        :param cars_that_reached_target: Number of cars that reached their target.
        :param collisions: Number of collisions.
        :param failed_pedestrian_spawns: Number of failed pedestrian spawns.
        :param failed_car_spawns: Number of failed car spawns.
        """

        self.pedestrians_that_reached_target = pedestrians_that_reached_target
        self.cars_that_reached_target = cars_that_reached_target
        self.collisions = collisions
        self.failed_pedestrian_spawns = failed_pedestrian_spawns
        self.failed_car_spawns = failed_car_spawns

    def to_list(self):
        """
        Generates a list representation of this data instance, in consistent order of columns.

        :return: A list representation of this data instance.
        """
        return [getattr(self, column) for column in IterationData.LABELS]

    def update_target_reach_counts(self, pedestrians, cars):
        """
        Updates the stored target reach counts with the new pedestrian and car counts.

        :param pedestrians: New diff count of pedestrians reaching their target.
        :param cars: New diff count of cars reaching their target.
        """

        self.pedestrians_that_reached_target += pedestrians
        self.cars_that_reached_target += cars

    def update_failed_spawn_counts(self, pedestrians, cars):
        """
        Updates the stored failed spawn counts with the new pedestrian and car counts.

        :param pedestrians: New diff count of pedestrians failing to spawn.
        :param cars: New diff count of cars failing to spawn.
        """

        self.failed_pedestrian_spawns += pedestrians
        self.failed_car_spawns += cars
