from pyprocessing import (
    size, cursor, no_cursor,
    CursorType, PPVariables,
)


def setup():
    size(600, 500)


def draw():
    var = PPVariables()
    if var.mouse_pressed:
        no_cursor()
    else:
        if var.mouseX < 100:
            cursor(CursorType.CROSS)
        elif var.mouseX < 200:
            cursor(CursorType.HAND)
        elif var.mouseX < 300:
            cursor(CursorType.MOVE)
        elif var.mouseX < 400:
            cursor(CursorType.TEXT)
        elif var.mouseX < 500:
            cursor(CursorType.ARROW)
        else:
            cursor(CursorType.WAIT)
