#!/usr/bin/env python3
"""A Sandbox Script to allow me to play with and learn the SQALchemy Tools.

Go to http://docs.sqlalchemy.org for more info.
"""

import sys, argparse, os, random, sqlite3
from collections import OrderedDict

try:
    import sqlalchemy
    from sqlalchemy.ext.declarative import declarative_base
except ImportError:
    print('Error: Cannot Import SQLAlchemy', file=sys.stderr)
    sys.exit(1)


VERSION = "0.0"
VERBOSE = False


def main():
    args = parse_cmd_line()
    vprint(args)

    datastore = Datastore(args.database, db_echo=args.verbose_db)
    session = datastore.connect()

    # Check table presence. Create any missing tables.
    print('Existing Tables: {}'.format(datastore.tables))
    if not datastore.tables_exist([Coord]):
        print('Required tables not present, creating them.')
        datastore.create_tables([Coord])

    # Verify that we have some Coordinate data to play with
    count = session.query(Coord).count()
    print('{} Coord objects present, adding {} new coords.'.format(
        count, 10 - count))
    while session.query(Coord).count() < 10:
        session.add(Coord.generate_random())
        session.commit()

    # Print the contents of the database
    print('Coord objects in the database.')
    for coord in session.query(Coord).all():
        print(coord)

    datastore.close()
    return 0


def parse_cmd_line():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', help='Print the version and exit.', action='version',
        version='%(prog)s {}'.format(VERSION))
    VerboseAction.add_parser_argument(parser)
    parser.add_argument(
        '--verbose-db', dest='verbose_db', default=False, action='store_true',
        help='Enable DB debugging output.')
    parser.add_argument(
        dest='database', metavar='DATABASE', default='sandbox.db', nargs='?')

    return parser.parse_args()


def vprint(msg):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(msg)


class VerboseAction(argparse.Action):
    """Enable the verbose output mechanism."""

    flag = '--verbose'
    help = 'Enable verbose output.'

    @classmethod
    def add_parser_argument(cls, parser):
        parser.add_argument(cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        super(VerboseAction, self).__init__(option_strings, dest, nargs=0,
                                            default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)


class BaseTable(object):
    @property
    def columns(self):
        raise NotImplemented

    def __repr__(self):
        return '<{cls}(id={id}, {attrs})>'.format(
            cls=self.__class__.__name__, id=self.id,
            attrs=', '.join(['{key}={val}'.format(key=key, val=val)
                            for key, val in self.columns.items()]))

DeclarativeBase = declarative_base()


class Coord(BaseTable, DeclarativeBase):
    __tablename__ = 'coord'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    sector_x = sqlalchemy.Column(sqlalchemy.Integer)
    sector_y = sqlalchemy.Column(sqlalchemy.Integer)
    system_x = sqlalchemy.Column(sqlalchemy.Integer)
    system_y = sqlalchemy.Column(sqlalchemy.Integer)

    system = sqlalchemy.orm.relationship(
        "System", uselist=False, back_populates="coord")

    @property
    def columns(self):
        return OrderedDict([('sector_x', self.sector_x),
                            ('sector_y', self.sector_y),
                            ('system_x', self.system_x),
                            ('system_y', self.system_y)])

    @classmethod
    def generate_random(self):
        coord_range = (0, 10)
        return Coord(sector_x=random.randint(*coord_range),
                     sector_y=random.randint(*coord_range),
                     system_x=random.randint(*coord_range),
                     system_y=random.randint(*coord_range))


class System(BaseTable, DeclarativeBase):
    __tablename__ = 'system'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    size = sqlalchemy.Column(sqlalchemy.Integer)
    sun_brightness = sqlalchemy.Column(sqlalchemy.Integer)

    coord_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('coord.id'))

    coord = sqlalchemy.orm.relationship("Coord", back_populates="system")

    @property
    def columns(self):
        return OrderedDict([('coord_id', self.coord_id),
                            ('coord', self.coord), ('size', self.size),
                            ('sun_brightness', self.sun_brightness)])


class Datastore(object):
    def __init__(self, database, db_echo=False):
        self.database = database
        self.db_echo = db_echo
        self.closed = True
        self.engine = None
        self.session_type = None
        self.session = None

    def connect(self):
        if self.engine is None:
            self.engine = sqlalchemy.create_engine(
                'sqlite:///{}'.format(self.database), echo=self.db_echo)
        if self.session_type is None:
            self.session_type = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = self.session_type()
        self.closed = False
        return self.session

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None
            self.closed = True

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @property
    def tables(self):
        inspector = sqlalchemy.inspect(self.engine)
        return inspector.get_table_names()

    def table_exists(self, table):
        return table.__tablename__ in self.tables

    def tables_exist(self, tables):
        return all(tbl.__tablename__ in self.tables for tbl in tables)

    def create_tables(self, tables):
        for table in tables:
            if not self.table_exists(table):
                table.metadata.create_all(self.engine)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if VERBOSE:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
