class Pedestrian:
    def __init__(self, position, target, map_state):
        self.position = position
        self.target = target
        self.map_state = map_state

    def move(self):
        pass

    def is_done(self):
        return self.position == self.target
