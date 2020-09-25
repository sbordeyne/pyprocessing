import tkinter as tk
from pyprocessing.renderer.tkinter.window import Window


class TkRenderer:
    def __init__(self, pyprocessing):
        self.pp = pyprocessing
        self.root = None
        self.window = None
        self.this = self

    def init(self):
        self.root = tk.Tk()
        w = self.pp.namespace.width
        h = self.pp.namespace.height
        x, y = self.pp.namespace.window_offset
        geometry = f"{w + 2}x{h + 20}+{x}+{y}"
        self.pp.logger.info(
            'Initializing window with geometry %s', geometry
        )
        self.root.geometry(geometry)
        self.root.title(self.pp.namespace.window_title)
        self.root.resizable(*self.pp.namespace.window_resizable)
        self.root.iconphoto(True, self.pp.namespace.window_icon.tk_photo_image)
        self.window = Window(self.root, self.pp)
        self.window.pack(expand=True, fill=tk.BOTH)

    def start(self):
        self.window.redraw()
        self.root.mainloop()

    def update_location(self):
        w = self.pp.namespace.width
        h = self.pp.namespace.height
        x, y = self.pp.namespace.window_offset
        geometry = f"{w + 2}x{h + 20}+{x}+{y}"
        self.pp.logger.info(
            'Updating window with geometry %s', geometry
        )
        self.root.geometry(geometry)

    def update_size(self):
        self.update_location()

    def update_title(self):
        self.root.title(self.pp.namespace.window_title)

    def update_resizable(self):
        self.root.resizable(self.pp.namespace.window_resizable)

    def update_icon(self):
        self.root.iconphoto(True, self.pp.namespace.window_icon.tk_photo_image)
