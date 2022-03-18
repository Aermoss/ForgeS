import os, shutil, sys

class Builder:
    def __init__(self, file_name, noconsole = True, flags = []):
        self.file_name = file_name
        self.default_flags = []

        if noconsole:
            self.default_flags.append("--noconsole")

        else:
            self.default_flags.append("--console")

        self.flags = self.default_flags + flags
        self.flags_string = ""

        space = 0

        for i in self.flags:
            if space != 0:
                space -= 1
                self.flags_string += " "

            self.flags_string += i
            space += 1

        for i in sys.path:
            if "site-packages" in i:
                files = os.listdir(i)

                state = 0

                for j in files:
                    if "forges" == j:
                        state += 1
                        self.forges_path = i + "\\" + j

                    if "sdl2" == j:
                        state += 1
                        self.sdl2_path = i + "\\" + j

                    if "sdl2dll" == j:
                        state += 1
                        self.sdl2dll_path = i + "\\" + j
                    
                if state == 3:
                    self.site_packages_path = i

    def build(self):
        os.system(f"pyinstaller {self.file_name} {self.flags_string} --noconfirm --onefile --clean --icon={self.forges_path}/assets/icon/icon_ico.ico --add-data \"{self.sdl2dll_path};sdl2dll/\" --add-data \"{self.forges_path};forges/\"")
        shutil.copy(f"dist/{os.path.splitext(os.path.basename(self.file_name))[0]}.exe", ".")
        shutil.rmtree("build", ignore_errors = True)
        shutil.rmtree("dist", ignore_errors = True)
        os.remove(f"{os.path.splitext(os.path.basename(self.file_name))[0]}.spec")