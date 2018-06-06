__version__ = '0.0'

try:
    from ._version import __version__
except ImportError:
    pass

VERSION = __version__.split('+')
VERSION = tuple(list(map(int, VERSION[0].split('.'))) + VERSION[1:])

default_app_config = 'people.apps.PeopleConfig'
