from pyprocessing import (
    size,  frame_rate,
    background, line, point,
    stroke_cap, stroke_weight,
    fill, stroke
)


def setup():
    size(100, 100)
    background(255)
    fill(0)
    stroke(0)
    stroke_weight(10)
    frame_rate(60)


def draw():
    stroke_cap(1)
    line(10, 10, 50, 10)
    point(70, 10)

    stroke_cap(2)
    line(10, 30, 50, 30)
    point(70, 30)

    stroke_cap(4)
    line(10, 50, 50, 50)
    point(70, 50)
