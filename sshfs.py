#!/usr/bin/env python
"""
Provides a wrapper around the 'sshfs' and 'fusermount' utilities to simplify
interactions with SSHFS mounts.
"""
import re
import os
import sys
import argparse
from subprocess import Popen, PIPE, STDOUT
from itertools import chain

VERSION = 'v0.1'


def main():
    parser = argparse.ArgumentParser(version=VERSION, description=__doc__)
    opts, args = parser.parse_known_args()

    sshfs = SSHFS()
    if len(args) == 0:
        sshfs.list_mountpoints()
    elif len(args) == 1:
        sshfs.unmount(args[0])
    elif len(args) == 2:
        sshfs.mount(args[0], args[1])


class Mountpoints(list):

    @staticmethod
    def load():
        mountpoints = Mountpoints()
        with open('/etc/mtab', 'r') as fin:
            for line in fin.readlines():
                if re.search('sshfs', line):
                    mountpoints.append(line.split(' ')[1])
        mountpoints.sort()
        return mountpoints

    def __str__(self):
        return '\n'.join(['%s: %s' % (count, mountpoint) for
                          count, mountpoint in enumerate(self)])


class SSHFS(object):

    def __init__(self):
        self.mountpoints = None
        self._load_mountpoints()
        self.sshfs_binary = '/usr/bin/sshfs'
        self.fusermount_binary = '/usr/bin/fusermount'
        self.mount_options = ['nonempty', 'allow_other', 'kernel_cache',
                              'auto_cache', 'reconnect', 'follow_symlinks',
                              'transform_symlinks']

    def _load_mountpoints(self):
        self.mountpoints = Mountpoints.load()

    def list_mountpoints(self):
        print self.mountpoints

    def _format_mount_options(self):
        return list(chain.from_iterable(zip(['-o'] * len(self.mount_options),
                                            self.mount_options)))

    def mount(self, source, dest):
        command = ([self.sshfs_binary] +
                   self._format_mount_options() +
                   [source, dest])
        if not os.path.exists(dest):
            os.mkdir(dest)
        _execute(command)
        self._load_mountpoints()

    def unmount(self, mountpoint):
        """Mountpoint can either be a path or an index for self.mountpoints"""
        err_msg = ("The given mountpoint '%s' doesn't appear to exist." %
                   mountpoint)
        if isinstance(mountpoint, int):
            try:
                mountpoint = self.mountpoints[mountpoint]
            except IndexError:
                raise Exception(err_msg)
        elif not os.path.exists(mountpoint):
            raise Exception(err_msg)

        command = [self.fusermount_binary, '-u', mountpoint]
        _execute(command)

        try: # remove mountpoint if empty
            os.rmdir(mountpoint)
        except OSError, e: # ignore error if directory not empty
            if e.args[0] == 39 and 'not empty' in e.args[1].lower():
                pass
        self._load_mountpoints()


def _execute(cmd):
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    output, _ = proc.communicate()
    if proc.returncode:
        print "Subcommand Failed:\n%s" % output
    return proc.returncode


if __name__ == '__main__':
    sys.exit(main())
