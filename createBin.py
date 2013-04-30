#!/usr/bin/env python
""" Create a bin directory that symlinks the various scripts and
    tools from my code repository.
"""
import sys, os


if __name__ == "__main__":
    usage = "createBin.py [code-repo] [new-bin]"
    symlinks = {  # filename: linkname,
                'alarm': 'alarm',
                'centurion': 'centurion',
                'detach': 'detach',
                'm3u.sh': 'm3u',
                'msgOn': 'msgOn',
                'nisDiscover.py': 'nisDiscover',
                'pidwatch.py': 'pidwatch',
                'processSnitch.py': 'processSnitch',
                'pygrep': 'pygrep',
                'random': 'random',
                'rd-back.sh': 'backup',
                'rmpyc': 'rmpyc',
                'sshfs.py': 'sfs',
                'timer': 'timer',
                'tree': 'tree',
                'tsrename.sh': 'tsrename',
                'wikiLookup.sh': 'wikiLookup'
                }

    args = sys.argv[:]
    args.pop(0)
    print args
    if ("-h" in args) or ('--help' in args) or (len(args) != 2):
        print usage
        sys.exit(0)

    repo = args[0]
    if not os.path.exists(repo):
        print usage
        sys.exit(0)

    bin = args[1]
    if not os.path.exists(bin):
        print "Creating new bin directory..."
        os.mkdir(bin)

    skipped = []
    for fname, link in symlinks.iteritems():
        src = os.path.join(repo, fname)
        dest = os.path.join(bin, link)
        if not os.path.exists(src):
            skipped.append(fname)
        print "linking %s -> %s" % (src, dest)
        os.symlink(src, dest)

    print "The following links are not available: %s" % skipped
