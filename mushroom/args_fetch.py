# 处理函数的参数
import types


def args_status_fetch(func:types.FunctionType, isClass=False):
    """
    """
    # if contains self argument, it's a class method
    start_idx = 1 if isClass else 0
    args_cnt = func.__code__.co_argcount
    func_varnames = func.__code__.co_varnames[start_idx:args_cnt]
    args_dtypes = func.__annotations__
    default_flags = fetch_defaults(func, func_varnames)

    return args_cnt, func_varnames, args_dtypes, default_flags



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

