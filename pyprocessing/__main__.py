#!/usr/bin/env python3.8

import argparse

from pyprocessing import __version__, __author__, Runner


def get_version():
    return f'PyProcessing v{__version__} by {", ".join(__author__)}'


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str)
parser.add_argument(
    '--tkinter', '-tk', dest='renderers',
    action='append_const', const='TkRenderer'
)
parser.add_argument('--version', '-V', action='version', version=get_version())
args = parser.parse_args()

runner = Runner.from_sketch_path(args.path, args.renderers)
runner.run()
