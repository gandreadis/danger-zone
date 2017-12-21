import json
import logging
import os
import pathlib


class Trace:
    DIRECTORY_NAME = "simulation_traces"

    def __init__(self, simulation_name, iteration):
        self.simulation_name = simulation_name
        self.iteration = iteration
        self.file_path = os.path.join(Trace.DIRECTORY_NAME,
                                      "{}_{}.json".format(self.simulation_name, self.iteration))

        self.tick_states = []

    def add_tick_state(self, map_state):
        new_tick_state = {
            "pedestrians": [{"x": pedestrian.position[0], "y": pedestrian.position[1]}
                            for pedestrian in map_state.pedestrians],
            "cars": [{"x": car.position[0], "y": car.position[1], "is_horizontal": car.is_horizontal}
                     for car in map_state.cars],
        }
        self.tick_states.append(new_tick_state)

    def save_and_close(self):
        pathlib.Path(Trace.DIRECTORY_NAME).mkdir(exist_ok=True)
        with open(self.file_path, 'w') as data_file:
            json.dump(self.tick_states, data_file)
        logging.info("Trace data saved in '{}'".format(self.file_path))

    def read_trace_from_file(self):
        with open(self.file_path, 'r') as data_file:
            return json.load(data_file)
