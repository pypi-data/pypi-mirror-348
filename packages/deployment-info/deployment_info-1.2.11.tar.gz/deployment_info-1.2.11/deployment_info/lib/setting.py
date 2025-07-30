from .static.constant import TECH_TABLE, PLACE_TABLE
from .model import setup


def env(hname, uname, name, version):

    if uname in TECH_TABLE:
        return

    if hname in PLACE_TABLE:
        return

    setup(hname, uname, name, version)
