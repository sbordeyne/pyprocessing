from pyprocessing import pp, width, height


def size(w, h):
    global pp
    global width
    global height
    pp.namespace['width'] = w
    pp.namespace['height'] = h
    width = w
    height = h


def frame_rate(fr=60):
    global pp
    pp.namespace['framerate'] = fr
