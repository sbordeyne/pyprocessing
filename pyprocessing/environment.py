from pyprocessing import pp, width, height


def size(w, h):
    global pp
    global width
    global height
    pp.width = w
    pp.height = h


def frame_rate(fr=60):
    global pp
    pp.namespace['framerate'] = fr
