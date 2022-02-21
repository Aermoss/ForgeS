# Forge S
A game engine made with SDL 2.

## Getting Started
1) Install Python
2) Open cmd/terminal and type:

```
pip install ForgeS
```

## Examples
# Creating a window
``` python
from forges import *

class Window(forges.Window):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def on_quit(self):
        pass

    def run(self):
        forges.run()

if __name__ == "__main__":
    window = Window()
    window.run()
```

# Creating a cube
``` python
from forges import *

class Cube(Entity):
    def __init__(self):
        super().__init__()

        self.center()

    def update(self):
        pass

class Window(Window):
    def __init__(self):
        super().__init__()

        self.cube = Cube()

    def update(self):
        pass

    def on_quit(self):
        pass

    def run(self):
        forges.run()

if __name__ == "__main__":
    window = Window()
    window.run()
```