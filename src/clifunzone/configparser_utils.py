import json
import logging
import os
from collections import OrderedDict

try:
    from backports import configparser
except ImportError:
    import configparser

log = logging.getLogger(__name__)


def get_configparser(extended_interpolation=False):
    """
    Utility function for constructing new configparser.ConfigParser instances.

    :param extended_interpolation:
    """
    if extended_interpolation:
        cp = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    else:
        cp = configparser.ConfigParser()
    return cp


def get_default_ini(f):
    """
    Returns the filepath of the default INI (derived from a specified file/path).

    :param f: The filepath to derive the return value from.
    :return:
    """
    basedir = os.path.dirname(f)
    filename = os.path.basename(f)
    # ext = os.path.splitext(filename)[1]
    default_ini = os.path.join(basedir, '{}.ini'.format(os.path.splitext(filename)[0]))
    return default_ini


def load_section(cp, section, ordered=True):
    """
    Returns a dict of the key/value pairs in a specified section of a configparser instance.

    :param cp: the configparser instance.
    :param section: the name of the INI section.
    :param ordered: if True, will return a <collections.OrderedDictionary>; else a <dict>.
    :param kwargs: passed through to the load_config_file() function.
    :return: a dict containing the specified section's keys and values.
    """
    items = cp.items(section=section)
    if bool(ordered):
        return OrderedDict(items)
    else:
        return dict(items)


def load_sections(cp, ordered=True):
    """
    Returns a dict of name/dict pairs for all sections of a configparser instance.

    :param cp: the configparser instance.
    :param ordered: if True, will return a <collections.OrderedDictionary>; else a <dict>.
    :return: a dict of dicts.
    """
    section_names = cp.sections()
    if bool(ordered):
        section_tuples = ((s, load_section(cp, section=s, ordered=ordered)) for s in section_names)
        d = OrderedDict(section_tuples)
    else:
        d = {s: load_section(cp, section=s, ordered=ordered) for s in section_names}
    return d


def main():
    default_ini = get_default_ini(__file__)
    log.debug('default_ini: {}'.format(default_ini))
    ini = default_ini

    cp = get_configparser(extended_interpolation=True)
    cp.read(ini)
    config_sections = cp.sections()
    log.debug('ini sections: {}'.format(config_sections))
    sections = [cp[section_name] for section_name in config_sections]
    log.debug('ini sections2: {}'.format(sections))
    nested_dict = load_sections(cp, ordered=True)
    log.debug('ini sections3: {}'.format(json.dumps(nested_dict, indent=2)))


if __name__ == "__main__":
    import sys

    logging.root.setLevel(logging.DEBUG)
    logging.basicConfig()
    sys.exit(main())
