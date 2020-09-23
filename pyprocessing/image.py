import pathlib

from PIL import Image, ImageTk, ImageQt


class _PixelsProxy(list):
    def __init__(self, image):
        self.image = image
        super().__init__(self.image.getdata())

    def __setitem__(self, index, value):
        x = index // self._image.width
        y = index % self._image.width
        self._image.putpixel((x, y), value)


class PImage:
    def __init__(self, path_or_img):
        if isinstance(path_or_img, (str, pathlib.Path)):
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

    def filter(self):
        pass

    def copy(self):
        pass

    def blend(self):
        pass

    def save(self):
        pass
