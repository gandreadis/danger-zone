import logging

from danger_zone.result_serialization.csv_reporter import CSVReporter
from danger_zone.simulation import Simulation


class Experiment:
    def __init__(self, args):
        self.args = args
        self.num_ticks = args.num_ticks
        self.num_iterations = args.num_iterations
        self.store_sequence = args.store_sequence
        self.simulation_name = args.simulation_name
        self.csv_reporter = CSVReporter(args.simulation_name)

    def run(self):
        for iteration in range(self.num_iterations):
            logging.info("Running simulation iteration {}/{}".format(iteration + 1, self.num_iterations))
            simulation = Simulation(self.args, iteration, self.csv_reporter)
            simulation.run()

        self.csv_reporter.close()
