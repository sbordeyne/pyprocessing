from threading import Thread

from pyprocessing import PyProcessing


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
