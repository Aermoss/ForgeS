class Script:
    def __init__(self):
        self.enabled = True

    def update(self, window, entity):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False