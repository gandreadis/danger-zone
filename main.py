import argparse

import pyglet

from danger_zone.parameters import DEFAULT_TIME_LIMIT
from danger_zone.scenario import Scenario
from danger_zone.simulation import Simulation
from danger_zone.ui.gif_exporter import GifExporter
from danger_zone.ui.window_controller import WindowController


def main():
    parser = argparse.ArgumentParser(description='Run traffic simulations.')
    parser.add_argument('--gif', '-g', dest='should_export_gif', action='store_true', help='Export GIF animation of the simulation.')
    parser.add_argument('--limit', '-l', metavar='N', dest='time_limit', type=int, help='Run a simulation for N ticks.')
    parser.add_argument('--multiple', '-m', metavar='S', dest='runs', type=int, default=1, help='Run S simulations.')
    args = parser.parse_args()

    total_bicycles_through = 0
    total_pedestrians_through = 0
    total_cars_through = 0
    print('Running %s simulations...' % args.runs)
    for run_number in range(1, args.runs + 1):
        print('      Run number %s:' % run_number)
        if args.time_limit and args.should_export_gif:
            print('Running simulation for %s ticks, then exporting GIF file.' % args.time_limit)
            window = WindowController(Simulation(Scenario('simple'), args.time_limit), GifExporter(args.time_limit))
        elif args.time_limit and not args.should_export_gif:
            print('Running simulation for %s ticks.' % args.time_limit)
            window = WindowController(Simulation(Scenario('simple'), args.time_limit))
        elif not args.time_limit and args.should_export_gif:
            print('Running simulation for the default number of ticks, then exporting GIF file.')
            window = WindowController(Simulation(Scenario('simple'), DEFAULT_TIME_LIMIT),
                                      GifExporter(DEFAULT_TIME_LIMIT))
        elif not args.time_limit and not args.should_export_gif:
            print('Running simulation for the default number of ticks.')
            window = WindowController(Simulation(Scenario('simple'), DEFAULT_TIME_LIMIT))
        pyglet.app.run()
        total_bicycles_through += window.simulation.bicycles_through
        total_pedestrians_through += window.simulation.pedestrians_through
        total_cars_through += window.simulation.cars_through

    print('An average of %s bicycles reached their target.' % (total_bicycles_through/args.runs))
    print('An average of %s pedestrians reached their target.' % (total_pedestrians_through/args.runs))
    print('An average of %s cars reached their target.' % (total_cars_through/args.runs))


if __name__ == "__main__":
    main()
