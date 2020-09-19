from pyprocessing import pp


def line(x1, y1, x2, y2):
    global pp
    pp.windows.set_line(x1, y1, x2, y2)
