import progressbar

from danger_zone.map.map import Map
from danger_zone.map.map_state import MapState
from danger_zone.result_serialization.iteration_data import IterationData
from danger_zone.result_serialization.trace import Trace


class Simulation:
    def __init__(self, args, iteration, csv_reporter):
        self.num_ticks = args.num_ticks
        self.store_sequence = args.store_sequence
        self.simulation_name = args.simulation_name
        self.pedestrian_spawn_delay = args.pedestrian_spawn_delay
        self.car_spawn_delay = args.car_spawn_delay
        self.iteration = iteration
        self.csv_reporter = csv_reporter

        self.map = Map.read_map_from_file(self.simulation_name)
        self.map_state = MapState(self.map)

        self.iteration_data = IterationData(0, 0, 0, 0, 0)

        if self.store_sequence:
            self.trace = Trace(self.simulation_name, iteration)

    def run(self):
        bar = progressbar.ProgressBar()

        for tick in bar(range(self.num_ticks)):
            self.iteration_data.update_target_reach_counts(*self.map_state.remove_finished_agents())
            self.map_state.spawn_agents(tick, self.pedestrian_spawn_delay, self.car_spawn_delay)

            self.save_tick_to_trace()

        self.csv_reporter.save_iteration_results(self.iteration_data)
        self.persist_trace()

    def save_tick_to_trace(self):
        if self.store_sequence:
            self.trace.add_tick_state(self.map_state)

    def persist_trace(self):
        if self.store_sequence:
            self.trace.save_and_close()
