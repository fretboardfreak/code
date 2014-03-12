#!/usr/bin/env python

"""
Given an input file containing defect numbers, extract the unique defect
numbers and generate a CSE query URL to help prioritize work on the tickets.
"""
USAGE="%prog [options] <input-file>, ..."

import sys, optparse, re

from cse import CseTool

DEFECT_PATTERN = '(?P<defects>q\d\d\d\d\d)'

OPEN_DEFECT_QUERY = '(cqDefects:rid:{{{defects}}})&(cqDefects:cseState:{{OPEN/DUPL|OPEN/PARKED|OPEN/REVIEW|OPEN/WORK|UNAN/ENG|UNAN/RCA|UNAN/RETURN|UNAN/TBD|UNAN/TRIAGE}})'

BASE_URL = 'https://cse.spgear.lab.emc.com/cgi-bin/login/cse/5433/zeph/query?sortFields=severity%2CcomputedPriority&resultFields=cseState%2Crid%2Cseverity%2CcomputedPriority%2Csummary&table=cqDefects&f0field=rid&f0val=cqDefects%3Arid%3A{{{defects}}}'


def main():
    opts, input_files = parse_command_line()
    defects = parse_for_defect_ids(input_files)
    opts.action(defects)

def print_unique_defects(defects):
    print "{defects}\n".format(defects=','.join(defects))

def generate_prioritized_query(defects):
    print "Full list of unique defects: {defects}\n".format(defects=','.join(defects))
    open_defects = filter_out_closed_defects(defects)
    print "List of open defects: {defects}\n".format(defects=','.join(open_defects))
    print BASE_URL.format(defects='|'.join(open_defects))

def print_closed_defects(defects):
    open_defects = filter_out_closed_defects(defects)
    closed_defects = defects - open_defects
    print "{defects}\n".format(defects=','.join(closed_defects))

def print_open_defects(defects):
    open_defects = filter_out_closed_defects(defects)
    print "{defects}\n".format(defects=','.join(open_defects))

def filter_out_closed_defects(defects):
    cseTool = CseTool('zeph')
    result = cseTool.query(OPEN_DEFECT_QUERY.format(defects='|'.join(defects)))
    return set(re.findall(DEFECT_PATTERN, result))

def parse_for_defect_ids(input_files):
    defect_ids = set()
    for f in input_files:
        defect_ids = defect_ids.union(_parse_for_defect_ids(f))
    return defect_ids

def _parse_for_defect_ids(input_file):
    with open(input_file, 'r') as fd:
        return set(re.findall(DEFECT_PATTERN, fd.read()))

def parse_command_line():
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option(
            '-p', '--print', action='store_const', dest='action',
            const=print_unique_defects,
            help='Print a list of defect IDs in the given files.')
    parser.add_option(
            '-c', '--closed', action='store_const', dest='action',
            const=print_closed_defects,
            help='Print a list of the closed defect IDs from the given files.')
    parser.add_option(
            '-o', '--open', action='store_const', dest='action',
            const=print_open_defects,
            help='Print a list of the open defect IDs from the given files.')

    opts, input_files = parser.parse_args()
    if getattr(opts, 'action', None) is None:
        setattr(opts, 'action', generate_prioritized_query)
    return opts, input_files

if __name__ == "__main__":
    sys.exit(main())
