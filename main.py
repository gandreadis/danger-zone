import argparse
import logging
import time

import progressbar

from danger_zone.experiment import Experiment


def main():
    """
    Main entry point for the simulator.

    Run `python main.py -h` for a list of all available command-line options.
    """

    parser = argparse.ArgumentParser(description="Simulation of urban traffic interactions.")
    parser.add_argument("-l", "--limit", metavar="N", dest="num_ticks", type=int, default=100,
                        help="Run simulation for N ticks.")
    parser.add_argument("-m", "--multiple", metavar="I", dest="num_iterations", type=int, default=1,
                        help="Run the simulation I times.")
    parser.add_argument("-p", "--pedestrians", metavar="P", dest="pedestrian_spawn_delay", type=int, default=5,
                        help="Run the simulation with P ticks of delay between pedestrian spawns.")
    parser.add_argument("-c", "--cars", metavar="C", dest="car_spawn_delay", type=int, default=5,
                        help="Run the simulation with C ticks of delay between car spawns.")
    parser.add_argument("-s", "--store-sequence", dest="store_sequence", action="store_true",
                        help="Store sequence of states in output file, for future playbacks.")
    parser.add_argument(metavar='SIMULATION_NAME', dest='simulation_name', type=str, default="simple-low")
    args = parser.parse_args()

    setup_logger()
    experiment = Experiment(args)

    start_time = time.clock()
    experiment.run()
    end_time = time.clock()
    logging.info("Successfully simulated experiment in {}s".format(int(end_time - start_time)))


def setup_logger():
    """Sets up the logging system."""

    progressbar.streams.wrap_stderr()
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
