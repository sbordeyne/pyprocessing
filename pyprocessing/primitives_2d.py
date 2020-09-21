from pyprocessing import PyProcessing


def ellipse(x, y, width, height):
    pp = PyProcessing()
    pp.windows.set_ellipse(x, y, width, height)


def rect(x, y, width, height, *args):
    pp = PyProcessing()
    if len(args) == 0:
        pp.windows.set_rectangle(x, y, width, height)
    elif len(args) == 1:
        pp.windows.set_rounded_rectangle(
            x, y, width, height,
            args[0], args[0], args[0], args[0]
        )
    elif len(args) == 4:
        pp.windows.set_rounded_rectangle(
            x, y, width, height,
            args[0], args[1], args[2], args[3]
        )
    else:
        raise ValueError(f'rect() takes 4, 5 or 8 parameters. ({len(args) + 4} given)')


def triangle(x1, y1, x2, y2, x3, y3):
    pp = PyProcessing()
    corners = [x1, y1, x2, y2, x3, y3]
    pp.windows.set_polygon(corners)


def quad(x1, y1, x2, y2, x3, y3, x4, y4):
    pp = PyProcessing()
    corners = [x1, y1, x2, y2, x3, y3, x4, y4]
    pp.windows.set_polygon(corners)


def arc(x, y, width, height, start, stop, mode='PIE'):
    pp = PyProcessing()
    pp.windows.set_arc(x, y, width, height, start, stop, mode)


def circle(x, y, size):
    pp = PyProcessing()
    pp.windows.set_ellipse(x, y, size, size)


def square(x, y, extent):
    pp = PyProcessing()
    pp.windows.set_rectangle(x, y, extent, extent)


def line(x1, y1, x2, y2):
    pp = PyProcessing()
    pp.windows.set_line(x1, y1, x2, y2)


def point(x, y):
    pp = PyProcessing()
    pp.windows.set_point(x, y)
