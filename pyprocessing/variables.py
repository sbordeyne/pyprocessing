from pyprocessing.utils import SingletonMeta


class PPVariables(metaclass=SingletonMeta):
    mouseX = 0
    mouseY = 0
    mouse_pressed = False
