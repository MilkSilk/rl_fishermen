class Fisherman:
    def __init__(self, policy=None, pond=None):
        self.policy = policy
        self.pond = pond
        self.fish = 0

    def action(self):
        self.fish += self.pond.serve_fisherman()

