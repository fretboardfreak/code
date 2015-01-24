#!/usr/bin/env python3
VERSION="0.0"
DESCRIPTION="Description of program. (Version: %s)" % VERSION

import sys, argparse

def parse_cmd_line():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    args, unknown = parser.parse_known_args()
    setattr(args, 'unknown', unknown)
    return args

def main():
    args = parse_cmd_line()
    return 0

if __name__ == '__main__':
    sys.exit(main())
