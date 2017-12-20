import argparse
import logging
import time

import progressbar

from danger_zone.experiment import Experiment


def main():
    parser = argparse.ArgumentParser(description="Simulation of urban traffic interactions.")
    parser.add_argument("-l", "--limit", metavar="N", dest="num_ticks", type=int, default=100,
                        help="Run simulation for N ticks.")
    parser.add_argument("-m", "--multiple", metavar="I", dest="num_iterations", type=int, default=1,
                        help="Run the simulation I times.")
    parser.add_argument("-s", "--store-sequence", dest="store_sequence", action="store_true",
                        help="Store sequence of states in output file, for future playbacks.")
    parser.add_argument(metavar='SIMULATION_NAME', dest='simulation_name', type=str, default="simple-low")
    args = parser.parse_args()

    setup_logger()
    experiment = Experiment(args.num_ticks, args.num_iterations, args.store_sequence, args.simulation_name)

    start_time = time.clock()
    experiment.run()
    end_time = time.clock()
    logging.info("Successfully simulated experiment in {}s".format(int(end_time - start_time)))


def setup_logger():
    progressbar.streams.wrap_stderr()
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
