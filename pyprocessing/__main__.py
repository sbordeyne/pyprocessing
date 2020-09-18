#!/usr/bin/env python3.8

import argparse
import sys

from pyprocessing import __version__, __author__, Runner


def get_version():
    return f'PyProcessing v{__version__} by {", ".join(__author__)}'


def run(path, renderers):
    runner = Runner.from_sketch_path(args.path, args.renderers)
    runner.run()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

run_parser = subparsers.add_parser('run')
run_parser.add_argument('path', type=str)
run_parser.add_argument(
    '--tkinter', '-tk', dest='renderers',
    action='append_const', const='TkRenderer'
)
run_parser.set_defaults(callback=run)

parser.add_argument('--version', '-V', action='version', version=get_version())
args = vars(parser.parse_args())
callback = args.pop('callback')
sys.exit(callback(**args))
