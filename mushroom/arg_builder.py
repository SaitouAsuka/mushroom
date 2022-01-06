# build the argparse object according to the function
import argparse
import re
import typing


def build_blank_parser(func_name):
    """
    No arguments, just return the parser object
    :return: argparse object
    """
    parser = argparse.ArgumentParser(description='Function {} No arguments, run directly'.format(func_name))
    return parser


def build_args_parser(func_vars, func_dtypes, func_default_vars, func_name):
    """
    Build a parser according to the function vars
    : return: argparse object
    """
    parser = argparse.ArgumentParser(description='Function {} Arguments parser, if args are not given, it will be regarded as a string.'.format(func_name))
    for var_name in func_vars:
        argument_add(parser, var_name, func_dtypes.get(var_name, str), func_default_vars.get(var_name, None))
    return parser


def argument_add(parser, var_name, var_dtype, func_default_var):
    """
    """
    type_dict = {
        "int" : int,
        "str" : str,
        "bool" : bool,
        "float" : float,
    }

    if var_dtype == bool:
        # bool type
        flag = "True" if func_default_var else "False"
        actions = {
            "False": "store_true",
            "True": "store_false",
        }
        parser.add_argument('--{}'.format(var_name), action=actions[flag], help='{}, deafult:{}, it will be {} if it\'s applied.'.format(var_name, flag, "False" if flag == "True" else "True"))
    elif isinstance(var_dtype, typing._GenericAlias):
        # list type
        dtype_fetch = re.findall(r'\[(.*)\]', str(var_dtype))
        dtype = dtype_fetch[0] if dtype_fetch else str
        parser.add_argument('--{}'.format(var_name), nargs='+', type=type_dict[dtype], help='{}, element type: {}'.format(var_name, dtype))
    else:
        # other type
        if func_default_var:
            parser.add_argument('--{}'.format(var_name), type=var_dtype, default=func_default_var, help='{}, default {}, type:{}'.format(var_name, func_default_var, var_dtype.__name__))
        else:
            parser.add_argument('--{}'.format(var_name), type=var_dtype, required=True, help='{}, type:{}'.format(var_name, var_dtype.__name__))