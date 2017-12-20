import argparse
import logging

import progressbar
import pyglet

from danger_zone.visualization.playback import Playback


def main():
    parser = argparse.ArgumentParser(description="Playback of an urban traffic simulation.")
    parser.add_argument(metavar='SIMULATION_RUN_NAME', dest='simulation_name', type=str, default="simple-medium")

    parser.add_argument("-i", "--iteration", metavar="I", dest="iteration", type=int, default=0,
                        help="Which iteration to visualize.")
    args = parser.parse_args()

    setup_logger()
    Playback(args.simulation_name, args.iteration)
    pyglet.app.run()


def setup_logger():
    progressbar.streams.wrap_stderr()
    logging.basicConfig()


if __name__ == "__main__":
    main()
