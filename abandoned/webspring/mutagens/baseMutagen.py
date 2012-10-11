"""Base Mutagen.  Unity text Mutagen.  Base class for webspring's mutagen library.
"""

class BaseMutagen:
    """This base Mutagen is intended to be subclassed by all other mutagens.

    The do method should be overwritten by any subclasses.
    """
    def __init__(self, inFname, outFname, **kwargs):
        self.inFname = inFname
        self.outFname = outFname

    def do(self):
        """To be overwritten by subclasses.  Calling do() completes the
        mutation by the Mutagen.
        """
        infp = open(self.inFname, 'r')
        outfp = open(self.outFname, 'w')
        outfp.write(infp.read())
        infp.close()
        outfp.close()
