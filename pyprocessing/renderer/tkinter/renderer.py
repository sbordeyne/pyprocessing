import tkinter as tk
from pyprocessing.renderer.tkinter.window import Window


class TkRenderer:
    def __init__(self, pyprocessing):
        self.pyprocessing = pyprocessing
        self.root = None
        self.window = None

    def init(self):
        self.root = tk.Tk()
        w = self.pyprocessing.width
        h = self.pyprocessing.height
        geometry = f"{w + 2}x{h + 20}+20+20"
        self.pyprocessing.logger.info(
            'Initializing window with geometry %s', geometry
        )
        self.root.geometry(geometry)
        self.root.title()
        self.root.resizable(False, False)
        self.window = Window(self.root, self.pyprocessing)
        self.window.pack(expand=True, fill=tk.BOTH)

    def start(self):
        self.window.redraw()
        self.root.mainloop()
