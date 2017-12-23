import argparse

import pyglet

from danger_zone.visualization.playback import Playback
from main import setup_logger


def main():
    """
    Main entry point for the visualizer.

    Run `python visualizer.py -h` for a list of all available command-line options.
    """

    parser = argparse.ArgumentParser(description="Playback of an urban traffic simulation.")
    parser.add_argument(metavar='SIMULATION_RUN_NAME', dest='simulation_name', type=str, default="simple-medium")

    parser.add_argument("-i", "--iteration", metavar="I", dest="iteration", type=int, default=0,
                        help="Which iteration to visualize.")
    args = parser.parse_args()

    setup_logger()
    Playback(args.simulation_name, args.iteration)
    pyglet.app.run()


if __name__ == "__main__":
    main()
