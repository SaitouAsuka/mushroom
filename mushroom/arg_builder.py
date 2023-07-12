# build the argparse object according to the function
import argparse
import re
import typing, types
from collections import Counter
from mushroom.arg_textwrap import RawDescriptionHelpFormatter as HelpFormatter
import mushroom.args_fetch as args_fetch


def build_blank_parser(func_name, func_doc=""):
    """
    No arguments, just return the parser object
    :return: argparse object
    """
    if not func_doc:
        func_doc = 'Function {} No arguments, run directly'.format(func_name)

    parser = argparse.ArgumentParser(description=func_doc, formatter_class=HelpFormatter)
    return parser


def build_args_parser(func_vars, func_dtypes, func_default_vars, func_name, func_doc="", mode="number"):
    """
    Build a parser according to the function vars
    : return: argparse object
    """
    if not func_doc:
        func_doc = 'Function {} Arguments parser, if args are not given, it will be regarded as a string.'.format(func_name)

    parser = argparse.ArgumentParser(description=func_doc, formatter_class=HelpFormatter)
    abbr_names_mapper = args_abbreviate(func_vars, mode=mode)
    helper_mapper = helper_builder_from_doc(func_doc=func_doc)
    for var_name in func_vars:
        argument_add(parser, var_name, func_dtypes.get(var_name, str), func_default_vars.get(var_name, None), abbr_names_mapper[var_name], helper=helper_mapper.get(var_name, ""))
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


def build_args_sub_parser(func, main_parser, func_vars, func_dtypes, func_default_vars, mode="number"):
    """
    """
    help_text = 'Function {} Arguments parser, if args are not given, it will be regarded as a string.'.format(func.__name__) if not func.__doc__ else func.__doc__
    sub_parser = main_parser.add_parser(func.__name__, help=help_text)
    sub_parser.set_defaults(func=func)
    abbr_names_mapper = args_abbreviate(func_vars, mode=mode)
    helper_mapper = helper_builder_from_doc(func.__doc__)
    for var_name in func_vars:
        argument_add(sub_parser, var_name, func_dtypes.get(var_name, str), func_default_vars.get(var_name, None), abbr_names_mapper[var_name], helper=helper_mapper.get(var_name, ""))
    return main_parser


def argument_add(parser, var_name, var_dtype, func_default_var, abbr_name, helper=""):
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
        parser.add_argument('--{}'.format(var_name), '-{}'.format(abbr_name), action=actions[flag], help='{}, deafult:{}, it will be {} if it\'s applied.'.format(var_name if not helper else helper, flag, "False" if flag == "True" else "True"))
    elif isinstance(var_dtype, typing._GenericAlias):
        # list type
        dtype_fetch = re.findall(r'\[(.*)\]', str(var_dtype))
        dtype = dtype_fetch[0] if dtype_fetch else str
        parser.add_argument('--{}'.format(var_name), '-{}'.format(abbr_name), nargs='+', type=type_dict[dtype], help='{}, element type: {}'.format(var_name if not helper else helper, dtype))
    else:
        # other type
        if func_default_var is not None:
            parser.add_argument('--{}'.format(var_name), '-{}'.format(abbr_name), type=var_dtype, default=func_default_var, help='{}, default:{}, type:{}'.format(var_name if not helper else helper, func_default_var, var_dtype.__name__))
        else:
            parser.add_argument('--{}'.format(var_name), '-{}'.format(abbr_name), type=var_dtype, required=True, help='{}, type:{}'.format(var_name if not helper else helper, var_dtype.__name__))


def args_abbreviate(func_vars, mode="number"):
    """
    构建一个变量简称的mapper
    """
    abbr_names_cnt = Counter()
    abbreviate_mapper = {}
    alphabet_marker = [0] * 26

    for var in func_vars:
        abbr_name = ''.join(part[0] for part in var.split("_"))
        if abbr_names_cnt[abbr_name] == 0:
            if len(abbr_name) == 1:
                alphabet_marker[ord(abbr_name) - ord('a')] = 1
            abbreviate_mapper[var] = abbr_name
            abbr_names_cnt[abbr_name] += 1
        
        else:
            if mode == "number":
                # 如果简称已经存在，则添加一个数字
                abbr_names_cnt[abbr_name] += 1
                abbreviate_mapper[var] = "{}{}".format(abbr_name, abbr_names_cnt[abbr_name])

            elif mode == "letter":
                # 如果简称已经存在，则寻找下一个不存在的字母
                init_cnt = 0
                while init_cnt < 26 and alphabet_marker[init_cnt] == 1:
                    init_cnt += 1
                
                if init_cnt >= 26:
                    raise ValueError("Too many arguments, cannot abbreviate.")

                abbreviate_mapper[var] = chr(ord('a') + init_cnt)

    return abbreviate_mapper


def helper_builder_from_doc(func_doc):
    """
    如果文档里面有特殊的flag，可以将其转为说明
    """
    var_helper = {}

    if func_doc is None:
        return var_helper
        
    for line in func_doc.split("\n"):
        if line.strip().startswith("@para"):
            match = re.search("@para\s*:\s*([A-Za-z_]*)\s*:(.*)", line)
            if match:
                var_helper[match.group(1)] = match.group(2)

    return var_helper
