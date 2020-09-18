import datetime
import time

from pyprocessing import pp


def second():
    return datetime.datetime.now().second


def minute():
    return datetime.datetime.now().minute


def hour():
    return datetime.datetime.now().hour


def day():
    return datetime.datetime.now().day


def month():
    return datetime.datetime.now().month


def year():
    return datetime.datetime.now().year


def millis():
    return int((time.time_ns() - pp.start_time_ns) / 1_000_000)
