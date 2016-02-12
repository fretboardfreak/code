#!/usr/bin/env python3
"""A demo implementation of a UI spinner."""

import sys, argparse
import time


VERSION = "1.0"


def main():
    args = parse_cmd_line()
    spinner1 = '-/|\\'
    spinner2 = 'v<^>'
    while True:
        for sequence in [spinner1, spinner2]:
            for _ in range(5):
                cycle_spinner(sequence)
    return 0


def cycle_spinner(char_sequence):
    stdout = sys.stdout
    for char in char_sequence:
        stdout.write(char)
        stdout.flush()
        time.sleep(0.3)
        stdout.write('\b\b\b')
        stdout.flush()


def parse_cmd_line():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', help='Print the version and exit.', action='version',
        version='%(prog)s {}'.format(VERSION))
    return parser.parse_args()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if DEBUG:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
