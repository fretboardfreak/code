#!/usr/bin/env python
""" FSRecurser
"""
import re, os, sys, logging
import pyLib.libMisc as libMisc

DEBUG = False
LOG = logging.getLogger('FSRecurser')

class FSRecurser:
    def __init__(self, directory, accumulator):
        self.directory = os.path.abspath(directory)
        self.accumulator = accumulator
        self._setup()

    def _setup(self):
        self._assertValidDirectory()
        self.genericExcludePatterns = ['^\.']
        self.excludedDirectoryPatterns = []
        self.excludedFilePatterns = []

    def _assertValidDirectory(self):
        """ Make sure given directory exists.
        """
        tests = {os.path.exists: "Given path '%s' does not exist",
                 os.path.isdir: "Given path '%s' is not a directory"}
        for test, msg in tests.iteritems():
            if not test(self.directory):
                raise IOError(msg % self.directory)
        LOG.debug('FSRecurser: directory is valid')

    def recurse(self):
        """ Walk through the directory, visiting files and accumulating results.
        """
        for current, dirs, files in os.walk(self.directory):
            LOG.debug('Recursing through %s' % current)
            LOG.debug('Removing excluded dirs...')
            self._removeExcluded(dirs, self.excludedDirectoryPatterns)
            LOG.debug('Removing excluded files...')
            self._removeExcluded(files, self.excludedFilePatterns)
            LOG.debug('Visiting files...')
            self.accumulator.visitFiles(current, files)

    def _removeExcluded(self, items, patterns):
        """ If one of the patterns matches with one of the items, remove the
            item from the list. Note: The generic exclude patterns are always
            used here.
        """
        for item in items[:]:
            for pattern in patterns + self.genericExcludePatterns:
                if re.search(pattern, item):
                    items.remove(item)

class Accumulator:
    def __init__(self):
        self.data = ""

    def visitFiles(self, current, files):
        self.data += '\n'.join([os.path.join(current, fname) for fname in files]) + '\n'

if __name__=="__main__":
    if len(sys.argv) < 2:
        raise Exception('FSRecurser expects at least one path ')
    for path in sys.argv[1:]:
        print "FSRecurser: %s" % sys.argv[1]
        acc = Accumulator()
        fsr = FSRecurser(sys.argv[1], acc)
        results = fsr.recurse()
        print results.replace('\n', '\n    ')
    sys.exit(0)
