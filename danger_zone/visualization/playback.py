import pyglet

from danger_zone.map.map import MAP_SIZE, Map
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
                self.draw_rect(x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE,
                               TILE_COLORS[tile])

    def draw_current_tick(self):
        pass

    def draw_rect(self, x1, y1, x2, y2, color):
        quad = pyglet.graphics.vertex_list(4,
                                           ('v2i', (x1, y1, x2, y1, x2, y2, x1, y2)),
                                           ('c3B', (*color, *color, *color, *color)))
        quad.draw(pyglet.gl.GL_QUADS)
