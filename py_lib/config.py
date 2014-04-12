""" This config module facilitates high level usage of the configobj module
"""
import configobj

def setConfigDefaults(config, default):
    """ Make sure all the required sections and fields are in the config file.

        :param config: the configobj object to operate on
        :param default: the dict representing your app's default config file
    """
    _setSectionDefaults(config, default)
    config.write()


def _setSectionDefaults(config, section):
    """ Set defaults for a section of the config.  Recurse on any subsections.

        :param config: the configobj object to operate on
        :param section: the dict representing your app's defaults for a section
    """
    for name, value in section.iteritems():
        config.setdefault(name, value)
        if isinstance(value, dict):
            _setSectionDefaults(config[name], section[name])


def getConfig(filename, default=None):
    """ Create and validate a new config object

        :param filename: the filename of the config file to load
        :param default: (optional) the default dict for the config file
    """
    if not default:
        default = {}
    config = configobj.ConfigObj(filename)
    setConfigDefaults(config, default)
    return config
