import errno
from subprocess import Popen, PIPE

class Pager(Popen):
    '''
    A process that pages it's input, passing on escape sequences (i.e. colors).
    '''
    def __init__(self):
        Popen.__init__(self, ['less', '-FRX'], stdin=PIPE)

    def communicate(self, input=None):
        try:
            return Popen.communicate(self, input)
        except IOError, e:
            # ignore broken pipe, so that we can quit less before
            # receiving all of stdin.
            if errno.EPIPE != e.errno:
                raise
            return None, None
