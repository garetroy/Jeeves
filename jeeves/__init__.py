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
__version__   = '0.1.0'


__all__ = ['cogs','jeeves','jeevesuser','riotinterface','jeevesuserinterface',\
            'test','games','db']

from collections                import namedtuple
from jeeves.jeeves              import Jeeves
from jeeves.jeevesuser          import JeevesUser
from jeeves.riotinterface       import RiotInterface
from jeeves.jeevesuserinterface import JeevesUserInterface
from jeeves.db                  import DB

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel='alpha', serial=0)
