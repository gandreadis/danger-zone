import pyglet

from danger_zone.parameters import MAP_WIDTH, MAP_HEIGHT
from danger_zone.util.vector_calculation import get_vector_angle


class WindowController(pyglet.window.Window):
    def __init__(self, simulation, gif_exporter=None):
        super().__init__(width=MAP_WIDTH, height=MAP_HEIGHT)

        self.simulation = simulation
        self.gif_exporter = gif_exporter

        pyglet.clock.schedule_interval(self.update, 1 / 30)

    # noinspection PyMethodOverriding
    def on_draw(self):
        self.clear()
        self.draw_agents()

    def update(self, dt):
        self.simulation.on_tick()

        if self.gif_exporter and not self.gif_exporter.save_frame():
            self.close()
            self.gif_exporter.export()

        if self.simulation.tick == self.simulation.maxtick :
            print('Simulation completed with %s collisions.' % self.simulation.collision_counter)
            self.close()

    def draw_agents(self):
        for agent in self.simulation.agents:
            self.draw_agent(agent)

    def draw_agent(self, agent):
        x = int(agent.position[0] - agent.width / 2)
        y = int(agent.position[1] - agent.height / 2)

        pyglet.graphics.glPushMatrix()
        pyglet.graphics.glTranslatef(agent.position[0], agent.position[1], 0)
        pyglet.graphics.glRotatef(-get_vector_angle(agent.velocity), 0, 0, 1)
        pyglet.graphics.glTranslatef(-agent.position[0], -agent.position[1], 0)
        quad = pyglet.graphics.vertex_list(4,
                                           ('v2i', self.create_quad_vertex_list(x, y,
                                                                                agent.width, agent.height)),
                                           ('c3B', (0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255)))
        quad.draw(pyglet.gl.GL_QUADS)
        pyglet.graphics.glPopMatrix()

    def create_quad_vertex_list(self, x, y, width, height):
        return x, y, x + width, y, x + width, y + height, x, y + height
