from math import (  # noqa
    ceil, dist as dist_, exp, floor,
    log, pow, sqrt,
)


def sq(n):
    return n * n


def constrain(amount, low, high):
    return min(max(amount, low), high)


def lerp(start, stop, amount):
    if not (0 <= amount <= 1):
        raise ValueError('`amount` must be between 0 and 1.')
    if float(amount) == 0:
        return start
    if float(amount) == 1:
        return stop
    return ((1 - amount) * start) + (amount * stop)


def dist(*args):
    if len(args) == 4:
        return dist_(args[:2], args[2:])
    elif len(args) == 6:
        return dist_(args[:3], args[3:])
    else:
        raise ValueError('Invalid number of arguments.')


def mag(a, b, c=0):
    if c == 0:
        return dist(0, 0, a, b)
    return dist(0, 0, 0, a, b, c)


def map(value, start1, stop1, start2, stop2):
    return (value - start1) * (stop2 - start2) / (stop1 - start1) + start2


def norm(value, start, stop):
    return map(value, start, stop, 0, 1)
