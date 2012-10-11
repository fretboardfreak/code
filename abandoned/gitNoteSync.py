#!/usr/bin/env python
'''
Sync markdown notes with an external folder like dropbox.

Notes will be named *.txt in the external folder and *.md in git.
The script will use proper git commands to do things such as, delete or add new files to git and reflect any git-side changes in the external folder.

This script is intended for use with cron to keep the external folder synced up.
'''
import sys, optparse

def parseCmdLine():
    '''
    manage cli invocation
    '''
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
    try:
        sys.exit( main() )
    except KeyboardInterrupt:
        print 'Interrupted by User.'
        sys.exit( 1 )


