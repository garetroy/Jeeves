"""
    Filename: __init__.py
    Author:   Garett Roberts
    Repo:     https://github.com/garetroy/Jeeves
    
    A bot for discord which is developed for 
    easier use of discord with desired
    functionality.

    :copyright: (c) 2018 garetroy
    :license: Unlicense, see LICENSE
"""

__title__     = 'Jeeves'
__author__    = 'garetroy'
__license__   = 'Unlicense'
__copyright__ = 'Coppyright 2018 garetroy'
__version__   = '0.0.1'


from .jeeves        import Jeeves
from .user          import User
from .riotinterface import RiotInterface

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)
