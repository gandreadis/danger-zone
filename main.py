import argparse

import pyglet

from danger_zone.simulation import Simulation
from danger_zone.ui.gif_exporter import GifExporter
from danger_zone.ui.window_controller import WindowController


def main():
    parser = argparse.ArgumentParser(description='Run traffic simulations.')
    parser.add_argument('--export', '-e', dest='num_frames', help='Export GIF animation with N frames', action='store',
                        type=int)
    args = parser.parse_args()

    if args.num_frames:
        WindowController(Simulation(), GifExporter(args.num_frames))
        pyglet.app.run()
    else:
        WindowController(Simulation())
        pyglet.app.run()


if __name__ == "__main__":
    main()
