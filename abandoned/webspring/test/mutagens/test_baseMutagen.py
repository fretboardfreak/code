#!/usr/bin/env python
"""
"""
import tempfile

import unittest

import mutagens.baseMutagen as baseMutagen

class testBaseMutagen(unittest.TestCase):
    def setUp(self):
       self.intmp = tempfile.NamedTemporaryFile()
       self.outtmp = tempfile.NamedTemporaryFile()
       self.bm = baseMutagen.BaseMutagen(self.intmp.name, self.outtmp.name)

    def test_do(self):
        text = "This is \n some text\t\n\tblah"
        prep = open(self.intmp.name, 'w')
        prep.write(text)
        prep.close()
        self.bm.do()
        check = open(self.outtmp.name, 'r')
        self.assertEquals(check.read(), text,
                          msg = "baseMutagen failed an output check")
        check.close()

if __name__=="__main__":
    unittest.main()

