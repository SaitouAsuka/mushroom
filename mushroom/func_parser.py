# one command type console app
from __future__ import absolute_import
from re import findall
from types import FunctionType as function
import mushroom.arg_builder as arg_builder


def func_parser(func:function):
    """

    """
    args_cnt = func.__code__.co_argcount
    func_varnames = func.__code__.co_varnames[:args_cnt]
    args_dtypes = func.__annotations__
    default_flags = fetch_defaults(func, func_varnames)

    if args_cnt == 0:
        # can run directly
        arg_parser = arg_builder.build_blank_parser(func.__name__)
        args = arg_parser.parse_args()
        kwargs = {var_name: getattr(args, var_name) for var_name in func_varnames if getattr(args, var_name)}
        func(**kwargs)
    else:
        arg_parser = arg_builder.build_args_parser(func_varnames, args_dtypes, default_flags, func.__name__)
        args = arg_parser.parse_args()
        kwargs = {var_name: getattr(args, var_name) for var_name in func_varnames if getattr(args, var_name)}
        func(**kwargs)


def fetch_defaults(func, func_varnames):
    """
    fetch default values for the function
    return a dict
    """
    func_defaults = func.__defaults__

    func_defaults_dict = {}
    if not func_defaults:
        return func_defaults_dict

    func_defaults = func_defaults[::-1]
    func_varnames = func_varnames[::-1]
    for i in range(len(func_defaults)):
        func_defaults_dict[func_varnames[i]] = func_defaults[i]

    return func_defaults_dict

