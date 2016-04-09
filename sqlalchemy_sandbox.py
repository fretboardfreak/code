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

    schema = SpaceDatastore(args.database, verbose=args.verbose_db)
    schema.open()

    try:
        schema.verify_tables()
    except DatastoreError as datastore_err:
        print(datastore_err.msg, file=sys.stderr)
        print('Attempting to Create the DB Schema...', file=sys.stderr)
        schema.create_tables()

    print('There are {} Coord rows in the database.'.format(
          schema.coord.count()))

    if schema.coord.count() < 10:
        print('Creating some Coords...')
        schema.create_random_coords(10)

    print('The Coord objects are:')
    for coord in schema.coord.all():
        print(coord)

    print('There are {} System rows in the database.'.format(
          schema.system.count()))

    schema.close()
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


class DatastoreError(Exception):
    pass


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

    @classmethod
    def generate_random(self, coord):
        return System(size=random.randint(1, 20),
                      sun_brightness=random.randint(100, 1000),
                      coord_id=coord.id)


class Planet(BaseTable, DeclarativeBase):
    __tablename__ = 'planet'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    orbit = sqlalchemy.Column(sqlalchemy.Integer)


class Datastore(object):
    def __init__(self, database, declarative_base, db_echo=False):
        self.database = database
        self._declarative_base_table = declarative_base
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
    def query(self):
        return self.session.query

    @property
    def add(self):
        return self.session.add

    def commit(self):
        self.session.commit()

    @property
    def tables(self):
        inspector = sqlalchemy.inspect(self.engine)
        return inspector.get_table_names()

    def table_exists(self, table):
        return table.__tablename__ in self.tables

    def tables_exist(self, tables):
        return all(tbl.__tablename__ in self.tables for tbl in tables)

    def create_tables(self):
        self._declarative_base_table.metadata.create_all(self.engine)

    def verify_tables(self):
        missing_tables = []
        for table in [Coord, System]:
            if not self.table_exists(table):
                missing_tables.append(table.__tablename__)
        if missing_tables:
            raise DatastoreError('The DB File appears to be missing the '
                              'following tables: {}'.format(
                                  ', '.join(missing_tables)))


class SpaceDatastore(Datastore):
    def __init__(self, database, verbose=None):
        super(SpaceDatastore, self).__init__(database, DeclarativeBase,
                                             db_echo=verbose)
    @property
    def coord(self):
        return self.query(Coord)

    @property
    def system(self):
        return self.query(System)

    def create_random_coords(self, minimum_count=10):
        """Generate Random Coord objects and add them to the database."""
        while self.coord.count() < minimum_count:
            self.add(Coord.generate_random())
        self.commit()

    def create_systems(self, coords):
        """Create a System object for each given Coord object."""
        try:
            for coord in coords:
                self.add(System.generate_random(coord))
            self.commit()
        except TypeError:  # coords is not iterable, assume single coord
            self.add(System.generate_random(coord))
            self.commit()

    def unlinked_coords(self):
        """Return the Coord objects that are not used in the rest of the model.

        Coord objects only need to exist in the DB when linked to one of the
        other game objects.
        """
        pass


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
