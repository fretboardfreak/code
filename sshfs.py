#!/usr/bin/env python
""" sshfs.py is a simple interface around the sshfs tool to help manage
    multiple sshfs mountpoints.
"""
import sys, optparse, commands, os


# Global Script Options
SMS_BIN = '/local/sandc3/bin'
MOUNT_DIR = '/local/sandc3/sshfs'


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
        return 0
    print "Failure:"
    print output
    return status


def _prepareDestination(dest, opts):
    """ Make sure the destination directory exists.  If given a relative
        destination it will be placed under the MOUNT_DIR directory.
    """
    if not os.path.isabs(dest):
        dest = os.path.join(opts.mountDir, dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    return dest


def listMounts(opts):
    """ List the existing sshfs mountpoints on the system.
    """
    mountpoints = _getMountPoints()
    print '\n'.join(['%s: %s' % (count, mnt) for count, mnt in enumerate(mountpoints)])
    return 0


def mount(opts):
    """ Create an sshfs mount point
    """
    dest = _prepareDestination(opts.args.pop(-1), opts)
    opts.args.append(dest)
    cmd = 'sshfs %s' % ' '.join(opts.args)
    print 'Creating mountpoint: %s' % dest
    return _executeCommand(cmd)


def unmount(opts):
    """ Remove an existing sshfs mountpoint and clean up the target directories
        too.
    """
    cmdStr = "fusermount -u %s"
    mountpoints = _getMountPoints()

    cmd = ''
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
    if _executeCommand(cmd) == 0:
        os.rmdir(target)
        return 0
    return 1


def mountSms(opts):
    """ Convenience feature to mount the CLI dir of an SMS system with a
        corresponding "sms-system.sh" based script in the SMS_BIN directory.

        .. note::  The bash script just needs to print the IP address when
                   executed with the "-l" flag.
    """
    smsName = opts.args.pop()
    if not smsName in os.listdir(opts.smsBin):
        print "No sms-system.sh bash script for SMS '%s'" % smsName
        sys.exit(1)

    getIPCmd = "%s -l" % (os.path.join(opts.smsBin, smsName))
    status, ip = commands.getstatusoutput(getIPCmd)
    if status != 0:
        print "Couldn't retrieve IP address of requested SMS '%s'" % smsName
        print "Output of \"%s\": %s" % (getIPCmd, ip)
        sys.exit(1)

    dest = _prepareDestination(smsName, opts)
    cmd = "sshfs service@%s:/var/log/VPlex/cli %s" % (ip, os.path.join(opts.mountDir, dest))
    print 'Creating mountpoint: %s' % dest
    return _executeCommand(cmd)


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
    parser.add_option('-s', '--sms', dest='action', action='store_const',
                      const=mountSms, help="Mount an SMS system with using " +
                      "Curtis's \"sms-system.sh\" bash scripts.")

    opts, args = parser.parse_args()
    if not opts.action:
        opts.action = defaultAction

    opts.args = args

    return opts


def main():
    """ Execute the script.
    """
    opts = parseCmdLine(defaultAction=listMounts)

    opts.smsBin = SMS_BIN
    opts.mountDir = MOUNT_DIR

    return opts.action(opts)


if __name__ == '__main__':
    sys.exit(main())
