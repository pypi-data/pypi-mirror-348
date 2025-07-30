import os
from .misc import get_name
from .os_utils import get_uname
from .setting import env


def init(name, version):
    hname = get_name()
    uname = get_uname()
    env(hname, uname, name, version)
