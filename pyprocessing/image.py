from base64 import b64decode
from enum import Enum, IntEnum
from io import BytesIO
import os.path
import pathlib

from PIL import (
    Image, ImageFilter, ImageOps,
    ImageQt, ImageTk,
)
import requests

from pyprocessing.utils import url_re


__all__ = (
    'PImage', 'FilterKind', 'ImageFormat',
    'create_image',
)


class _PixelsProxy(list):
    def __init__(self, image):
        self.image = image
        super().__init__(self.image.getdata())

    def __setitem__(self, index, value):
        x = index % self._image.width
        y = index // self._image.width
        self._image.putpixel((x, y), value)


class ImageFormat(IntEnum):
    RGB = 0
    ARGB = 1
    ALPHA = 2


class FilterKind(IntEnum):
    THRESHOLD = 0
    GRAY = 1
    OPAQUE = 2
    INVERT = 3
    POSTERIZE = 4
    BLUR = 5
    ERODE = 6
    DILATE = 7


class _FilterKindParamDefault(Enum):
    THRESHOLD = 0.5
    GRAY = None
    OPAQUE = None
    INVERT = None
    POSTERIZE = None
    BLUR = 1
    ERODE = None
    DILATE = None


def _threshold_filter(image, threshold):
    if isinstance(threshold, float):
        threshold *= 256
    gray = image.convert(mode='L')
    mapping = [0, 255]
    for i, pixel in enumerate(gray.getdata()):
        x = i % gray.width
        y = i // gray.width
        gray.putpixel((x, y), mapping[pixel <= threshold])
    return gray


def _gray_filter(image):
    return ImageOps.grayscale(image)


def _opaque_filter(image):
    return image.putalpha(0)


def _invert_filter(image):
    return ImageOps.invert(image)


def _posterize_filter(image, bits):
    if bits > 8:
        bits = bits // 8
    bits = min(max(bits, 1), 8)
    return ImageOps.posterize(image, bits)


def _blur_filter(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius))


def _erode_filter(image):
    return image.filter(ImageFilter.MinFilter(3))


def _dilate_filter(image):
    return image.filter(ImageFilter.MaxFilter(3))


class PImage:
    def __init__(self, path_or_img):
        if isinstance(path_or_img, str) and path_or_img.startswith('base64:'):
            self.path = None
            self._image = Image.open(
                BytesIO(b64decode(path_or_img[len('base64:'):]))
            )
        elif isinstance(path_or_img, (str, pathlib.Path)):
            self.path = pathlib.Path(path_or_img)
            self._image = Image.open(str(self.path))
        elif isinstance(path_or_img, Image.Image):
            self.path = None
            self._image = path_or_img
        else:
            raise TypeError((
                'Expected str, pathlib.Path or PIL.Image.Image type '
                f'for `path_or_img`, got {type(path_or_img)}'
            ))

    def __copy__(self):
        return PImage(self._image.copy())

    @property
    def pixels(self):
        return _PixelsProxy(self._image)

    @property
    def tk_photo_image(self):
        return ImageTk.PhotoImage(self._image)

    @property
    def qt_image(self):
        return ImageQt.ImageQt(self._image)

    def load_pixels(self):
        '''Not needed, pixels are automatically loaded on class creation'''

    def update_pixels(self):
        '''Not needed, pixels update automatically on mutation.'''

    def resize(self, width, height):
        if not width and not height:
            raise ValueError('`width` and `height` cannot be both zero.')

        if width == 0:
            aspect_ratio = self._image.width / self._image.height
            width = height * aspect_ratio
        if height == 0:
            aspect_ratio = self._image.height / self._image.width
            height = width * aspect_ratio
        self._image = Image.resize((width, height))

    def get(self):
        pass

    def set(self):
        pass

    def mask(self):
        pass

    def filter(self, kind, param=None):
        filters = {
            FilterKind.THRESHOLD: _threshold_filter,
            FilterKind.GRAY: _gray_filter,
            FilterKind.OPAQUE: _opaque_filter,
            FilterKind.INVERT: _invert_filter,
            FilterKind.POSTERIZE: _posterize_filter,
            FilterKind.BLUR: _blur_filter,
            FilterKind.ERODE: _erode_filter,
            FilterKind.DILATE: _dilate_filter,
        }
        if kind not in filters:
            raise ValueError(f'Kind {kind} not in available filters.')
        image_filter = filters[kind]
        arg = _FilterKindParamDefault[FilterKind(kind).name].value
        if arg is None and kind == FilterKind.POSTERIZE:
            raise ValueError('Kind FilterKind.POSTERIZE requires an argument.')

        if arg is None:
            return image_filter(self._image)
        return image_filter(self._image, arg)

    def copy(self):
        pass

    def blend(self):
        pass

    def save(self, filename):
        fname, ext = os.path.splitext(filename)
        if not ext:
            ext = 'tiff'
        filename = f"{fname}.{ext}"
        self._image.save(filename)
        return True


def create_image(width, height, format):
    if format == ImageFormat.RGB:
        format = 'RGB'
    elif format == ImageFormat.ARGB:
        format = 'RGBA'
    else:
        format = 'LA'
    pil_image = Image.new(format, (width, height))
    return PImage(pil_image)


def load_image(url, extension=None):
    if url_re.match(url):
        pil_image = Image.open(requests.get(url, stream=True).raw)
    else:
        pil_image = Image.open(url)
    return PImage(pil_image)
