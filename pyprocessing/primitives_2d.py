from pyprocessing import pp


def line(x, y, width, height):
    global pp
    pp.windows.set_line(x, y, width, height)
