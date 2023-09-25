# 处理函数的参数
import types
from mushroom.arg_exceptions import TypeNotMatchException


def args_status_fetch(func:types.FunctionType, isClass=False, strict_mode:bool=True):
    """
    """
    # if contains self argument, it's a class method
    start_idx = 1 if isClass else 0
    args_cnt = func.__code__.co_argcount
    func_varnames = func.__code__.co_varnames[start_idx:args_cnt]
    args_dtypes = func.__annotations__
    default_flags = fetch_defaults(func, func_varnames, args_dtypes, strict_mode)

    return args_cnt, func_varnames, args_dtypes, default_flags



def fetch_defaults(func, func_varnames, args_dtypes, strict_mode:bool=True):
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
        if strict_mode and  not isinstance(func_defaults[i], args_dtypes.get(func_varnames[i], str)):
            raise TypeNotMatchException("arg '{}' default value {} can not match the type {} ".format(func_varnames[i], func_defaults[i], args_dtypes.get(func_varnames[i], str)))
        func_defaults_dict[func_varnames[i]] = func_defaults[i]

    return func_defaults_dict

