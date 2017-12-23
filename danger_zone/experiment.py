import logging

from danger_zone.result_serialization.csv_reporter import CSVReporter
from danger_zone.simulation import Simulation


class Experiment:
    """Class representing an experiment, consisting of multiple simulation runs."""

    def __init__(self, args):
        """
        Constructs an instance of this class.

        :param args: The parsed commandline arguments passed to this program.
        """

        self.args = args
        self.num_iterations = args.num_iterations
        self.csv_reporter = CSVReporter(args)

    def run(self):
        """Runs the experiment."""

        for iteration in range(self.num_iterations):
            logging.info("Running simulation iteration {}/{}".format(iteration + 1, self.num_iterations))
            simulation = Simulation(self.args, iteration, self.csv_reporter)
            simulation.run()

        self.csv_reporter.close()
