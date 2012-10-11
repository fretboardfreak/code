"""This module contains the TextMutagen class.
"""

class TextMutagen:
    """Text Mutagen does a basic mutation on text files.

    It searches through each line of the input file searching for token.  If
    a token and key pair are found they are replaced with the value of
    self.kwargs[key].

    This is only compatible with 1 token per line, the value '' is used if the
    key is not given in kwargs and the token cannot be escaped and thus
    cannot be used elsewhere in the text file.
    """
    def __init__(self, inFname = '', outFname = '', token='template', **kwargs):
        self.inFname = inFname
        self.outFname = outFname
        self.token = token
        self.kwargs = kwargs

    def do(self):
        """
        The file mutagen replaces the text "token=key" (where token is the
        value of token) with self.kwargs[key].
        """
        inFp = open(self.inFname, 'r')
        outFp = open(self.outFname, 'w')
        line = inFp.readline()
        while line != '':
            preLine, key, postLine = self._extractKey(line)
            if not key and not postLine:
                outFp.write(line)
                break
            val = ''
            if self.kwargs.has_key(key):
                val = self.kwargs[key]
            outFp.write(preLine + val + postLine)
            line = inFp.readline()

    def _extractKey(self, line):
        """Given a line of text that contains the token, extract the key in
        the form of token=key.

        Return the beggining of the line up to token, the key, and the end of
        the line after the token and key pair.  If token isn't found return
        just the line intact.

        For example:
        -> "this was written by template=user for his website"
        return: ("this was written by ", "user", " for his website")
        """
        pos = line.find(self.token)
        if pos < 0:
            return (line, None, None)
        parts = line.split(self.token)
        preLine = parts[0]

        #extract the first word after the '=' from parts[1]
        key = parts[1][1:].split(' ')[0]

        postLine = parts[1][1 + len(key):]

        return (preLine, key, postLine)
