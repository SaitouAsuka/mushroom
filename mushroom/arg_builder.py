# build the argparse object according to the function
import argparse
import re
import typing, types
import mushroom.args_fetch as args_fetch


def build_blank_parser(func_name, func_doc=""):
    """
    No arguments, just return the parser object
    :return: argparse object
    """
    if not func_doc:
        func_doc = 'Function {} No arguments, run directly'.format(func_name)

    parser = argparse.ArgumentParser(description=func_doc)
    return parser


def build_args_parser(func_vars, func_dtypes, func_default_vars, func_name, func_doc=""):
    """
    Build a parser according to the function vars
    : return: argparse object
    """
    if not func_doc:
        func_doc = 'Function {} Arguments parser, if args are not given, it will be regarded as a string.'.format(func_name)

    parser = argparse.ArgumentParser(description=func_doc)
    for var_name in func_vars:
        argument_add(parser, var_name, func_dtypes.get(var_name, str), func_default_vars.get(var_name, None))
    return parser


def build_class_init_method(class_):
    """
    """
    args_cnt, func_varnames, args_dtypes, default_flags = args_fetch.args_status_fetch(class_.__init__, isClass=True)
    help_text = "MAIN PROGRAM" if not class_.__doc__ else class_.__doc__
    if args_cnt == 0:
        parser = build_blank_parser(func_name="", func_doc=help_text)
            
    else:
        parser = build_args_parser(func_varnames, args_dtypes, default_flags, func_name="", func_doc=help_text)

    subparser = parser.add_subparsers(help='sub command')    
    return parser, subparser


def build_blank_sub_parser(func:types.FunctionType, main_parser):
    """
    Build a blank sub command function
    function should be a instance method
    : return : argparse object
    """
    help_text = "sub command:{}, run directly".format(func.__name__) if not func.__doc__ else func.__doc__
    sub_parser = main_parser.add_parser(func.__name__, help=help_text)
    sub_parser.set_defaults(func=func)
    return main_parser


def build_args_sub_parser(func, main_parser, func_vars, func_dtypes, func_default_vars):
    """
    """
    help_text = 'Function {} Arguments parser, if args are not given, it will be regarded as a string.'.format(func.__name__) if not func.__doc__ else func.__doc__
    sub_parser = main_parser.add_parser(func.__name__, help=help_text)
    sub_parser.set_defaults(func=func)
    for var_name in func_vars:
        argument_add(sub_parser, var_name, func_dtypes.get(var_name, str), func_default_vars.get(var_name, None))
    return main_parser


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
        if func_default_var is not None:
            parser.add_argument('--{}'.format(var_name), type=var_dtype, default=func_default_var, help='{}, default:{}, type:{}'.format(var_name, func_default_var, var_dtype.__name__))
        else:
            parser.add_argument('--{}'.format(var_name), type=var_dtype, required=True, help='{}, type:{}'.format(var_name, var_dtype.__name__))



