# one command type console app
from __future__ import absolute_import
from types import FunctionType as function
import mushroom.arg_builder as arg_builder
import mushroom.args_fetch as args_fetch


def func_parser(func:function, strict_mode:bool=True):
    """

    """
    args_cnt, func_varnames, args_dtypes, default_flags = args_fetch.args_status_fetch(func, isClass=False, strict_mode=strict_mode)

    if args_cnt == 0:
        # can run directly
        arg_parser = arg_builder.build_blank_parser(func.__name__, func.__doc__)
    else:
        arg_parser = arg_builder.build_args_parser(func_varnames, args_dtypes, default_flags, func.__name__, func.__doc__)

    return arg_parser


def class_parser(class_, strict_mode:bool=True):
    """
    """
    # initialize first
    parser, subparser = arg_builder.build_class_init_method(class_)
    # iter the method of class
    for func_name, func in class_.__dict__.items():
        if isinstance(func, function) and not func_name.startswith("_"):
            # function type
            args_cnt, func_vars, func_dtypes, func_default_vars = args_fetch.args_status_fetch(func, isClass=True, strict_mode=strict_mode)
            if args_cnt == 0:
                # can run directly
                arg_builder.build_blank_sub_parser(func, subparser)
            else:
                # need args parser
                arg_builder.build_args_sub_parser(func, subparser, func_vars, func_dtypes, func_default_vars)
    return parser
        

def run_func(args, func, isClass=False, self=None):
    """
    run the function
    """
    start_idx = 1 if isClass else 0
    args_cnt = func.__code__.co_argcount
    kwargs = {var_name: getattr(args, var_name) for var_name in func.__code__.co_varnames[start_idx:args_cnt] if hasattr(args, var_name)}
    if self:
        kwargs['self'] = self
            
    return func(**kwargs)

