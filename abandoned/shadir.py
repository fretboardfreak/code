#!/usr/bin/env python
""" shadir : Generate a checksum for a directory of files.

    Note: The calculated hash depends on the input path in most situations.
          For consistent results make sure you call shadir with the same
          arguments.  Bash wildcard expansion needs to be taken into account
          because './' != './*' since bash will expand the latter to './<file1>
          ./<file2> ...'.
"""
DEBUG = False

import os, sys, optparse, subprocess, hashlib
import pyLib.libMisc as libMisc
from pyLib.fsRecurser import FSRecurser

libMisc.setupLogging()
LOG = libMisc.getLogger(__name__, DEBUG)

def parseCmdLine():
    """
    manage cli invocation
    """
    usage = '%prog <path>'
    version = '%prog v1.0'
    description = __doc__
    parser = optparse.OptionParser( usage = usage,
                           version = version,
                           description = description )
    parser.add_option('-s', '--singlesha', dest='single', action="store_true",
            default=False,
            help="When enabled, Single SHA mode will combine all"
                 "calculated SHAs into a single SHA.  This is useful for"
                 "when you want to monitor a set of distinct paths for"
                 "changes.")
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    return opts, args

class ShaAccumulator:
    def __init__(self):
        self.shas = ""

    def getResults(self):
        return hashlib.sha1(self.shas).hexdigest()

    def visitFiles(self, current, files):
        newSha = libMisc.calculateSha(' '.join([os.path.join(current, f)
                                                for f in files]))
        if not newSha:
            return
        self.shas += newSha.strip('\n')

def getDirectorySha(directory):
    shaAcc = ShaAccumulator()
    fsr = FSRecurser(directory, shaAcc)
    fsr.genericExcludePatterns = []
    fsr.recurse()
    return shaAcc.getResults()

def main():
    opts, args = parseCmdLine()
    argShas = ''
    LOG.info('shadir: calculating shaw for "%s"' % str(args))
    shaCount = 0
    for directory in args:
        if not os.path.isdir(directory) and os.path.isfile(directory):
            newShaw = libMisc.calculateSha(directory)
            LOG.debug('new file sha: %s' % newShaw)
        else:
            newShaw = getDirectorySha(directory) + '  %s' % directory
            LOG.debug('new dir shaw: %s' % newShaw)
        argShas += newShaw + '\n'
        shaCount += 1
    if opts.single and shaCount > 1:
        LOG.info('Hashing multiple shas into a single sha...')
        sys.stdout.write(hashlib.sha1(argShas).hexdigest() + '\n')
    else:
        LOG.debug('found single sha...')
        sys.stdout.write(argShas.split('  ')[0] + '\n')
    return 0

if __name__ == '__main__':
    sys.exit(main())
