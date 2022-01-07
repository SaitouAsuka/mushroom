from __future__ import absolute_import
import types
from mushroom.func_parser import func_parser, run_func, class_parser



def Mushroom(func):
    """
    one command type console app
    """
    rslt = None
    if isinstance(func, types.FunctionType):
        # function type
        argparser = func_parser(func)
        args = argparser.parse_args()
        rslt = run_func(args, func)
    elif type(func) == type:
        # class type
        argparser = class_parser(func)
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