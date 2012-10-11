#!/usr/bin/env python
import docutils.core
import sys, os

def toHtml(text):
    return docutils.core.publish_parts(source=text, writer_name='html')['html_body']

if __name__=="__main__":
    if len(sys.argv) == 3:
        fin = fout = None
        if os.path.isfile(sys.argv[1]):
            fin = open(sys.argv[1], 'r')
        if os.path.isfile(sys.argv[2]):
            os.remove(sys.argv[2])
        fout = open(sys.argv[2], 'w')
        fout.write(toHtml(fin.read()))
        fin.close()
        fout.close()
    else:
        print "Expecting only an input and an output file argument."
