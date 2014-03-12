#!/usr/bin/env python
'''
General functionality for CLI driven programs.
'''

import inspect
import os
import readline
import shlex
import sys
from optparse import OptionParser

from prompt import FreeChoicePrompt, ChoiceListPrompt


class Cmd:
    '''
    A command to be run by the CLI program.
    '''
    def __init__(self, action, **completers):
        self.name = action.__name__.replace('_', '-')
        self.help = action.__doc__.strip()
        self.action = action

        self.options = OptionParser()
        self.completers = {}
        for name, completer in completers.items():
            if isinstance(completer, Optional):
                long_opt = '--%s' % name.replace('_', '-')
                self.options.add_option(completer.short_opt, long_opt)
                completer = completer.completer
            self.completers[name] = completer

    def get_args(self, *args, **kwds):
        '''
        Prompt for the arguments to self.action, or, if the keyword
        argument "interactive" is present and False, print the valid
        choices for the next argument and exit.
        '''
        interactive = kwds.get('interactive', True)

        args = list(args)
        opts, args = self.options.parse_args(args)
        spec, _, _, defaults = inspect.getargspec(self.action)
        if 'self' in spec:
            spec.remove('self')

        result = dict(zip(spec, args))
        for opt, value in vars(opts).items():
            if not value:
                value = self.completers[opt].default()
            result[opt] = value
        count = len(result.values())
        if not interactive and len(spec) >= count and count > 0:
            # remove the last argument if it's only a partial
            # completion
            # TODO: don't remove it if it has a space after it...
            key = spec[count - 1]
            if (key in self.completers
                and result[key] not in self.completers[key].choices()):
                count -= 1
        spec = spec[count:]

        for key in spec:
            if not interactive:
                print '\n'.join(self.completers[key].choices())
                sys.exit(0)
            if key in self.completers:
                result[key] = self.completers[key].prompt(key)
        if not interactive:
            sys.exit(0)

        return result

class Optional:
    def __init__(self, short_opt, completer):
        self.short_opt = short_opt
        self.completer = completer

class Completer:
    '''
    A set of possible completions with methods for choosing one of
    them.
    '''
    def __init__(self, default=None):
        self._default = default
        self._choices = []

    def default(self):
        '''
        Return the default completion.
        '''
        if callable(self._default):
            return self._default()
        return self._default

    def choices(self):
        '''
        Return all of the valid choices for completion.
        '''
        if callable(self._choices):
            return self._choices()
        return list(self._choices)

    def prompt(self, name):
        '''
        Prompt the user for one of the valid choices.
        '''
        return FreeChoicePrompt('%s?' % name, self.choices(),
                                default=self.default()).prompt()


class CompAny(Completer):
    '''
    A Completer with no prescribed choices, that accepts any input.
    '''
    pass


class CompChoice(Completer):
    '''
    A Completer whose choices are passed in by a static list.
    '''
    def __init__(self, choices, default=None):
        Completer.__init__(self, default)
        self._choices = choices


class CompMany(Completer):
    '''
    A Completer whose choices are passed in by a static list, but
    multiples may be selected.
    '''
    def __init__(self, choices, default=None):
        Completer.__init__(self, default)
        self._choices = choices

    def prompt(self, name):
        '''
        Prompt the user for one of the valid choices.
        '''
        return ChoiceListPrompt('%s?' % name, self.choices(),
                                default=self.default()).prompt()


class CLI:
    '''
    Base class for CLI driven programs.
    '''
    def __init__(self, argv):
        self.program = argv[0]
        parser = self.get_parser()
        self.opts, self.args = parser.parse_args(argv[1:])
        self.hist_file = None
        self.allowed_exceptions = ()
        self.cmds = [Cmd(self.help), Cmd(self.quit)]

    def usage(self):
        '''
        Return a usage string for the program
        '''
        return '%s [options] [command] [args]' % self.program

    def get_parser(self):
        '''
        Return an option parser for the program
        '''
        parser = OptionParser(usage=self.usage())
        parser.disable_interspersed_args()
        parser.add_option('--listCompletions', dest='complete',
                          default=False, action='store_true',
                          help='list available completions for a shell')
        return parser

    def run_cmd(self, cmd_name=None, args=()):
        '''
        Run the command with the given name.
        '''
        cmd_completer = CompChoice(cmd.name for cmd in self.cmds)
        if cmd_name is None:
            if self.opts.complete:
                print '\n'.join(cmd_completer.choices())
                sys.exit(0)

            cmd_name = cmd_completer.prompt('command')

        if not args:
            args = shlex.split(cmd_name)
            cmd_name = args.pop(0)

        found = []
        for cmd in self.cmds:
            if cmd.name.startswith(cmd_name):
                found.append(cmd)
        if not found:
            if self.opts.complete:
                print '\n'.join(cmd_completer.choices())
                sys.exit(0)
            print >> sys.stderr, 'command not found: %s' % cmd_name
            return

        cmd = found[0]
        if cmd.name != cmd_name:
            if self.opts.complete:
                print '\n'.join(cmd_completer.choices())
                sys.exit(0)

        try:
            i = not self.opts.complete
            args = cmd.get_args(*args, interactive=i)
            cmd.action(**args)
        except self.allowed_exceptions, ex:
            print >> sys.stderr, 'ERROR: %s' % ex
        except NotImplementedError:
            print >> sys.stderr, '%s: Not implemented.' % cmd_name

    def main(self):
        '''
        Run the main program loop.
        '''
        if self.hist_file is not None and os.path.exists(self.hist_file):
            readline.read_history_file(self.hist_file)

        if 0 != len(self.args):
            self.run_cmd(self.args[0], self.args[1:])
            return 0

        try:
            while True:
                self.run_cmd()

        except (EOFError, KeyboardInterrupt):
            pass

        if self.hist_file is not None:
            readline.write_history_file(self.hist_file)
        return 0

    def help(self):
        '''
        Print help about the available commands.
        '''
        print 'Commands:'
        longest = max(len(cmd.name) for cmd in self.cmds)
        for cmd in self.cmds:
            fmt = '%%%ds: %%s' % (longest + 2)
            print fmt % (cmd.name, cmd.help)

    def quit(self):
        '''
        abandon, cease, desist, give up, and exit.
        '''
        raise EOFError
