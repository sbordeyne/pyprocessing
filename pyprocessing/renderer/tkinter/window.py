from collections import deque
import tkinter as tk

from pyprocessing.renderer.actions import Action


class Window(tk.Frame):
    def __init__(self, master, pyprocessing):
        super().__init__(master)
        namespace = pyprocessing.namespace
        self.pyprocessing = pyprocessing

        width = namespace.get('width', 640)
        height = namespace.get('height', 480)
        self.frame_rate = namespace.get('framerate', 60)
        self.stroke = namespace.get('stroke', '#ffffff')

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.queued_actions = deque()
        self.canvas_objs = []

    def setup(self):
        namespace = self.pyprocessing.namespace
        width = namespace.get('width', 640)
        height = namespace.get('height', 480)
        self.frame_rate = namespace.get('framerate', 60)
        self.stroke = namespace.get('stroke', '#ffffff')

        self.config(width=width, height=height)
        self.canvas.config(width=width, height=height)
        self.canvas.update()
        if self.queued_actions:
            self.draw_once()

    def draw_once(self):
        for obj in self.canvas_objs:
            self.canvas.delete(obj)
        self.canvas_objs = []

        while self.queued_actions:
            act = self.queued_actions.popleft()
            self.pyprocessing.logger.info('Processing action : %s', act)
            rv = act()
            if isinstance(rv, (str, int)):
                self.canvas_objs.append(rv)

    def redraw(self):
        self.canvas.update()

        self.pyprocessing.draw()
        self.draw_once()
        self.after(int(1_000 / self.frame_rate), self.redraw)

    def set_background(self, color):
        action = Action(self.canvas, 'config', bg=color.hex)
        self.queued_actions.append(action)

    def set_line(self, x1, y1, x2, y2):
        action = Action(
            self.canvas, 'create_line',
            x1, y1, x2, y2, fill=self.stroke.hex,
        )
        self.queued_actions.append(action)
