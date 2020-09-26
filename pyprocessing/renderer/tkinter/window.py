from collections import deque
from math import degrees
import tkinter as tk

from pyprocessing.renderer.actions import Action


class Window(tk.Frame):
    def __init__(self, master, pyprocessing):
        super().__init__(master)
        self.pp = pyprocessing

        self.canvas = tk.Canvas(
            self, width=self.pp.namespace.width,
            height=self.pp.namespace.height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.queued_actions = deque()
        self.canvas_objs = []

    def setup(self):
        self.config(
            width=self.pp.namespace.width,
            height=self.pp.namespace.height,
        )
        self.canvas.config(
            width=self.pp.namespace.width,
            height=self.pp.namespace.height,
        )
        self.canvas.update()
        if self.queued_actions:
            self.draw_once()

    def draw_once(self):
        for obj in self.canvas_objs:
            self.canvas.delete(obj)
        self.canvas_objs = []

        while self.queued_actions:
            act = self.queued_actions.popleft()
            self.pp.logger.info('Processing action : %s', act)
            rv = act()
            if isinstance(rv, (str, int)):
                self.canvas_objs.append(rv)

    def redraw(self):
        self.canvas.update()
        self.pp.draw()
        self.draw_once()
        self.after(
            int(1_000 / self.pp.namespace.framerate),
            self.redraw,
        )

    def set_background(self, color):
        action = Action(self.canvas, 'config', bg=color.hex)
        self.queued_actions.append(action)

    def set_line(self, x1, y1, x2, y2):
        action = Action(
            self.canvas, 'create_line',
            x1, y1, x2, y2,
            fill=self.pp.namespace.stroke.hex,
            capstyle=self.pp.namespace.stroke_cap_attribute,
            width=self.pp.namespace.stroke_thickness_attribute,
        )
        self.queued_actions.append(action)

    def set_ellipse(self, x, y, width, height):
        x1 = x - (width + 1) // 2
        y1 = y - (height + 1) // 2
        x2 = x + width // 2 + 1
        y2 = y + height // 2 + 1
        action = Action(
            self.canvas, 'create_oval',
            x1, y1, x2, y2,
            fill=self.pp.namespace.fill.hex,
            outline=self.pp.namespace.stroke.hex,
            width=self.pp.namespace.stroke_thickness_attribute,
        )
        self.queued_actions.append(action)

    def set_rectangle(self, x1, y1, width, height):
        x2 = x1 + width + 1
        y2 = y1 + height + 1
        thickness = self.pp.namespace.stroke_thickness_attribute
        action = Action(
            self.canvas, 'create_rectangle',
            x1 + thickness, y1 + thickness, x2 - thickness, y2 - thickness,
            fill=self.pp.namespace.fill.hex,
            outline=None,
            width=thickness,
        )
        # Makes the corners with the right shape
        line_action = Action(
            self.canvas, 'create_line',
            x1, y1,
            x1 + width, y1,
            x1 + width, y1 + height,
            x1, y1 + height,
            x1, y1,
            fill=self.pp.namespace.stroke.hex,
            width=thickness,
            joinstyle=self.pp.namespace.join,
        )

        self.queued_actions.append(action)
        self.queued_actions.append(line_action)

    def set_rounded_rectangle(self, x, y, width, height, c1, c2, c3, c4):
        # For when rect has 5 or 8 arguments
        # TODO Handle 5 or 8 arguments passed to rect by making a rectangle with rounded corners
        pass

    def set_polygon(self, points):
        action = Action(
            self.canvas, 'create_polygon',
            points, fill=self.pp.namespace.fill.hex,
            outline=None,
            width=self.pp.namespace.stroke_thickness_attribute,
        )
        # Makes the corners with the right shape
        line_action = Action(
            self.canvas, 'create_line',
            *points, points[0], points[1],
            fill=self.pp.namespace.stroke.hex,
            joinstyle=self.pp.namespace.join,
            width=self.pp.namespace.thickness,
        )
        self.queued_actions.append(action)
        self.queued_actions.append(line_action)

    def set_arc(self, x, y, width, height, start, stop, mode):
        x1 = x - (width + 1) // 2
        y1 = y - (height + 1) // 2
        x2 = x + width // 2 + 1
        y2 = y + height // 2 + 1
        start_degree = degrees(start)
        stop_degree = degrees(stop)
        angle = start_degree - stop_degree
        mode = mode.lower()
        if mode == 'pie':
            mode += 'slice'
        action = Action(
            self.canvas, 'create_arc',
            x1, y1, x2, y2,
            start=start_degree, extent=angle, style=mode,
            fill=self.pp.namespace.fill.hex,
            outline=self.pp.namespace.stroke.hex,
            width=self.pp.namespace.stroke_thickness_attribute,
        )
        self.queued_actions.append(action)

    def set_point(self, x, y):
        if self.pp.namespace.stroke_cap_attribute not in ('round', 'projecting'):
            return

        if self.pp.namespace.cap == 'round':
            draw_function = 'create_rectangle'
        else:
            draw_function = 'create_oval'

        offset = self.pp.namespace.stroke_thickness_attribute // 2
        action = Action(
            self.canvas, draw_function,
            x - offset, y - offset, x + offset + 1, y + offset + 1,
            fill=self.pp.namespace.stroke.hex,
            outline=None,
        )
        self.queued_actions.append(action)
