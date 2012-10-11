#!/usr/bin/env python
"""
This module is intended to provide compilation support for rst.  The intention
is to keep the required libraries all in one place to provide a deployable,
python 2.6 compatible, rst compiler.
"""
import docutils.core
import sys, os.path

def toHtml(text):
    return docutils.core.publish_parts(source=text, writer_name='html')['html_body']

if __name__=="__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            fp = open(sys.argv[1], 'r')
            print toHtml(fp.read())
