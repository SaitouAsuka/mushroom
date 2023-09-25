import sys, re
from pprint import pprint
from collections import namedtuple, deque
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
    

def cmd_parser(cmd):
    """
    将输入的命令拆分成不同的指令以及给予标签
    """
    single_cmd_pattern = r"(?P<scmd>\w+)"
    double_cmd_pattern = r"(?P<dcmd>\w+)\s+(?P<obj>.+)"

    s = re.compile("|".join([double_cmd_pattern, single_cmd_pattern]))
    mo = s.match(cmd)
    
    if mo.group("scmd"):
        # 单指令
        return {"msg": None, "cmd":mo.group("scmd"), "type":"scmd"}
    elif mo.group("dcmd"):
        # 双指令
        return {"msg": None, "cmd":mo.group("dcmd"), "args":mo.group("obj"), "type": "dcmd"}
    else:
        return {"msg": "Invaild command : {}".format(cmd)}
        
    
def interactive_ter(stacks, isBreakPoint:bool=False):
    # 交互终端设计
    idx = 0

    f = stacks[idx].tb_frame
    global_values, local_values = f.f_globals, f.f_locals
    while True:
        cmd_str = input("\033[92m >> \033[0m").strip()
        
        if not cmd_str:
            continue 
        
        cmd_p = cmd_parser(cmd_str)
        
        if cmd_p["msg"]:
            print(cmd_p["msg"])
            continue    
        
        cmd, opt = cmd_p["cmd"], cmd_p.get("args", [])
        
        if cmd in ("?", "h", "help"):
            print(USAGE_DOC)
        elif cmd == "print":
            if not opt:
                print("Plz apply value...")
            else:
                print_var_func(opt, global_values, local_values)
        elif cmd == "list":
            if not opt or opt == "local":
                print_all_var(local_values, filter_func=lambda x: not x.startswith("__"))
            elif opt == "global":
                print_all_var(global_values, filter_func=lambda x: not x.startswith("__"))
            else:
                print("Invaild option: {}".format(" ".join(opt)))
        elif cmd == "all":
            if not opt or opt == "local":
                print_all_var(local_values)
            elif opt == "global":
                print_all_var(global_values)
            else:
                print("Invaild option: {}".format(" ".join(opt)))
        elif cmd == "show":
            print(f)
        elif cmd in ("back", "b"):
            if idx >= len(stacks) - 1:
                print("无法再返回上一层")
            else:
                idx += 1
                f = stacks[idx].tb_frame
                global_values, local_values = f.f_globals, f.f_locals
                print(f)
                print("函数名：{}".format(f.f_code.co_name))
        elif cmd in ("step", 's'):
            if idx == 0:
                print("已经是最底层了")
            else:
                idx -= 1
                f = stacks[idx].tb_frame
                global_values, local_values = f.f_globals, f.f_locals
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
            print("Invaild command : {}".format(cmd_str))