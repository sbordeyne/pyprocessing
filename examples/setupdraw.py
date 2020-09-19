from pyprocessing import (
    size, stroke, frame_rate,
    background, line, height, width,
)

y = 100


def setup():
    size(640, 360)
    stroke(255)
    frame_rate(60)
    background(0)


def draw():
    global y
    y = y - 1
    if y < 0:
        y = height
    line(0, y, width, y)
