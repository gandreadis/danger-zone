import argparse

import pyglet

from danger_zone.simulation import Simulation
from danger_zone.ui.gif_exporter import GifExporter
from danger_zone.ui.window_controller import WindowController
from danger_zone.parameters import DEFAULT_TIME_LIMIT


def main():
    parser = argparse.ArgumentParser(description='Run traffic simulations.')
    parser.add_argument('--gif', '-g', dest='should_export_gif', action='store_true', help='Export GIF animation of the simulation.')
    parser.add_argument('--limit', '-l', metavar='N', dest='time_limit', type=int, help='Run a simulation for N ticks.')
    args = parser.parse_args()
    if args.time_limit and args.should_export_gif:
        print('Running simulation for %s ticks, then exporting GIF file.' % args.time_limit)
        WindowController(Simulation('simple', args.time_limit), GifExporter(args.time_limit))
    elif args.time_limit and not args.should_export_gif:
        print('Running simulation for %s ticks.' % args.time_limit)
        WindowController(Simulation('simple', args.time_limit))
    elif not args.time_limit and args.should_export_gif:
        print('Running simulation for default number of ticks, then exporting GIF file.')
        WindowController(Simulation('simple', DEFAULT_TIME_LIMIT), GifExporter(DEFAULT_TIME_LIMIT))
    elif not args.time_limit and not args.should_export_gif:
        print('Running simulation for default number of ticks.')
        WindowController(Simulation('simple', DEFAULT_TIME_LIMIT))  # these 25s can be changed to set the default, or we can figure out something with a parameter
    else:
        print('An error occurred in the options. Blame Jackson if you see this.')
        return
    pyglet.app.run()


if __name__ == "__main__":
    main()
