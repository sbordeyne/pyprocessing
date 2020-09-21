import colorsys

from pyprocessing import PyProcessing


class Color:
    RGB = 1
    HLS = 2
    HSB = 3
    
    colorspace = RGB
    maxv1 = maxv2 = maxv3 = maxva = 255

    def __init__(self, *args, colorspace=0):
        
        self.colorspace = colorspace
        def adjust(val, max):
            if val > max:
                return 255
            return round((val / max) * 255)

        def adjusttuple(tup, maxes):
            return (adjust(i, j) for i, j in zip(tup, maxes))

        if len(args) == 1:
            # 1 argument : no matter the colorspace, it's grayscale
            self.red = adjust(args[0], self.maxv1)
            self.green = adjust(args[0], self.maxv2)
            self.blue = adjust(args[0], self.maxv3)
            self.alpha = 255
        elif len(args) == 2:
            self.red = adjust(args[0], self.maxv1)
            self.green = adjust(args[0], self.maxv2)
            self.blue = adjust(args[0], self.maxv3)
            self.alpha = adjust(args[1], self.maxva)
        elif len(args) == 3:
            self.alpha = 255
            self.red, self.green, self.blue = self._values_to_rgb(*adjusttuple(  # Adjust vals then unpack and convert
                args, (self.maxv1, self.maxv2, self.maxv3)                       # Terribly done by Peanutbutter_Warrior
            ))
        elif len(args) == 4:
            v1, v2, v3, self.alpha = adjusttuple(args, (self.maxv1, self.maxv2, self.maxv3, self.maxva))
            self.red, self.green, self.blue = self._values_to_rgb(v1, v2, v3)
    
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
        elif self.colorspace == Color.HSB:
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

def stroke(*colors):
    pp = PyProcessing()
    color = Color(*colors)
    pp.namespace['stroke'] = color


def no_stroke():
    pp = PyProcessing()
    pp.namespace['stroke'] = None


def fill(*colors):
    pp = PyProcessing()
    color = Color(*colors)
    pp.namespace['fill'] = color


def no_fill():
    pp = PyProcessing()
    pp.namespace['fill'] = None


def background(color):
    pp = PyProcessing()
    color = Color(color)
    pp.windows.set_background(color)


def color_mode(mode, *args):
    if mode != 1 and mode != 3:
        raise ValueError('Invalid color mode. Valid modes are 1 (RGB) and 3 (HSB)')
    
    Color.colorspace = mode
    if len(args) == 0:
        pass
    elif len(args) == 1:
        Color.maxv1 = Color.maxv2 = Color.maxv3 = Color.maxva = args[0]
    elif len(args) == 3:
        Color.maxv1, Color.maxv2, Color.maxv3 = args
    elif len(args) == 4:
        Color.maxv1, Color.maxv2, Color.maxv3, Color.maxva = args
    else:
        raise ValueError(f'Invalid amount of maximums. Accepts 1, 3, or 4. (found {len(args)})')
