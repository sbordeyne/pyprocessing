from pyprocessing import pp


def ellipse(x, y, width, height):
    global pp
    pp.windows.set_ellipse(x, y, width, height)


def rect(x, y, width, height, *args):
    global pp
    if len(args) == 0:
        pp.windows.set_rectangle(x, y, width, height)
    elif len(args) == 1:
        pp.windows.set_rounded_rectangle(x, y, width, height,
                                         args[0], args[0], args[0], args[0])
    elif len(args) == 4:
        pp.windows.set_rounded_rectangle(x, y, width, height,
                                         args[0], args[1], args[2], args[3])
    else:
        raise TypeError


def triangle(x1, y1, x2, y2, x3, y3):
    global pp
    corners = [x1, y1, x2, y2, x3, y3]
    pp.windows.set_polygon(corners)


def quad(x1, y1, x2, y2, x3, y3, x4, y4):
    global pp
    corners = [x1, y1, x2, y2, x3, y3, x4, y4]
    pp.windows.set_polygon(corners)


def arc(x, y, width, height, start, stop, mode='PIE'):
    global pp
    pp.windows.set_arc(x, y, width, height, start, stop, mode)