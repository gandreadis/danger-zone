class Pedestrian:
    def __init__(self, position, target):
        self.position = position
        self.target = target

    def is_done(self):
        return self.position == self.target
