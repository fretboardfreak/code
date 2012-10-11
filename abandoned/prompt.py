#!/usr/bin/env python
'''
Various prompts which use readline for tab completion
'''

import readline, sys
from subprocess import Popen, PIPE

def output( text, dest = sys.stdout, ttyOnly = False ):
    '''
    Print the given text to the given file.

    If ttyOnly is True, then only print if stdin is a tty.
    '''
    if (not ttyOnly) or sys.stdin.isatty():
        print >> dest, text

class Prompt:
    '''
    Prompt a user for information.
    '''
    def __init__( self, text, default = '' ):
        self.text = text
        self.default = default
        readline.parse_and_bind( 'tab: complete' )
        readline.parse_and_bind( 'set show-all-if-unmodified on' )

    def completer( self ):
        '''
        Returns a completer( text, state ) for use with readline.
        '''
        def completer( text, state ):
            '''
            Disable completion.
            '''
            return False
        return completer

    def validate( self, answer ):
        '''
        Returns True if the given answer is valid.
        '''
        return True

    def prompt( self ):
        '''
        Prompt the user.
        '''
        readline.set_completer( self.completer() )
        if self.default:
            output( '%s [%s] ' % (self.text, self.default),
                    dest = sys.stderr, ttyOnly = True )
        else:
            output( '%s ' % self.text, dest = sys.stderr, ttyOnly = True )
        while True:
            answer = raw_input()
            if not answer:
                answer = self.default
            if self.validate( answer ):
                return answer
            output( 'Invalid response. Please try again.', dest = sys.stderr )

class NonEmptyPrompt(Prompt):
    '''
    Prompts the user for a non-empty string.
    '''
    def validate( self, answer ):
        '''
        Returns true if the answer is non-empty.
        '''
        return len( answer ) > 0

class ChoicePrompt(Prompt):
    '''
    Prompts a user to choose one of a list of options
    '''
    def __init__( self, text, choices, default = '' ):
        Prompt.__init__( self, text, default )
        self.choices = choices
        # disable delimitors, we only want to complete one word
        readline.set_completer_delims( '' )

    def completer( self ):
        '''
        Returns a completer( text, state ) for use with readline.
        '''
        def completer( text, state ):
            '''
            Complete the valid choices
            '''
            textLength = len( text )
            return [ choice for choice in self.choices
                     if len( choice ) > textLength
                     if choice.startswith( text ) ][state]
        return completer

    def validate( self, answer ):
        '''
        Returns True if the given answer is valid.
        '''
        return answer in self.choices

class ChoicePrefixPrompt(ChoicePrompt):
    '''
    A ChoicePrompt that allows unambiguous prefixes of choices.
    '''
    def validate( self, answer ):
        '''
        Returns True if the given answer is valid.
        '''
        found = False
        for choice in self.choices:
            if choice.startswith( answer ):
                if found:
                    return False
                found = True
        return found

class FreeChoicePrompt(ChoicePrompt):
    '''
    A ChoicePrompt that allows choices that are not in the list
    '''
    def validate( self, answer ):
        '''
        Returns True if the given answer is valid.
        '''
        return 0 != len( answer.strip() )

class ChoiceListPrompt(ChoicePrompt):
    '''
    Prompts a user to choose one or more of a list of options.
    '''
    def __init__( self, text, choices, delimiter = ' ', default = '' ):
        ChoicePrompt.__init__( self, text, choices, default )
        self.delimiter = delimiter
        readline.set_completer_delims( delimiter )

    def validate( self, answer ):
        '''
        Returns True if the given answer is valid.
        '''
        return all( (ChoicePrompt.validate( self, a )
                     for a in answer.split( self.delimiter )) )

    def prompt( self ):
        '''
        Prompt the user.
        '''
        answer = ChoicePrompt.prompt( self )
        return answer.split(self.delimiter)

def prepMenu(text, choices):
    '''
    converts text into the menu and converts choices to a valid list
    '''
    count = 1
    for item in choices:
        text += '\n %d. %s' % ( count, item )
        count += 1
    valid = choices
    for a in range( 1, len(choices)+1 ):
        valid.append( '%d' % a)
    return (text, valid)

class MenuPrompt(ChoicePrompt):
    '''
    Prints a menu and accepts either the item number or the text
    '''
    def __init__( self, text, choices, default = '' ):
        ( menu, valid ) = prepMenu( text, choices )
        ChoicePrompt.__init__( self, menu, valid, default )

    def prompt( self ):
        answer = ChoicePrompt.prompt( self )
        if answer.isdigit():
            return self.choices[ int( answer ) - 1 ]
        else:
            return answer

class MenuListPrompt(ChoiceListPrompt):
    '''
    prints a menu and accepts multiple choices
    returns a list
    '''
    def __init__( self, text, choices, delimiter = ',', default = '' ):
        ( menu, valid ) = prepMenu( text, choices )
        ChoiceListPrompt.__init__( self, menu, valid,
                                   delimiter = ',', default = '' )

    def fixChoice( self, answer ):
        if answer.isdigit():
            return self.choices[ int( answer ) -1 ]
        else:
            return answer

    def prompt( self ):
        answer = ChoiceListPrompt.prompt( self )
        retval = []
        for ans in answer:
            retval.append( self.fixChoice(ans) )
        return retval
