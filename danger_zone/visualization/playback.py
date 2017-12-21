import pyglet

from danger_zone.map.map import MAP_SIZE, Map
from danger_zone.map.tile_types import Tile
from danger_zone.result_serialization.trace import Trace
from danger_zone.visualization.tile_colors import TILE_COLORS

TILE_SIZE = 32


class Playback(pyglet.window.Window):
    def __init__(self, simulation_name, iteration):
        super().__init__(width=MAP_SIZE * TILE_SIZE, height=MAP_SIZE * TILE_SIZE)
        self.simulation_name = simulation_name
        self.iteration = iteration
        self.map = Map.read_map_from_file(self.simulation_name)

        trace = Trace(self.simulation_name, self.iteration)
        self.tick_states = trace.read_trace_from_file()
        self.tick = 0

        pyglet.clock.schedule_interval(self.update, 1 / 2)

    def on_draw(self):
        self.clear()
        self.draw_map()
        self.draw_current_tick()

    def update(self, dt):
        if self.tick >= len(self.tick_states):
            self.close()

        self.tick += 1

    def draw_map(self):
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                tile = self.map.get_tile(x, y)
                self.draw_tile(x, y, TILE_COLORS[tile])

    def draw_current_tick(self):
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
        self.draw_rect(x * TILE_SIZE, (MAP_SIZE - y - 1) * TILE_SIZE, (x + 1) * TILE_SIZE, (MAP_SIZE - y) * TILE_SIZE,
                       color)

    def draw_rect(self, x1, y1, x2, y2, color):
        quad = pyglet.graphics.vertex_list(4,
                                           ('v2i', (x1, y1, x2, y1, x2, y2, x1, y2)),
                                           ('c3B', (*color, *color, *color, *color)))
        quad.draw(pyglet.gl.GL_QUADS)
