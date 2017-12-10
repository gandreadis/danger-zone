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
    parser.add_argument('--multiple', '-m', metavar='S', dest='runs', type=int, default=1, help='Run S simulations.')
    args = parser.parse_args()
    run_number = 1
    print('Running %s simulations:' % args.runs)
    for run_number in range(0, args.runs):
        if args.time_limit and args.should_export_gif:
            print('Running simulation for %s ticks, then exporting GIF file.' % args.time_limit)
            WindowController(Simulation('simple', args.time_limit), GifExporter(args.time_limit))
        elif args.time_limit and not args.should_export_gif:
            print('Running simulation for %s ticks.' % args.time_limit)
            WindowController(Simulation('simple', args.time_limit))
        elif not args.time_limit and args.should_export_gif:
            print('Running simulation for the default number of ticks, then exporting GIF file.')
            WindowController(Simulation('simple', DEFAULT_TIME_LIMIT), GifExporter(DEFAULT_TIME_LIMIT))
        elif not args.time_limit and not args.should_export_gif:
            print('Running simulation for the default number of ticks.')
            WindowController(Simulation('simple', DEFAULT_TIME_LIMIT))
        pyglet.app.run()


if __name__ == "__main__":
    main()
