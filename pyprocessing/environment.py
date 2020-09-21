from time import sleep
import tkinter
import ctypes
import platform

from pyprocessing import PyProcessing, width, height  # noqa


def size(w, h):
    pp = PyProcessing()
    global width
    global height
    pp.namespace['width'] = w
    pp.namespace['height'] = h
    width = w
    height = h
    pp.width = w
    pp.height = h


def frame_rate(fr=60):
    pp = PyProcessing()
    pp.namespace['framerate'] = fr


def delay(nap_time):
    sleep(nap_time / 1_000)


def display_density(display=0):
    if platform.system() != 'Windows':
        raise NotImplementedError()

    MM_TO_IN = 0.0393700787

    # Set process DPI awareness
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # Create a tkinter window
    root = tkinter.Tk()
    # Get a DC from the window's HWND
    dc = ctypes.windll.user32.GetDC(root.winfo_id())
    # The the monitor phyical width
    # (returned in millimeters then converted to inches)
    mw = ctypes.windll.gdi32.GetDeviceCaps(dc, 4) * MM_TO_IN
    # The the monitor phyical height
    mh = ctypes.windll.gdi32.GetDeviceCaps(dc, 6) * MM_TO_IN
    # Get the monitor horizontal resolution
    dw = ctypes.windll.gdi32.GetDeviceCaps(dc, 8)
    # Get the monitor vertical resolution
    dh = ctypes.windll.gdi32.GetDeviceCaps(dc, 10)
    # Destroy the window
    root.destroy()

    # Diagonal DPI calculated using Pythagoras
    ddpi = round((dw ** 2 + dh ** 2) ** 0.5 / (mw ** 2 + mh ** 2) ** 0.5, 1)
    if ddpi <= 213:
        return 1
    return 2
