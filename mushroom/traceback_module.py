import sys
from pprint import pprint
from collections import namedtuple
import inspect
import traceback


USAGE_DOC = """
    输入以下指令执行对应动作:
    ?,h,help : 打印帮助
    print {value_name}: 打印{value_name}的值
    list {global, [local]}: 打印所有变量名(不包含隐藏变量),默认打印local
    all {global, [local]}: 打印所有变量名(包含隐藏变量),默认打印local
    show : 打印当前的frame的情况
    back,b : 跳回上一层的堆栈
    step,s : 往下跳一层堆栈
    c, continue : 当为断点时，可以直接往后执行。否则直接退出程序。
    q,quit,exit: 退出程序
"""

TB = namedtuple("MyTraceBack", "tb_frame")


def global_excepthook(ttype,tvalue,ttraceback):
    print("错误类型：\033[91m {} \033[0m".format(ttype))
    print("错误信息：\033[91m {} \033[0m".format(tvalue))
    print("=" * 30)
    traceback_details = traceback.format_exception(ttype,tvalue,ttraceback)
    traceback_string = "".join(traceback_details)
    print(traceback_string)
    print("=" * 30)
    stacks = []
    while ttraceback:
        stacks.append(ttraceback)
        ttraceback = ttraceback.tb_next
    interactive_ter(stacks[::-1])


def add_breakpoint():
    """
    获取当前的frame并且启动交互终端设计
    """
    cur_frame = inspect.currentframe()
    print("进入断点...")
    print("断点位置 {}行".format(cur_frame.f_lineno))
    stacks = []
    while cur_frame:
        stacks.append(TB(cur_frame))
        cur_frame = cur_frame.f_back
    
    interactive_ter(stacks[::-1], isBreakPoint=True)
    print("="*30)    


def interactive_ter(stacks, isBreakPoint:bool=False):
    # 交互终端设计
    idx = 0
    stacks_depth = len(stacks)

    f = stacks[idx].tb_frame
    global_values = f.f_globals
    local_values = f.f_locals
    while True:
        cmd = input("\033[92m >> \033[0m").strip()
        if cmd in ("?", "h", "help"):
            print(USAGE_DOC)
        elif cmd.startswith("print"):
            var_name = cmd.split()[-1]
            print_var_func(var_name, global_values, local_values)
        elif cmd.startswith("list"):
            cmd = cmd.split()
            if len(cmd) == 1 or cmd[-1] == "local":
                print_all_var(local_values, filter_func=lambda x: not x.startswith("__"))
            elif cmd[-1] == "global":
                print_all_var(global_values, filter_func=lambda x: not x.startswith("__"))
            else:
                print("Invaild option: {}".format(" ".join(cmd[1:])))
        elif cmd.startswith("all"):
            cmd = cmd.split()
            if len(cmd) == 1 or cmd[-1] == "local":
                print_all_var(local_values)
            elif cmd[-1] == "global":
                print_all_var(global_values)
            else:
                print("Invaild option: {}".format(" ".join(cmd[1:])))
        elif cmd == "show":
            print(f)
        elif cmd in ("back", "b"):
            if idx >= stacks_depth - 1:
                print("无法再返回上一层")
            else:
                idx += 1
                f = stacks[idx].tb_frame
                global_values = f.f_globals
                local_values = f.f_locals
                print(f)
                print("函数名：{}".format(f.f_code.co_name))
        elif cmd in ("step", 's'):
            if idx == 0:
                print("已经是最底层了")
            else:
                idx -= 1
                f = stacks[idx].tb_frame
                global_values = f.f_globals
                local_values = f.f_locals
                print(f)
                print("函数名：{}".format(f.f_code.co_name))
        elif cmd in ("q", 'exit', 'quit'):
            sys.exit(0)
        elif cmd in ('c', 'continue'):
            if isBreakPoint:
                break
            else:
                sys.exit(0)
        else:
            print("Invaild command : {}".format(cmd))

                
def print_var_func(var_name, global_values, local_values):
    attrs = var_name.split(".")
    var_name = attrs.pop(0)
    name_flag = var_name

    def show_attrs(var):
        nonlocal attrs, name_flag
        while attrs:
            cur_attr = attrs.pop(0)
            if cur_attr == 'type':
                return "var {} type : {}".format(var, type(var))
            elif hasattr(var, cur_attr):
                var = getattr(var, cur_attr)
                name_flag += '.{}'.format(cur_attr)
            else:
                var = None
                break
        
        return " {} : {}".format(name_flag, var) if var else "attr {} can not be found in {}".format(cur_attr, var_name)

    if var_name in local_values:
        if not attrs:
            pprint("in locals: {} : {}".format(var_name, local_values[var_name]))
        else:
            pprint(show_attrs(local_values[var_name]))
    elif var_name in global_values:
        if not attrs:
            pprint("in globals: {} : {}".format(var_name, global_values[var_name]))
        else:
            pprint(show_attrs(global_values[var_name]))
    else:
        pprint("can not find the var : {}".format(var_name))
        

def print_all_var(values, filter_func=lambda x:True):
    keys = [key for key in values.keys() if filter_func(key)]
    keys.sort()
    pprint("; ".join(keys))