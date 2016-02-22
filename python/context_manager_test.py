#!/usr/bin/env python3

"""
This script was used to verify the behaviour of nested context managers in
python 3.
"""

import tempfile
from contextlib import contextmanager

@contextmanager
def first_manager():
    print('Entering First Manager')
    yield
    print('Exiting First Manager')

@contextmanager
def second_manager(argument=None):
    print("Entering Second Manager: {}".format(argument))
    yield
    print("Exiting Second Manager")


if __name__ == "__main__":
    print('Running nested context manager test...')
    with first_manager(), \
            tempfile.TemporaryDirectory() as temp_dir, \
            second_manager(temp_dir):
        print('Inside context')
        print('temp dir = {}'.format(temp_dir))
    print('Done')
