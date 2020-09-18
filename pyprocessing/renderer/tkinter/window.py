from collections import deque
import tkinter as tk

from pyprocessing.renderer.actions import Action


class Window(tk.Frame):
    def __init__(self, master, namespace, draw_fn):
        width = namespace.get('width', 640)
        height = namespace.get('height', 480)
        frame_rate = namespace.get('framerate', 60)
        self.stroke = namespace.get('stroke', '#ffffff')

        super().__init__(master, width=width, height=height)
        self.master.resizable(False, False)
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.queued_actions = deque()
        self.canvas_objs = []
        self.frame_rate = frame_rate
        self.draw_fn = draw_fn

    def redraw(self):
        self.draw_fn()
        for obj in self.canvas_objs:
            self.canvas.delete(obj)
        self.canvas_objs = []

        while act := self.queued_actions.popleft() in self.queued_actions:
            rv = act()
            if isinstance(rv, str):
                self.canvas_objs.append(rv)

        self.after(int(1_000 / self.frame_rate), self.redraw)

    def set_background(self, color):
        action = Action(self.canvas, 'config', bg=color)
        self.queued_actions.append(action)

    def set_line(self, x, y, width, height):
        action = Action(
            self.canvas, 'create_line',
            x, y, x + width, y + height, color=self.stroke,
        )
        self.queued_actions.append(action)
