#!/usr/bin/env python3

import argparse
import sys

from pyprocessing import __version__, __author__, Runner


def get_version():
    return f'PyProcessing v{__version__} by {", ".join(__author__)}'


def run(path, renderers, verbosity):
    runner = Runner.from_sketch_path(
        path, renderers=renderers, logging_level=verbosity
    )
    runner.run()


def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('path', type=str, help='Path to the sketch to run.')
    run_parser.add_argument(
        '--tkinter', '-tk', dest='renderers',
        action='append_const', const='TkRenderer',
        help='Renders the result in a Tcl/Tk window.'
    )
    run_parser.add_argument(
        '--verbosity', '-v', action='count', default=1,
        help=(
            'Verbosity level. Will set the logging level internally.'
            'Specify this flag multiple times for increased verbosity.'
        )
    )
    run_parser.set_defaults(callback=run)

    parser.add_argument(
        '--version', '-V', action='version',
        version=get_version()
    )
    args = vars(parser.parse_args())

    # This converts the verbosity flag into appropriate
    # log level values. I.e. -vv = logging.WARNING, -vvvv = logging.DEBUG
    args['verbosity'] = max((5 - args['verbosity']), 0) * 10
    return args


args = setup_parser()
callback = args.pop('callback')
sys.exit(callback(**args))
