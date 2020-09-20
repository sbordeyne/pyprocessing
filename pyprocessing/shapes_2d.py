from pyprocessing import pp


def circle(x, y, size):
    global pp
    pp.windows.set_ellipse(x, y, size, size)


def square(x, y, extent):
    global pp
    pp.windows.set_rectangle(x, y, extent, extent)


def line(x1, y1, x2, y2):
    global pp
    pp.windows.set_line(x1, y1, x2, y2)