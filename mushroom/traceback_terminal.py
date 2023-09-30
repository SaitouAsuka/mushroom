import cmd
from pprint import pprint
from collections import deque
import sys
import re


def var_scanner(var_str):
    """
    扫描变量的组成语法

    Args:
        var_str (str): 变量字符串
    """
    attr_pattern = r"(?P<attr_p>\w+)[\.\[]"
    key_pattern = r'\[?[\'"](?P<key_p>\w+)[\'"]\]\.?'
    index_pattern = r'\[?(?P<index_p>\d+)\]'
    final_pattern = r"(?P<final_p>\w+)"

    backbone_pattern = re.compile("|".join([attr_pattern, key_pattern, index_pattern, final_pattern]))
    s = backbone_pattern.scanner(var_str)
    
    return deque([(item.lastgroup, item.group(item.lastgroup)) for item in iter(s.match, None)])


def print_var_func(var_name, global_values, local_values):
    
    tokens = var_scanner(var_name)
    var_ = tokens.popleft()[1]

    def show_detail_attr(base_value, tokens):
        print(tokens)
        while tokens:
            tok_type, tok_name = tokens.popleft()
            try:
                if tok_type == "key_p":
                    # 字典类检索
                    base_value = base_value[tok_name]
                elif tok_type == "index_p":
                    # 索引
                    base_value = base_value[int(tok_name)]
                else:
                    if tok_name == "type":
                        base_value = type(base_value)
                    else:
                        base_value = getattr(base_value, tok_name)
            except Exception as e:
                print("Error : {}".format(e))
                return "attr {} can not be found in {}".format(tok_name, var_name)
        
        return base_value
                

    if var_ in local_values:
        if not tokens:
            pprint("in locals: {} : {}".format(var_name, local_values[var_]))
        else:
            pprint("in locals: {} : {}".format(var_name, show_detail_attr(local_values[var_], tokens)))
    elif var_ in global_values:
        if not tokens:
            pprint("in globals: {} : {}".format(var_name, global_values[var_]))
        else:
            pprint("in globals: {} : {}".format(var_name, show_detail_attr(global_values[var_], tokens)))
    else:
        pprint("can not find the var : {}".format(var_name))


def print_all_var(values, filter_func=lambda x:True):
    keys = [key for key in values.keys() if filter_func(key)]
    keys.sort()
    pprint("; ".join(keys))


class TracebackTerminal(cmd.Cmd):
    
    intro = "Welcome to the shell, type help or ? to list commands.\n"
    prompt = "\033[92m >> \033[0m"
    
    
    # setup current frame
    def setup(self, stacks, isBreakpoint=False):
        self.isBreakpoint = isBreakpoint
        self.stacks = stacks
        self.idx = 0
        self.f = stacks[self.idx].tb_frame
        self.global_values, self.local_values = self.f.f_globals, self.f.f_locals
    
    # basic commands
    def do_print(self, arg):
        """
        打印当前frame里面的变量,可以支持索引以及方法的打印\n
        examle: 
            >> print var_name
            >> print var_name.attr_name
            >> print var_name["key"]
            >> print var_name[1]
            >> print var_name.type
        
        """
        if arg:
            print_var_func(arg, self.global_values, self.local_values)
        else:
            print("Plz input var name")
    
    def do_list(self, arg):
        """打印当前所有的非私有变量,如果是local则打印locals()里面的,如果是global则打印globals()里面的,默认local"""
        if not arg or arg == "local":
            print_all_var(self.local_values, filter_func=lambda x: not x.startswith("__"))
        elif arg== "global":
            print_all_var(self.global_values, filter_func=lambda x: not x.startswith("__"))
        else:
            print("Invaild opition: {}".format(arg))
            
    def do_show(self, arg):
        """打印当前的frame"""
        print(self.f)
        
    def do_back(self, arg):
        """返回上一层堆栈"""
        if self.idx >= len(self.stacks) - 1:
            print("无法再返回上一层")
        else:
            self.idx += 1
            self.f = self.stacks[self.idx].tb_frame
            self.global_values, self.local_values = self.f.f_globals, self.f.f_locals
            print(self.f)
            print("函数名:{}".format(self.f.f_code.co_name))
            
    def do_step(self, arg):
        """进入下层堆栈"""
        if self.idx == 0:
            print("已经是最底层了")
        else:
            self.idx -= 1
            self.f = self.stacks[self.idx].tb_frame
            self.global_values, self.local_values = self.f.f_globals, self.f.f_locals
            print(self.f)
            print("函数名:{}".format(self.f.f_code.co_name))
            
    def do_exit(self, arg):
        sys.exit(0)


    def do_quit(self, arg):
        sys.exit(0)

        
    def do_continue(self, arg):
        """如果是断点，则继续执行。非断点忽视"""
        if self.isBreakpoint:
            return True
        return False

    def do_all(self, arg):
        """打印当前所有的变量,如果是local则打印locals()里面的,如果是global则打印globals()里面的,默认local"""
        if not arg or arg == "local":
            print_all_var(self.local_values)
        elif arg == "global":
            print_all_var(self.global_values)
        else:
            print("Invaild opition: {}".format(arg[0]))
            
            
    