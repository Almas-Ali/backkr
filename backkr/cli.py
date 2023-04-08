import argparse

from backkr import __version__
from backkr.cli import Backkr


def main():
    parser = argparse.ArgumentParser(
        description='Backkr is a backend framework the web')

    parser.add_argument('--version', action='version',
                        version=f'Backkr {__version__}')
    parser.add_argument('createproject', help='Create a new project')
    parser.add_argument('start', help='Start the server')

    args = parser.parse_args()

    if args.createproject:
        print(f'Creating project {args.createproject}')

    elif args.start:
        print(f'Starting server at {args.start}')

    else:
        parser.print_help()
