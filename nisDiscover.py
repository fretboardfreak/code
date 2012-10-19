#!/usr/bin/env python
""" nisDiscover.py discovers all of the details of the nis maps available
    through the system's default map and writes a report.
"""
import os, sys, optparse, nis, time

def parseCmdLine():
    """
    manage cli invocation
    """
    usage = '%prog REPORTFILE'
    version = '%prog v0.0'
    description = __doc__
    parser = optparse.OptionParser( usage = usage,
                           version = version,
                           description = description )
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('%prog expects 1 positional argument, REPORTFILE.')

    return (opts, args)

def getTitle():
    ts = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
    return "%s\n%s\n" % (ts, '-' * len(ts))

def main():
    opts, args = parseCmdLine()
    logFile = args[0]
    if os.path.exists(logFile):
        raise Exception('Please choose a REPORTFILE that does not yet exist.')

    maps = nis.maps()
    with open(logFile, 'w') as log:
        log.write(getTitle())
        log.write('\nNIS Maps of domain: %s\n' % nis.get_default_domain())
        for mapname in maps:
            log.write('\n%s:\n' % mapname)
            entries = nis.cat(mapname)
            for key, value in entries.iteritems():
                log.write('  "%s" : "%s"\n' % (key, value))
            log.write('\n' + '-' * 80 + '\n')

    return 0

if __name__ == '__main__':
    sys.exit(main())
