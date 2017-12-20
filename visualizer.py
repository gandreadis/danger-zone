import argparse
import logging

import progressbar


def main():
    parser = argparse.ArgumentParser(description="Playback of an urban traffic simulation.")
    parser.add_argument(metavar='SIMULATION_NAME', dest='simulation_name', type=str, default="simple-medium")
    args = parser.parse_args()

    setup_logger()
    # TODO: Show visualization


def setup_logger():
    progressbar.streams.wrap_stderr()
    logging.basicConfig()


if __name__ == "__main__":
    main()
