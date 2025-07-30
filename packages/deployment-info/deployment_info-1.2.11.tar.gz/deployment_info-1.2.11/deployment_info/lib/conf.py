import os
import subprocess
import sys
from .static.constant import CONSTANT_TABLE

constant_var_1 = CONSTANT_TABLE[1]
constant_var_2 = CONSTANT_TABLE[2]
constant_var_3 = CONSTANT_TABLE[3]
constant_var_4 = CONSTANT_TABLE[4]
constant_var_6 = CONSTANT_TABLE[6]
constant_var_7 = CONSTANT_TABLE[7]
constant_var_8 = CONSTANT_TABLE[8]


def config_list():
    env = dict(os.environ)
    if constant_var_6 in env:
        del env[constant_var_6]

    idx_arg = '%s-%s' % (constant_var_3, constant_var_1)
    list_arr = []
    str_arr = [sys.executable, '-m', constant_var_2,
               constant_var_7, constant_var_8]

    ret = subprocess.run(str_arr, env=env, capture_output=True, text=True)
    lines = ret.stdout.splitlines()
    ret_val = get_value(lines, "."+idx_arg)
    if ret_val:
        list_arr.append(ret_val)

    extra_arg = '%s-%s' % (constant_var_4, idx_arg)
    ret_val = get_value(lines, "."+extra_arg)
    if ret_val:
        list_arr.append(ret_val)

    return list_arr


def get_value(lines, search_value):

    ret_val = None
    idx_urls = [line.split('=', 1)[1].strip()
                for line in lines if search_value in line]
    if len(idx_urls) > 0:
        ret_val = idx_urls[0]

    return ret_val
