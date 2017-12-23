import pyglet

from danger_zone.map.map import MAP_SIZE, Map
from danger_zone.map.tile_types import Tile
from danger_zone.result_serialization.trace import Trace
from danger_zone.visualization.tile_colors import TILE_COLORS

TILE_SIZE = 32


class Playback(pyglet.window.Window):
    """Class representing a simulation trace playback window."""

    def __init__(self, simulation_name, iteration):
        """
        Constructs an instance of this class.

        :param simulation_name: The name of the simulation to be loaded.
        :param iteration: The number of the iteration that should be played back.
        """

        super().__init__(width=MAP_SIZE * TILE_SIZE, height=MAP_SIZE * TILE_SIZE)
        self.simulation_name = simulation_name
        self.iteration = iteration
        self.map = Map.read_map_from_file(self.simulation_name)

        trace = Trace(self.simulation_name, self.iteration)
        self.tick_states = trace.read_trace_from_file()
        self.tick = 0

        pyglet.clock.schedule_interval(self.update, 1 / 2)

    def on_draw(self):
        """Callback to be invoked when the scene should be re-rendered."""

        self.clear()
        self.draw_map()
        self.draw_current_tick()

    def update(self, dt):
        """Callback to be invoked periodically to progress through the trace."""

        if self.tick >= len(self.tick_states):
            self.close()

        self.tick += 1

    def draw_map(self):
        """Draws the static map to the window surface."""

        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                tile = self.map.get_tile(x, y)
                self.draw_tile(x, y, TILE_COLORS[tile])

    def draw_current_tick(self):
        """Draws all agents to the window surface."""

        if self.tick >= len(self.tick_states):
            return

        pedestrians = self.tick_states[self.tick]["pedestrians"]
        for pedestrian in pedestrians:
            self.draw_tile(pedestrian["x"], pedestrian["y"], TILE_COLORS[Tile.PEDESTRIAN])
            self.draw_rectangle_outline(pedestrian["x"], pedestrian["y"], 1, 1)

        cars = self.tick_states[self.tick]["cars"]
        for car in cars:
            self.draw_tile(car["x"], car["y"], TILE_COLORS[Tile.CAR])
            self.draw_tile(car["x"] + 1, car["y"], TILE_COLORS[Tile.CAR])
            self.draw_tile(car["x"], car["y"] + 1, TILE_COLORS[Tile.CAR])
            self.draw_tile(car["x"] + 1, car["y"] + 1, TILE_COLORS[Tile.CAR])

            if car["is_horizontal"]:
                self.draw_tile(car["x"] + 2, car["y"], TILE_COLORS[Tile.CAR])
                self.draw_tile(car["x"] + 2, car["y"] + 1, TILE_COLORS[Tile.CAR])
                self.draw_rectangle_outline(car["x"], car["y"], 3, 2)
            else:
                self.draw_tile(car["x"], car["y"] + 2, TILE_COLORS[Tile.CAR])
                self.draw_tile(car["x"] + 1, car["y"] + 2, TILE_COLORS[Tile.CAR])
                self.draw_rectangle_outline(car["x"], car["y"], 2, 3)

    def draw_rectangle_outline(self, x, y, width, height):
        """
        Draws a rectangle outline around the given rectangular area.

        :param x: The grid x coordinate.
        :param y: The grid y coordinate.
        :param width: The grid width of the rectangle.
        :param height: The grid height of the rectangle.
        """

        pyglet.graphics.glColor3b(0, 0, 0)
        pyglet.gl.glLineWidth(3)
        display_x = x * TILE_SIZE
        display_y = (MAP_SIZE - y) * TILE_SIZE
        point1 = display_x, display_y
        point2 = display_x + width * TILE_SIZE, display_y
        point3 = display_x + width * TILE_SIZE, display_y - height * TILE_SIZE
        point4 = display_x, display_y - height * TILE_SIZE

        pyglet.graphics.draw(8, pyglet.gl.GL_LINES, ('v2i', [
            *point1, *point2,
            *point2, *point3,
            *point3, *point4,
            *point4, *point1,
        ]))

    def draw_tile(self, x, y, color):
        """
        Draws a tile at the given location, with given `color`.

        :param x: The grid x coordinate.
        :param y: The grid y coordinate.
        :param color: The RGB color triple to be used while drawing this tile.
        """

        self.draw_rect(x * TILE_SIZE, (MAP_SIZE - y - 1) * TILE_SIZE, (x + 1) * TILE_SIZE, (MAP_SIZE - y) * TILE_SIZE,
                       color)

    def draw_rect(self, x1, y1, x2, y2, color):
        """
        Draws a rectangle on the screen, with given `color`.

        :param x1: The x coordinate of one point.
        :param y1: The y coordinate of another point.
        :param x2: The x coordinate of one point.
        :param y2: The y coordinate of another point.
        :param color: The RGB triple to be used to draw this rectangle.
        """

        quad = pyglet.graphics.vertex_list(4,
                                           ('v2i', (x1, y1, x2, y1, x2, y2, x1, y2)),
                                           ('c3B', (*color, *color, *color, *color)))
        quad.draw(pyglet.gl.GL_QUADS)
