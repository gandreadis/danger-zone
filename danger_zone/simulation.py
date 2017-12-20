import time

import progressbar


class Simulation:
    def __init__(self, num_ticks, store_sequence, simulation_name, iteration):
        self.num_ticks = num_ticks
        self.store_sequence = store_sequence
        self.simulation_name = simulation_name
        self.iteration = iteration

    def run(self):
        bar = progressbar.ProgressBar()
        for tick in bar(range(self.num_ticks)):
            time.sleep(0.1)
