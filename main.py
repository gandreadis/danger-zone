import argparse
import csv
import os
import pathlib

import pyglet

from danger_zone.parameters import DEFAULT_TIME_LIMIT
from danger_zone.setups import SETUPS
from danger_zone.simulation import Simulation
from danger_zone.ui.gif_exporter import GifExporter
from danger_zone.ui.window_controller import WindowController


def main():
    parser = argparse.ArgumentParser(description='Run traffic simulations.')
    parser.add_argument('-g', '--gif', dest='should_export_gif', action='store_true',
                        help='Export GIF animation of the simulation.')
    parser.add_argument('-l', '--limit', metavar='N', dest='time_limit', type=int, help='Run a simulation for N ticks.')
    parser.add_argument('-m', '--multiple', metavar='S', dest='runs', type=int, default=1, help='Run S simulations.')
    parser.add_argument('-c', '--csv', dest='should_export_csv', action='store_true',
                        help='Export CSV file of run statistics.')
    parser.add_argument('-i', '--invisible', dest='window_is_hidden', action='store_true',
                        help='Hide the window and run the simulation in headless mode.')
    parser.add_argument('-s', '--scenario', metavar='MAP_NAME', dest='map_name', type=str, default="simple-sparse")
    args = parser.parse_args()

    total_bicycles_through = 0
    total_pedestrians_through = 0
    total_cars_through = 0

    if args.should_export_csv:
        pathlib.Path('results').mkdir(exist_ok=True)
        results_file = open(os.path.join("results", args.map_name + ".csv"), 'w', newline='')
        writer = csv.writer(results_file)
        writer.writerow(["Bicycles", "Pedestrians", "Cars", "Collisions"])

    print('Running %s simulations...' % args.runs)
    for run_number in range(1, args.runs + 1):
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print('      Run number %s:' % run_number)
        if args.time_limit and args.should_export_gif:
            print('Running simulation for %s ticks, then exporting GIF file.' % args.time_limit)
            window = WindowController(Simulation(SETUPS[args.map_name], args.time_limit),
                                      GifExporter(args.time_limit),
                                      hidden=args.window_is_hidden)
        elif args.time_limit and not args.should_export_gif:
            print('Running simulation for %s ticks.' % args.time_limit)
            window = WindowController(Simulation(SETUPS[args.map_name], args.time_limit),
                                      hidden=args.window_is_hidden)
        elif not args.time_limit and args.should_export_gif:
            print('Running simulation for the default number of ticks, then exporting GIF file.')
            window = WindowController(Simulation(SETUPS[args.map_name], DEFAULT_TIME_LIMIT),
                                      GifExporter(DEFAULT_TIME_LIMIT),
                                      hidden=args.window_is_hidden)
        elif not args.time_limit and not args.should_export_gif:
            print('Running simulation for the default number of ticks.')
            window = WindowController(Simulation(SETUPS[args.map_name], DEFAULT_TIME_LIMIT),
                                      hidden=args.window_is_hidden)
        pyglet.app.run()

        if args.should_export_csv:
            print('Writing to CSV file...')
            writer.writerow([window.simulation.bicycles_through, window.simulation.pedestrians_through,
                             window.simulation.cars_through, window.simulation.collision_counter])
        total_bicycles_through += window.simulation.bicycles_through
        total_pedestrians_through += window.simulation.pedestrians_through
        total_cars_through += window.simulation.cars_through

    if args.should_export_csv:
        results_file.close()
        print('Results file saved as results.csv')
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')
    print('      Results:')
    print('An average of %s bicycles reached their target.' % (total_bicycles_through / args.runs))
    print('An average of %s pedestrians reached their target.' % (total_pedestrians_through / args.runs))
    print('An average of %s cars reached their target.' % (total_cars_through / args.runs))


if __name__ == "__main__":
    main()
