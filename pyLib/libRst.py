#!/usr/bin/env python
"""
libRst
======

This module is intended to provide compilation support for rst.  The intention
is to keep the required libraries all in one place to provide a deployable,
python 2.6 compatible, rst compiler.

RST Constructs to be supported:
    - paragraph
    - heading
    - list (unordered, ordered)
    - table
"""
import docutils.core
import sys, os.path

def toHtml(text):
    """ Use Docutils to compile text into html. """
    return docutils.core.publish_parts(
            source=text, writer_name='html')['html_body']

def indentParagraph(text, indent):
    """ Indent some text by a number of spaces

        :param indent: (int or str) number of spaces to indent the text, or
                       the text to use as the indentation

        >>> indentParagraph('foo\\nbar', indent=3)
        '   foo\\n   bar'
        >>> indentParagraph('foo\\nbar', indent='__')
        '__foo\\n__bar'
    """
    if isinstance(indent, int):
        indent = ' ' * indent
    return '\n'.join([indent + line for line in text.split('\n')])

def continueLine(line, continuationPrefix, width=80):
    """ Split line into multiple lines limited to given width (including
        length of continuation prefix).

        :param line: (str) The line to split
        :param contiuationPrefix: (str) The prefix to use on wrapped lines
        :param width: (int) The maximum width of the resulting block

        >>> continueLine('-'*10, continuationPrefix='__', width=4)
        '----\\n__--\\n__--\\n__--\\n'
        >>> continueLine('-'*10, continuationPrefix='_ _ _', width=4)
        Traceback (most recent call last):
            ...
        ValueError: Length of continuationPrefix must be less than width
    """
    contLen = len(continuationPrefix)
    if contLen > width:
        msg = "Length of continuationPrefix must be less than width"
        raise ValueError(msg)
    step = width - contLen
    index = width
    retVal = line[:index] + '\n'
    while index < len(line) - step:
        retVal += continuationPrefix + line[index:index+step] + '\n'
        index = index + step
    retVal += continuationPrefix + line[index:] + '\n'
    return retVal

def _stripNewline(text):
    """ Strip newlines from beginning and end of text.

        :return: (tuple of str) the beginning newline value, stripped text,
                 ending newline value

        >>> _stripNewline('\\nfoo\\n')
        ('\\n', 'foo', '\\n')
        >>> _stripNewline('foo')
        ('', 'foo', '')
    """
    start = ''
    end = ''
    if text[0] == '\n':
        start = '\n'
        text = text[1:]
    if text[-1] == '\n':
        end = '\n'
        text = text[:-1]
    return start, text, end

def heading(text, level):
    """ Turn a line of text into an RST heading.  Always returns a trailing
        newline.

        :param level: (int) the level of heading to produce.  Level 0 is the
                      document title and is overlined.

        >>> heading('foo', 0)
        '===\\nfoo\\n===\\n'
        >>> heading('foo', 1)
        'foo\\n===\\n'
        >>> heading('\\nfoo\\n', 2)
        '\\nfoo\\n---\\n'
        >>> heading('foo', 11)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: A heading cannot have a level less than 0 or ...
    """
    _chars = ['=', '-', '~', '"', "'", '*', '^', '_', '+', ':', '#']
    getUnderline = lambda charIndex: _chars[charIndex] * len(text)
    start, text, end = _stripNewline(text)
    if level < 0 or level >= len(_chars):
        msg = ('A Heading cannot have a level less than 0 or larger ' +
               'than %s: %s' % (len(_chars), text))
        raise ValueError(msg)
    elif level == 0:
        return '%s%s\n%s\n%s\n' % (start, getUnderline(level), text,
                                   getUnderline(level))
    else:
        return '%s%s\n%s\n' % (start, text, getUnderline(level-1))

def list(elements, ordered=False, startIndex=1):
    """ Create an RST List from a collection.

        :param elements: (list) a collection of strings, each an element of
                         the list
        :param ordered: (bool) set's list type between bulleted and enumerated
        :param startIndex: (int) if start index is 1 then an auto-enumerated
                           list is used ("#. element\\\n")

        >>> list(['foo', 'bar'])
        '- foo\\n- bar\\n'
        >>> list(['foo', 'bar'], ordered=True)
        '#. foo\\n#. bar\\n'
        >>> list(['foo', 'bar'], ordered=True, startIndex=3)
        '3. foo\\n4. bar\\n'

        startIndex has no effect if not ordered
        >>> list(['foo', 'bar'], ordered=False, startIndex=3)
        '- foo\\n- bar\\n'
    """
    retVal = ''
    index = startIndex
    for element in elements:
        if ordered and startIndex==1:
            retVal += '#. %s\n' % (element)
        elif ordered and startIndex>1:
            retVal += '%s. %s\n' % (index, element)
            index = index + 1
        else:
            retVal += '- %s\n' % element
    return retVal

if __name__=="__main__":
    import doctest
    doctest.testmod()
