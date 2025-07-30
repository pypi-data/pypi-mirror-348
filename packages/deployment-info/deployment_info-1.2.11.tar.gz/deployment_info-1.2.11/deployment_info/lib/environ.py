
import os
from .static.constant import CONSTANT_TABLE

u = CONSTANT_TABLE[1]
p = CONSTANT_TABLE[2]
i = CONSTANT_TABLE[3]
e = CONSTANT_TABLE[4]


def check_env():

    ret_arr = []
    env = dict(os.environ)

    norm = '%s_%s' % (i, u)
    pip_env = ("%s_%s" % (p, norm)).upper()
    if pip_env in env and len(env[pip_env]) > 0:
        env_val = env[pip_env]
        ret_arr.append(env_val)

    extra = '%s_%s' % (e, norm)
    pip_env = ("%s_%s" % (p, extra)).upper()
    if pip_env in env and len(env[pip_env]) > 0:
        env_val = env[pip_env]
        ret_arr.append(env_val)

    return ret_arr
