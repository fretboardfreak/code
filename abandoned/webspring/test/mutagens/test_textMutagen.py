#!/usr/bin/env python
"""
"""
import unittest

import tempfile

import mutagens.textMutagen as textMutagen

class testTextMutagen(unittest.TestCase):
    def setUp(self):
       self.intmp = tempfile.NamedTemporaryFile()
       self.outtmp = tempfile.NamedTemporaryFile()
       self.token = 'template'

    def test_do(self):
        text = ("This is a ", " with some text")
        key = "template=name"
        value = "testing"
        prep = open(self.intmp.name, 'w')
        prep.write(text[0] + key + text[1])
        prep.close()
        self.tm = textMutagen.TextMutagen(self.intmp.name, self.outtmp.name, self.token, name=value)
        self.tm.do()
        check = open(self.outtmp.name, 'r')
        content = check.read()
        check.close()
        self.assertEquals(content, text[0] + value + text[1],
                          msg = "baseMutagen failed an output check")

if __name__=="__main__":
    unittest.main()

