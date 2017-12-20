import csv
import logging
import os
import pathlib

from danger_zone.iteration_data import IterationData


class CSVReporter:
    DIRECTORY_NAME = "simulation_data"

    def __init__(self, simulation_name):
        self.path_name = os.path.join(CSVReporter.DIRECTORY_NAME, simulation_name + ".csv")
        pathlib.Path(CSVReporter.DIRECTORY_NAME).mkdir(exist_ok=True)
        self.output_file = open(self.path_name, "w", newline="")
        self.output_writer = csv.writer(self.output_file)
        self.output_writer.writerow(IterationData.LABELS)

    def save_iteration_results(self, iteration_data):
        self.output_writer.writerow(iteration_data.to_list())

    def close(self):
        self.output_file.close()
        logging.info("Simulation data saved in '{}'".format(self.path_name))
