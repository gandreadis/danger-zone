import pyglet

from danger_zone.simulation import Simulation
from danger_zone.ui.window_controller import WindowController


def show_window():
    WindowController(Simulation())
    pyglet.app.run()


if __name__ == "__main__":
    # TODO interpret command-line arguments

    show_window()
