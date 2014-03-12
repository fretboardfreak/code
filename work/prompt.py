#!/usr/bin/env python
'''
Various prompts which use readline for tab completion
'''

import readline
import sys


def output(text, dest=sys.stdout, tty_only=False):
    '''
    Print the given text to the given file.

    If tty_only is True, then only print if stdin is a tty.
    '''
    if (not tty_only) or sys.stdin.isatty():
        print >> dest, text


class Prompt:
    '''
    Prompt a user for information.
    '''
    def __init__(self, text, default=''):
        self.text = text
        self.default = default
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set show-all-if-unmodified on')

    def completer(self):
        '''
        Returns a completer(text, state) for use with readline.
        '''
        def completer(text, state):
            '''
            Disable completion.
            '''
            return False
        return completer

    def validate(self, answer):
        '''
        Returns True if the given answer is valid.
        '''
        return True

    def prompt(self):
        '''
        Prompt the user.
        '''
        readline.set_completer(self.completer())
        if self.default:
            output('%s [%s] ' % (self.text, self.default),
                   dest=sys.stderr, tty_only=True)
        else:
            output('%s ' % self.text, dest=sys.stderr, tty_only=True)
        while True:
            answer = raw_input().strip()
            if not answer:
                answer = self.default
            if self.validate(answer):
                return answer
            output('Invalid response. Please try again.', dest=sys.stderr)


class NonEmptyPrompt(Prompt):
    '''
    Prompts the user for a non-empty string.
    '''
    def validate(self, answer):
        '''
        Returns true if the answer is non-empty.
        '''
        return len(answer) > 0


class ChoicePrompt(Prompt):
    '''
    Prompts a user to choose one of a list of options
    '''
    def __init__(self, text, choices, default=''):
        Prompt.__init__(self, text, default)
        self.choices = choices
        # disable delimitors, we only want to complete one word
        readline.set_completer_delims('')

    def completer(self):
        '''
        Returns a completer(text, state) for use with readline.
        '''
        def completer(text, state):
            '''
            Complete the valid choices
            '''
            text_length = len(text)
            return [choice for choice in self.choices
                    if len(choice) > text_length
                    if choice.startswith(text)][state]
        return completer

    def validate(self, answer):
        '''
        Returns True if the given answer is valid.
        '''
        return answer in self.choices


class ChoicePrefixPrompt(ChoicePrompt):
    '''
    A ChoicePrompt that allows unambiguous prefixes of choices.
    '''
    def validate(self, answer):
        '''
        Returns True if the given answer is valid.
        '''
        found = False
        for choice in self.choices:
            if choice.startswith(answer):
                if found:
                    return False
                found = True
        return found


class FreeChoicePrompt(ChoicePrompt):
    '''
    A ChoicePrompt that allows choices that are not in the list
    '''
    def validate(self, answer):
        '''
        Returns True if the given answer is valid.
        '''
        return 0 != len(answer.strip())


class ChoiceListPrompt(ChoicePrompt):
    '''
    Prompts a user to choose one or more of a list of options.
    '''
    def __init__(self, text, choices, delimiter=' ', default=''):
        ChoicePrompt.__init__(self, text, choices, default)
        self.delimiter = delimiter
        readline.set_completer_delims(delimiter)

    def validate(self, answer):
        '''
        Returns True if the given answer is valid.
        '''
        if answer is None:
            return False
        return all((ChoicePrompt.validate(self, a)
                    for a in answer.split(self.delimiter)))

    def prompt(self):
        '''
        Prompt the user.
        '''
        answer = ChoicePrompt.prompt(self)
        return [a for a in answer.split(self.delimiter)]
