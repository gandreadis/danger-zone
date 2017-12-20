import logging

from danger_zone.simulation import Simulation


class Experiment:
    def __init__(self, num_ticks, num_iterations, store_sequence, simulation_name):
        self.num_ticks = num_ticks
        self.num_iterations = num_iterations
        self.store_sequence = store_sequence
        self.simulation_name = simulation_name

    def run(self):
        for iteration in range(self.num_iterations):
            logging.info("Running simulation iteration {}/{}".format(iteration + 1, self.num_iterations))
            simulation = Simulation(self.num_ticks, self.store_sequence, self.simulation_name, iteration)
            simulation.run()
