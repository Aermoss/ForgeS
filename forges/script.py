import forges

class Script:
    def __init__(self):
        self.engine = forges.get()
        self.enabled = True

    def update(self, window, entity):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def bound(self, func):
        setattr(self.__class__, func.__name__, classmethod(func))