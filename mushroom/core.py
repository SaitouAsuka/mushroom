from __future__ import absolute_import
import sys
import time
from functools import wraps
import types
from mushroom.func_parser import func_parser, run_func, class_parser
import mushroom.traceback_module as tb


def Mushroom(func, timer=False, traceback=False, strict_mode=True):
    """
    one command type console app
    """
    rslt = None
    if timer:
        start_time = time.perf_counter()

    if traceback:
        sys.excepthook = tb.global_excepthook

    if isinstance(func, types.FunctionType):
        # function type
        argparser = func_parser(func, strict_mode=strict_mode)
        args = argparser.parse_args()
        rslt = run_func(args, func)
    elif type(func) == type:
        # class type
        argparser = class_parser(func, strict_mode=strict_mode)
        args = argparser.parse_args()
        # initialize first
        kwargs = {var_name: getattr(args, var_name) for var_name in func.__init__.__code__.co_varnames[1:] if getattr(args, var_name)}
        instance_ = func(**kwargs)
        #fetch the function
        if not hasattr(args, 'func'):
            print("Subcommand not found, plz type -h or --help to get more information")
            return
        rslt = run_func(args, args.func, isClass=True, self=instance_)
    else:
        raise Exception("func must be function or class type")

    if rslt:
        print(rslt)

    if timer:
        print("[INFO] Time cost: {}s".format(time.perf_counter() - start_time))



def mushroom(timer=False, traceback=False):
    def main_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Mushroom(func, timer, traceback)
        return wrapper
    return main_func

