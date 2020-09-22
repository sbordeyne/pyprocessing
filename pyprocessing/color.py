import colorsys

from pyprocessing import PyProcessing


class Color:
    RGB = 0
    HSV = 1
    HLS = 2

    @staticmethod
    def from_hex(color):
        # strip the leading '#' sign
        color = color[1:]

        # select the hex r, g, b component, cast into an int
        # It's hex, so specify the base for the int function
        red = int(color[0:2], base=16)
        green = int(color[2:4], base=16)
        blue = int(color[4:6], base=16)
        return Color(red, green, blue, colorspace=Color.RGB)

    def __init__(self, *args, colorspace=0):
        self.colorspace = colorspace

        if len(args) == 1:
            # 1 argument : no matter the colorspace, it's grayscale
            self.red = self.green = self.blue = args[0]
            self.alpha = 255
        elif len(args) == 2:
            self.red = self.green = self.blue = args[0]
            self.alpha = args[1]
        elif len(args) == 3:
            self.alpha = 255
            self.red, self.green, self.blue = self._values_to_rgb(*args)
        elif len(args) == 4:
            v1, v2, v3, self.alpha = args
            self.red, self.green, self.blue = self._values_to_rgb(v1, v2, v3)

    def _values_to_rgb(self, v1, v2, v3):
        def f(v):
            if isinstance(v, int) and 0 <= v < 256:
                return v / 255
            elif isinstance(v, float) and 0 <= v <= 1:
                return v

        def _(v):
            return int(v * 255)

        if self.colorspace == Color.RGB:
            return _(f(v1)), _(f(v2)), _(f(v3))
        elif self.colorspace == Color.HSV:
            return tuple(_(v) for v in colorsys.hsv_to_rgb(f(v1), f(v2), f(v3)))
        elif self.colorspace == Color.HLS:
            return tuple(_(v) for v in colorsys.hls_to_rgb(f(v1), f(v2), f(v3)))

        hue, sat, brightness = self.hsb
        hue2, luminance, sat2 = self.hls
        self.hue = int(hue * 255)
        self.hsb_sat = int(sat * 255)
        self.brightness = int(brightness * 255)
        self.luminance = int(luminance * 255)
        self.hls_sat = int(sat2 * 255)

    @property
    def redf(self):
        return self.red / 255

    @property
    def greenf(self):
        return self.green / 255

    @property
    def bluef(self):
        return self.blue / 255

    @property
    def rgb(self):
        return self.red, self.green, self.blue

    @property
    def hsb(self):
        return colorsys.rgb_to_hsv(self.redf, self.greenf, self.bluef)

    @property
    def hls(self):
        return colorsys.rgb_to_hls(self.redf, self.greenf, self.bluef)

    @property
    def hex(self):
        return '#' + ''.join(hex(v)[2:].zfill(2) for v in (self.rgb))


# Creating and reading color

def alpha(color):
    return color.alpha


def red(color):
    return color.red


def green(color):
    return color.green


def blue(color):
    return color.blue


def brightness(color):
    return color.brightness


def hue(color):
    return color.hue


def saturation(color):
    return color.hsb_sat


def lerp_color(color_from, color_to, amount):
    if not (0 <= amount <= 1):
        raise ValueError('`amount` must be between 0 and 1.')
    if float(amount) == 0:
        return color_from
    if float(amount) == 1:
        return color_to
    color_from = tuple(int((1 - amount) * v) for v in color_from.rgb)
    color_to = tuple(int(amount * v) for v in color_to.rgb)
    return Color(*(color_from + color_to))


# Setting colors

def stroke(color=0):
    pp = PyProcessing()
    color = Color(color)
    pp.namespace['stroke'] = color


def fill(color=255):
    pp = PyProcessing()
    color = Color(color)
    pp.namespace['fill'] = color


def background(color):
    pp = PyProcessing()
    color = Color(color)

    pp.windows.set_background(color)
