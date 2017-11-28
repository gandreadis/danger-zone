import pyglet

from danger_zone.parameters import MAP_WIDTH, MAP_HEIGHT


class WindowController(pyglet.window.Window):
    def __init__(self, simulation):
        super().__init__(width=MAP_WIDTH, height=MAP_HEIGHT)

        self.simulation = simulation
        pyglet.clock.schedule_interval(self.update, 1 / 30)

    def on_draw(self):
        self.clear()
        # TODO draw map background
        self.draw_agents()

    def update(self, dt):
        self.simulation.on_tick()

    def draw_agents(self):
        for agent in self.simulation.agents:
            self.draw_agent(agent)

    def draw_agent(self, agent):
        quad = pyglet.graphics.vertex_list(4,
                                           ('v2i', self.create_quad_vertex_list(
                                               int(agent.position[0] - agent.width / 2),
                                               int(agent.position[1] - agent.height / 2),
                                               agent.width,
                                               agent.height)),
                                           ('c3B', (0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255)))
        quad.draw(pyglet.gl.GL_QUADS)

    def create_quad_vertex_list(self, x, y, width, height):
        return x, y, x + width, y, x + width, y + height, x, y + height
