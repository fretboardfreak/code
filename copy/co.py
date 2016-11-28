#!/usr/bin/env python3
"""An rsync wrapper to simplify syncing multiple filesystems from a master.

For each DIR argument given, the local path will be transferred to the same
absolute path on the remote hosts listed in the config file. For example,
"co.py /home/user/mydir" will transfer the contents of the "mydir" directory to
the matching path, "/home/user", on each of the remote hosts listed.
"""

import os
import sys
import argparse
import enum
import subprocess
import configparser


VERSION = "0.1"
VERBOSE = False
DEBUG = False


def build_rsync_command(source, dest, host, excludes=None, erase=True,
                        output_flags=None):
    if not excludes:
        excludes = []
    if not output_flags:
        output_flags = []
    command = ['rsync', '--inplace', '-ha']
    if erase:
        command.append('--delete')
    for pattern in excludes:
        command.append('--exclude')
        command.append(pattern)
    command.extend(output_flags)

    command.append(source)
    full_dest = "%s:%s" % (host, dest)
    command.append(full_dest)
    return command


def sanitize_source(path):
    """Ensure the source does not have a trailing /"""
    return path[:-1] if path.endswith('/') else path


def sanitize_dest(path):
    """Ensure the destination does have a trailing /"""
    return path if path.endswith('/') else path + '/'


def main():
    command_parser = CommandParser()
    args = command_parser.parse()
    dprint(args)

    cfg = Config(filename=args.config)
    cfg.load()

    for argument in args.dir:
        if not os.path.exists(argument):
            print('Path "%s" does not appear to exist, skipping...' %
                  argument)
            continue
        argument = os.path.abspath(os.path.relpath(argument))
        source_path = sanitize_source(argument)
        if not args.dest:
            parent, _ = os.path.split(source_path)
            dest_path = sanitize_dest(parent)
        else:
            dest_path = args.dest
        excludes = cfg.rsync_excludes if not args.no_excludes else []
        for hostname in cfg.hosts:
            print('Transfering "%s" to "%s" on %s...' %
                  (source_path, dest_path, hostname))
            command = build_rsync_command(
                source_path, dest_path, cfg.hosts[hostname], excludes,
                args.erase, cfg.rsync_output_flags)
            dprint('Running command: %s' % ' '.join(command))
            if not args.dry_run:
                subprocess.call(command, stderr=subprocess.PIPE)

    return 0


class Config(object):
    """Wrapper interface for an INI Config Parser object."""

    # Default Config Locations: Home dir, current dir, script's dir
    default_filename = 'co.cfg'
    default_paths = [os.path.join(os.environ['HOME'],
                                  '.%s' % default_filename),
                     os.path.join('.', default_filename),
                     os.path.join(os.path.dirname(sys.argv[0]),
                                  default_filename)]

    def __init__(self, filename=None):
        self.filename = filename
        if not self.filename:
            self.filename = self.default_paths
        self._parser = configparser.ConfigParser()

    def load(self):
        self._parser.read(self.filename)

    def get_string(self, sect, opt):
        if (not self._parser.has_section(sect)
                or opt not in self._parser.options(sect)):
            return None
        return self._parser.get(sect, opt)

    def get_list(self, sect, opt):
        if (not self._parser.has_section(sect)
                or opt not in self._parser.options(sect)):
            return None
        return self._parser.get(sect, opt).split(' ')

    @property
    def hosts(self):
        sect = 'hosts'
        if not self._parser.has_section(sect):
            return {}
        return {opt: self._parser.get(sect, opt)
                for opt in self._parser.options(sect)}

    def iter_hosts(self):
        for index, hostname in enumerate(sorted(self.hosts.keys())):
            yield (index, hostname)

    @property
    def rsync_excludes(self):
        return self.get_list('rsync_opts', 'excludes')

    @property
    def rsync_output_flags(self):
        return self.get_list('rsync_opts', 'output_flags')

    @property
    def defaults_dir(self):
        return self.get_string('defaults', 'dir')

    @property
    def defaults_dest(self):
        return self.get_string('defaults', 'dest')

    @property
    def reverse_defaults_dir(self):
        return self.get_string('reverse_defaults', 'dir')

    @property
    def reverse_defaults_dest(self):
        return self.get_string('reverse_defaults', 'dest')

    @property
    def reverse_defaults_host(self):
        return self.get_string('reverse_defaults', 'host')


class CommandParser(object):
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description=__doc__)

    def add_options(self):
        self.arg_parser.add_argument(
            '--version', help='Print the version and exit.', action='version',
            version='%(prog)s {}'.format(VERSION))
        DebugAction.add_parser_argument(self.arg_parser)
        VerboseAction.add_parser_argument(self.arg_parser)
        self.arg_parser.add_argument(
            '-n', '--dry-run', action='store_true', dest='dry_run',
            help="Print full output but do not run rsync.")
        self.arg_parser.add_argument(dest='dir', metavar='DIR', nargs='*')
        self.arg_parser.add_argument(
            '-c', '--config', action='store', dest='config', metavar='CONFIG',
            help=('Specify a config file to use. Default config paths: %s' %
                  ' '.join(Config.default_paths)))
        self.arg_parser.add_argument(
            '--no-excludes', dest='no_excludes', action='store_true',
            help="Don't use the rsync excludes option from the config file.")
        self.arg_parser.add_argument(
            '-e', '--erase', dest='erase', action='store_true',
            help="Include the --erase option in the rsync commands.")
        self.arg_parser.add_argument(
            '-D', '--dest', dest='dest', metavar="DESTINATION",
            help=("Specify an alternate destination path. Otherwise the "
                  "same source path is used on each host destination."))

    def set_defaults(self):
        self.arg_parser.set_defaults(dir=[os.environ.get('HOME', '')],
                                     config=None, no_excludes=False,
                                     erase=False, dry_run=False, dest=None)

    def parse(self):
        self.add_options()
        self.set_defaults()
        return self.arg_parser.parse_args()


def dprint(msg):
    """Conditionally print a debug message."""
    if DEBUG:
        print(msg)


def vprint(msg):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(msg)


class DebugAction(argparse.Action):
    """Enable the debugging output mechanism."""

    short_flag = '-d'
    flag = '--debug'
    help = 'Enable debugging output.'

    @classmethod
    def add_parser_argument(cls, parser):
        if hasattr(cls, 'short_flag') and cls.short_flag:
            parser.add_argument(cls.short_flag, cls.flag, help=cls.help,
                                action=cls)
        else:
            parser.add_argument(cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        super(DebugAction, self).__init__(option_strings, dest, nargs=0,
                                          default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # print('Enabling debugging output.')
        global DEBUG
        DEBUG = True
        setattr(namespace, self.dest, True)


class VerboseAction(DebugAction):
    """Enable the verbose output mechanism."""

    short_flag = '-v'
    flag = '--verbose'
    help = 'Enable verbose output.'

    def __call__(self, parser, namespace, values, option_string=None):
        # print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if DEBUG:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
