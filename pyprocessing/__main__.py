#!/usr/bin/env python3

import argparse
import pathlib
import sys

from pyprocessing import __version__, __author__, Runner, Converter


def get_version():
    return f'PyProcessing v{__version__} by {", ".join(__author__)}'


<<<<<<< HEAD
def run(path, renderers, verbosity):
    # This converts the verbosity flag into appropriate
    # log level values. I.e. -vv = logging.WARNING, -vvvv = logging.DEBUG
    verbosity = max((5 - verbosity), 0) * 10

    runner = Runner.from_sketch_path(
        path, renderers=renderers, logging_level=verbosity
    )
=======
def run(path, renderers):
    runner = Runner.from_sketch_path(args.path, args.renderers)
>>>>>>> parent of a6acebd... Merge pull request #2 from Dogeek/master
    runner.run()


def convert(path):
    path = pathlib.Path(path)
    converter = Converter.from_path(path)
    fname = path.stem + '_converted.py'
    with open(path.parent.joinpath(fname), 'w') as f:
        f.write(str(converter))


def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('path', type=str)
    run_parser.add_argument(
        '--tkinter', '-tk', dest='renderers',
        action='append_const', const='TkRenderer'
    )
    run_parser.set_defaults(callback=run)

<<<<<<< HEAD
    convert_parser = subparsers.add_parser('convert')
    convert_parser.add_argument(
        'path', type=str,
        help='Path to the processing sketch to convert to PyProcessing syntax.'
    )
    convert_parser.set_defaults(callback=convert)

    parser.add_argument(
        '--version', '-V', action='version',
        version=get_version()
    )
    args = vars(parser.parse_args())

    return args
=======
    parser.add_argument('--version', '-V', action='version', version=get_version())
    return vars(parser.parse_args())
>>>>>>> parent of a6acebd... Merge pull request #2 from Dogeek/master


args = setup_parser()
callback = args.pop('callback')
sys.exit(callback(**args))
