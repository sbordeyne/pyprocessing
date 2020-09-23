from threading import Thread

from pyprocessing import PyProcessing
from pyprocessing.image import PImage
from pyprocessing.utils import SingletonMeta


class PyProcessingThread(Thread):
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()


def thread(thread_name):
    pp = PyProcessing()
    callback = pp.callables[thread_name]
    thread = PyProcessingThread(callback)
    if not hasattr(callback, '__timeout__'):
        timeout = None
    else:
        timeout = callback.__timeout__
    thread.join(timeout)


def timeout(timeout=30.):
    '''
    Decorator that sets the timeout for a function, when used as a threading
    callback

    :param timeout: The timeout of the thread, defaults to 30 seconds
    :type timeout: float, optional
    '''
    def wrapper(func):
        nonlocal timeout
        func.__timeout__ = timeout
        return func
    return wrapper


class PSurface(metaclass=SingletonMeta):
    def __init__(self):
        self.pp = PyProcessing()

    def set_location(self, x, y):
        self.pp.namespace['window_offset'] = (x, y)
        self.pp.renderers.update_location()

    def set_resizable(self, resizable):
        self.pp.namespace['window_resizable'] = (resizable, resizable)
        self.pp.renderers.update_resizable()

    def set_title(self, title):
        self.pp.namespace['window_title'] = title
        self.pp.renderers.update_title()

    def set_size(self, width, height):
        self.pp.namespace['width'] = width
        self.pp.namespace['height'] = height
        self.pp.renderers.update_size()

    def set_icon(self, image):
        if not isinstance(image, PImage):
            raise TypeError(
                f'Argument `image` is not of type PImage. Type: {type(image)}'
            )
        self.pp.namespace['window_icon'] = image
        self.pp.renderers.update_icon()
