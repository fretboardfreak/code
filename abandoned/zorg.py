#!/usr/bin/env python
"""
zorg.py : A script providing multiple time saving features for tracking stats
and info about Hellenia and members.
"""
import libmisc
import sys, os, argparse, re, sqlite3

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(name)s: %(levelname)s: %(message)s')

class Member:
    """Represents a member of Hellenia
    """
    def __init__(self, name, coords, points, position, joined):
        self.name = name
        self.coords = coords
        self.points = points
        self.position = position
        self.joined = joined

    def __str__(self):
        return '%s %s %s %s %s' % (self.name, self.coords, self.points,
                self.position, self.joined)

    def getlist(self):
        return [self.name, ':'.join(self.coords), self.points,
                self.position, self.joined]

class AllianceParser(libmisc.FileParser):
    def __init__(self, filename):
        libmisc.FileParser.__init__(self, filename)
        BaseZorgParser.__init__()
        self.pattern = '^\d+\t(?P<name>.*)\t{2}(?P<position>.*)\t(?P<points>.*)\t(?P<coords>.*)\t(?P<joined>.*)\t.*$'
        self.log = logging.getLogger('AllianceParser')
        self.zorgNumSep = '\.'
        self.myNumSep = ' '
        self.members = []

    def emitData(self):
        self.log.debug('emitting member data')
        return self.members

    def _parseLine(self, line):
        self.log.debug('parsing line: %s' % line)
        match = re.search(self.pattern, line)
        if not match:
            self.log.warning('Could not Parse line: ' + line)
        self.members.append(self._constructMember(match.groupdict()))

    def _constructMember(self, data):
        #TODO: should use time.strftime to convert "joined" to a datetime object
        coords = data['coords'].split(':')
        points = re.sub(self.zorgNumSep, self.numSep, data['points'])
        self.log.info('found member %s with %s' % (data['name'], points))
        return Member(data['name'], coords, points, data['position'], data['joined'])

class ZorgDBM(libmisc.DBManager):
    """ Class to store code for generic DB actions. """
    def __init__(self, dbFname=None):
        DBManager.__init__(self, fname=dbFname)

    def _getTables(self):
        return {'Player': ['homeCoords INTEGER PRIMARY KEY', 'name text'],
                'HelleniaRecord': ['homeCoords INTEGER', 'joined TEXT', 'status TEXT',
                    'points INTEGER', 'recordDate TEXT', 'position TEXT',
                    'FOREIGN KEY(homeCoords) REFERENCES Player(homeCoords)'],
                'Colony': ['homeCoords INTEGER', 'colCoords INTEGER', 'moonSize INTEGER'
                    'FOREIGN KEY(homeCoords) REFERENCES Player(homeCoords)'],
                'ACSDepot': ['colCoords INTEGER', 'onMoon INTEGER', 'level INTEGER',
                    'FOREIGN KEY(colCoords) REFERENCES Colony(colCoords)'],
                'PlayerRecord': ['homeCoords INTEGER', 'recordDate TEXT',
                    'buildingPts INTEGER', 'fleetPts INTEGER', 'researchPts INTEGER',
                    'defensePts', 'wins INTEGER', 'losses INTEGER',
                    'FOREIGN KEY(homeCoords) REFERENCES Player(homeCoords)'],
                'GrowthStats': ['homeCoords INTEGER', 'startRecordDate TEXT',
                    'endRecordDate TEXT', 'duration REAL', 'absoluteRate REAL',
                    'normalizedRate REAL', 'newWins INTEGER', 'newLosses INTEGER',
                    'FOREIGN KEY(homeCoords) REFERENCES Player(homeCoords)',
                    'FOREIGN KEY(startRecordDate) REFERENCES PlayerRecord(recordDate)',
                    'FOREIGN KEY(endRecordDate) REFERENCES PlayerRecord(recordDate)'],
                }

    def createdb(self):
        """ Create the required tables for this db. """
        sqlTemplate = 'CREATE TABLE %s (%s);'
        sqlStatements = [sqlTemplate % (name, ', '.join(columns))
                         for name, columns in self._getTables().iteritems()]
        self.conn.executescript('\n'.join(sqlStatements))

class ZorgScript:
    def __init__(self):
        self.args = None
        self.modeName = 0
        self.modeFunc = 1
        self.modeHelp = 2

    def main(self):
        self.args = self.parseCmdLine()
        for name, function, _ in self.getModes(fullMapping=True):
            if self.args.mode == name:
                function()

    def getModes(self, fullMapping=False):
        modes = [('createdb', self.createdb, 'Initialize an empty database.')]
        if fullMapping:
            return modes
        else:
            return [mode[0] for mode in modes]

    def registerModeArguments(self, parser):
        for name, _, hlp in self.getModes(fullMapping=True):
            parser.add_argument('--%s' % name, dest='mode', action='store_const',
                    const=name, help=hlp)

    def parseCmdLine(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-db', '--database', type=str, dest='database',
                default=os.path.join(os.getcwd(), 'zorg.db'),
                help='An existing database file to use.')
        self.registerModeArguments(parser)

        args = parser.parse_args()
        if not os.path.isfile(args.database) and args.mode != 'createdb':
            parser.error('The given database file does not exist.')
        return args

    def createdb(self):
        print 'in createdb'
        return 0


class HackJob:
    def parseCmdLine(self):
        """
        manage cli invocation
        """
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('-a', '--alliance-file',
                help='The file containing alliance info to parse.')
        parser.add_argument('-o', '--output-file', default='hellenia.txt',
                help='The file the results will be written to.')
        return parser.parse_args()

    def createMemberArray(self, members):
        array = [['Name', 'Coords', 'Points', 'Position', 'Joined Hellenia']]
        for member in members:
            array.append(member.getlist())
        return array

    def main(self):
        log = logging.getLogger('main')
        log.info('parsing cmd line args')

        args = self.parseCmdLine()
        if not args.alliance_file:
            raise UserWarning('An alliance file must be provided via the "-a" option.')

        log.info('starting to parse alliance file %s ...' % args.alliance_file)

        ap = AllianceParser(args.alliance_file)
        members = ap.parse()

        log.info('done parsing, generating table...')

        rtg = libmisc.rstTableGenerator(self.createMemberArray(members), rowsep=False)
        table = rtg.getTableString()

        log.info('writing table to file %s ...' % args.output_file)
        open(args.output_file, 'w').write(table)
        log.info('finished')
        return 0

if __name__ == '__main__':
    #sys.exit(HackJob().main())
    sys.exit(ZorgScript().main())
