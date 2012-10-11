#!/usr/bin/env python
"""
"""
import sys, optparse

def parseCmdLine():
    """
    manage cli invocation
    """
    usage = '%prog'
    version = '%prog v0.0'
    description = __doc__
    parser = optparse.OptionParser( usage = usage,
                           version = version,
                           description = description )
    return parser.parse_args()

def main():
    opts, args = parseCmdLine()
    print ' '.join(args)
    return 0

if __name__ == '__main__':
    sys.exit(main())
