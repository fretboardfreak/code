import os, sys
from copy import deepcopy
from argparse import ArgumentParser

class Dispatcher:
    def __init__(self, actions, default_action=None, common_action_args=None,
                 add_non_action_arguments_cb=None, description=None):
        # Actions => { ACTION_NAME: (ARGUMENTS_DICT, CALLABLE) }
        # ARGUMENTS_DICT is kwargs for the ArgumentParser add_argument method.
        # The special key 'short' is used to denote the short option string.
        self.actions = actions

        # If default_action is None then user must supply an action option
        self.default_action = default_action

        # description for ArgumentParser
        self.description = description

        self.common_action_args = {'dest': 'action', 'action': 'store_const'}
        if common_action_args:
            self.common_action_args.update(common_action_args)

        # non-action arguments cb will be given a parser argument
        self.add_non_action_arguments_cb=add_non_action_arguments_cb

        self._args_parsed = False
        self._parsed_args = None

    def _add_action_argument_group(self, parser):
        action_group = parser.add_argument_group('actions')
        for opt, (kwargs, _) in self.actions.iteritems():
            arg_dict = deepcopy(self.common_action_args)
            arg_dict.update(kwargs)
            short = None
            try:
                short = arg_dict.pop('short')
            except KeyError:
                pass
            if 'const' not in arg_dict.keys():
                arg_dict['const'] = opt
            if short:
                option = ('-' + short, '--' + opt)
            else:
                option = ('--' + opt,)
            action_group.add_argument(*option, **arg_dict)
        return action_group

    def parse_args(self):
        parser = ArgumentParser(description=self.description)
        self._add_action_argument_group(parser)
        if self.add_non_action_arguments_cb:
            self.add_non_action_arguments_cb(parser)
        parser.add_argument(dest='args', nargs='*', type=str, metavar='ARG')
        namespace, _ = parser.parse_known_args()
        if namespace.action == None:
            namespace.action = self.default_action
        self._args_parsed = True
        self._parsed_args = namespace
        return self._parsed_args

    def do_action(self, **kwargs):
        if not self._args_parsed:
            self.parse_args()
        self.actions[self._parsed_args.action][1](self._parsed_args, **kwargs)

if __name__=="__main__":

    def example_action(args):
        print "example_action: %s" % args

    EXAMPLE_ACTIONS = {
        'foobar': ({'short': 'f', 'help': 'foo bar baz.'}, example_action),
    }

    def example_add_non_action_arguments_cb(parser):
        parser.add_argument('-t', '--test', action='store', type=str,
                            default='testing', help="Random Test Option.")

    example = Dispatcher(
            EXAMPLE_ACTIONS, default_action='foobar',
            add_non_action_arguments_cb=example_add_non_action_arguments_cb,
            description='A Description of the program')
    example.do_action()
