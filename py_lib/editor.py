import os
from subprocess import Popen
from tempfile import mkstemp

class Editor:
    '''
    An editor with which to edit blocks of text.
    '''
    def __init__(self, editor=None):
        '''
        Initialize the editor.

        If editor is None, a sensible editor will be chosen from the
        environment.
        '''
        if not editor:
            if 'EDITOR' in os.environ:
                self.editor = os.environ['EDITOR']
            else:
                # TODO: make sure to choose something that exists...
                self.editor = 'vi'

    def compose(self):
        '''
        Compose a block of text and return it.
        '''
        _, path = mkstemp(prefix='CSE-')
        Popen('%s %s' % (self.editor, path), shell=True).wait()
        f = open(path)
        output = f.read()
        f.close()
        os.remove(f.name)
        return output
