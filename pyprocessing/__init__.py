# flake8: noqa

from pyprocessing.pyprocessing import PyProcessing
from pyprocessing.runner import Runner
from pyprocessing.converter import Converter


__version__ = '0.0.1b4'
__author__ = ('Dogeek', )

width = 640
height = 480
pp = PyProcessing()

from pyprocessing.environment import (
    size, frame_rate,
)
from pyprocessing.primitives_2d import (
    line,
)
from pyprocessing.color import (
    Color, alpha, red, green, blue,
    brightness, hue, saturation, lerp_color,
    stroke, background,
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
