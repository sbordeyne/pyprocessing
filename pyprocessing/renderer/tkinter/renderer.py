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
        self.root.geometry(f"{w + 2}x{h + 20}+20+20")
        self.root.title()
        self.window = Window(
            self.root, self.pyprocessing.namespace,
            self.pyprocessing.draw
        )
        self.window.pack(expand=True, fill=tk.BOTH)

    def start(self):
        self.window.redraw()
        print(self.window.winfo_width(), self.window.winfo_height())
        print(self.window.canvas.winfo_width(), self.window.canvas.winfo_height())
        self.root.mainloop()
