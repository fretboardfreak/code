#!/usr/bin/env python
""" sshfs.py is a simple interface around the sshfs tool to help manage
    multiple sshfs mountpoints.
"""
import sys, optparse, commands, os


def _getMountPoints():
    """ Run the bash command: grep sshfs /etc/mtab | cut -f 2 -d ' '; to get
        the list of sshfs mount points.
    """
    mountpoints = commands.getoutput("grep sshfs /etc/mtab | cut -f 2 -d ' '").strip().split()
    if not mountpoints:
        print "No mounts found"
        sys.exit(0)

    mountpoints.sort()
    return mountpoints


def _executeCommand(cmd):
    """ Execute a bash command and print the results.
    """
    status, output = commands.getstatusoutput(cmd)
    if status == 0:
        return
    print "Failure:"
    print output


def listMounts(opts):
    mountpoints = _getMountPoints()
    print '\n'.join(['%s: %s' % (count, mnt) for count, mnt in enumerate(mountpoints)])


def mount(opts):
    """ Create an sshfs mount point
    """
    dest = opts.args.pop(-1)
    if not os.path.isabs(dest):
        dest = os.path.join(opts.mountDir, dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    opts.args.append(dest)
    cmd = 'sshfs %s' % ' '.join(opts.args)
    print 'Creating mountpoint: %s' % dest
    _executeCommand(cmd)


def unmount(opts):
    cmdStr = "fusermount -u %s"
    mountpoints = _getMountPoints()

    target = opts.args.pop(0)
    if os.path.exists(target) and target in mountpoints:
        cmd = cmdStr % target
    elif len(target) == 1:
        try:
            targetIndex = int(target)
        except:
            print "Could not interpret which mountpoint to remove: %s" % target
            sys.exit(1)
        target = mountpoints.pop(targetIndex)
        cmd = cmdStr % target
    print  "Removing mountpoint: %s" % target
    _executeCommand(cmd)
    os.rmdir(target)


def parseCmdLine(defaultAction):
    """
    manage cli invocation
    """
    usage = '%prog [action] [options]'
    version = '%prog v0.1'
    description = __doc__
    parser = optparse.OptionParser(usage=usage, version=version,
                                   description=description )
    parser.add_option('-m', '--mount', dest='action', action='store_const',
                      const=mount, help="Create new mount point. Uses the same syntax as sshfs.")
    parser.add_option('-u', '--unmount', dest='action', action='store_const',
                      const=unmount, help="Remove an existing mountpoint.")
    parser.add_option('-l', '--list', dest='action', action='store_const',
                      const=listMounts, help="List existing mountpoints. [default action]")

    opts, args = parser.parse_args()
    if not opts.action:
        opts.action = defaultAction

    opts.args = args

    return opts

def main():
    opts = parseCmdLine(defaultAction=listMounts)
    opts.mountDir = '/local/sandc3/sshfs'

    opts.action(opts)

    return 0

if __name__ == '__main__':
    sys.exit(main())
