import os

import __main__

class FontManager:
    def __init__(self, engine = None):
        if engine == None:
            if hasattr(__main__.forges, "forges"):
                self.engine = __main__.forges.forges

            else:
                self.engine = __main__.forges

        else:
            self.engine = engine

        self.path = self.engine.path + "\\assets\\fonts"
        self.fonts = {}

    def get(self):
        for file in os.listdir(self.path):
            self.fonts[file] = {}

            for font in os.listdir(self.path + f"\\{file}"):
                file_name, file_ext = os.path.splitext(font)

                if file_ext in [".ttf"]:
                    self.fonts[file][file_name] = self.path + f"\\{file}\\" + font

        return self.fonts