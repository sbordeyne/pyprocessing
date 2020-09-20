from pyprocessing import (
    size, stroke, frame_rate, fill,
    background, line, circle, ellipse,
    square, rect, triangle, quad, arc,
    PI, QUARTER_PI
)


def setup():
    size(640, 360)
    stroke(0)
    fill(255)
    frame_rate(60)
    background(127)


def draw():
    line(50, 100, 150, 100)
    circle(200, 100, 50)
    ellipse(300, 100, 50, 25)
    square(400, 100, 50)
    rect(500, 100, 50, 25)
    triangle(50, 200, 300, 250, 100, 300)
    quad(400, 200, 500, 250, 350, 300, 375, 100)
    arc(200, 400, 80, 80, 0, PI+QUARTER_PI, 'PIE')
