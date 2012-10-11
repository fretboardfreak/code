# config : Website Config File
#
# Defines a number of customizable options for building your website.
#
# Copy this file to the build directory for your website and edit to suit your
# needs.  Follow the instructions in the comments below; options labeled with
# "*Optional*" have defaults defined by the build.py script.

# sourceDir : str
# The directory containing the rst files that make up the source files of your
# site.
sourceDir = '/home/csand/fret/'

# outputDir : str
# The directory that will contain the built website.  If this directory exists
# and config option "buildDir" is defined then files in "outputDir" will only be
# replaced if their new sha is different.
outputDir = '/home/csand/tmp/website/'

# buildDir : str
# A directory for the build script to use for some temporary files.  This helps
# minimize resource usage for large websites.  It is recommended to have space
# available in this directory to hold at least twice the size of your website
# source rst files.  If not defined, the default is to use linux's /tmp
# directory.
#buildDir =

title = "Fret's Thoughts"
script = {'./fret.css':'css'}

if __name__ == '__main__':
    import sys
    sys.stderr.write('This module is not a script.\n')
    sys.exit(1)
