from pyprocessing.utils import int_to_color
from pyprocessing.pyprocessing import PyProcessing
from pyprocessing.runner import Runner


__version__ = '0.0.1'
__author__ = ('Dogeek', )

width = 640
height = 480
pp = PyProcessing()


def size(w, h):
    global pp
    global width
    global height
    pp.namespace['width'] = w
    pp.namespace['height'] = h
    width = w
    height = h


def stroke(color=255):
    global pp
    if isinstance(color, int):
        color = int_to_color(color)
    pp.namespace['stroke'] = color


def frame_rate(fr=60):
    global pp
    pp.namespace['framerate'] = fr


def background(color):
    global pp
    if isinstance(color, int):
        color = int_to_color(color)

    pp.windows.set_background(color)


def line(x, y, width, height):
    global pp
    pp.windows.set_line(x, y, width, height)
