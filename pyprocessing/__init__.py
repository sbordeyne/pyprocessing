# flake8: noqa

__version__ = '0.0.1b6'
__author__ = ('Dogeek', )

width = 640
height = 480
frame_count = 0

from pyprocessing.pyprocessing import PyProcessing
from pyprocessing.runner import Runner
from pyprocessing.converter import Converter


pp = PyProcessing()

from pyprocessing.environment import (
    size, frame_rate, delay,
)
from pyprocessing.primitives_2d import (
    ellipse, rect, triangle, quad, arc,
    square, circle, line, point
)
from pyprocessing.attributes import (
    stroke_cap, stroke_weight, stroke_join,
)
from pyprocessing.color import (
    Color, alpha, red, green, blue,
    brightness, hue, saturation, lerp_color,
    stroke, background, fill,
)
from pyprocessing.time import (
    second, minute, hour, day, month,
    year, millis,
)
from pyprocessing.math import (
    PVector,
)
from pyprocessing.random import (
    noise, noise_detail, random_gaussian,
    random, random_seed,
)
# Trigonometry functions from math
from math import (
    acos, asin, atan, atan2, cos,
    degrees, radians, sin, tan
)
from pyprocessing.constants import (
    HALF_PI, PI, QUARTER_PI, TAU, TWO_PI,
)
from pyprocessing.calculation import (
    ceil, dist, exp, floor, log, pow, sqrt,
    sq, constrain, lerp, mag, map, norm
)
from pyprocessing.structure import (
    thread, timeout,
)