import sys


USAGE_DOC = """
    输入以下指令执行对应动作:
    ?,h,help : 打印帮助
    print {value_name}: 打印{value_name}的值
    list {global, [local]}: 打印所有变量名(不包含隐藏变量),默认打印local
    all {global, [local]}: 打印所有变量名(包含隐藏变量),默认打印local
    show : 打印当前的frame的情况
    back,b : 跳回上一层的堆栈
    step,s : 往下跳一层堆栈
    q,quit,exit: 退出程序
"""


def global_excepthook(ttype,tvalue,ttraceback):
    print("错误类型：{}".format(ttype))
    print("错误信息：{}".format(tvalue))

    stacks = []
    while ttraceback:
        stacks.append(ttraceback)
        ttraceback = ttraceback.tb_next
    interactive_ter(stacks[::-1])


def interactive_ter(stacks):
    # 交互终端设计
    idx = 0
    stacks_depth = len(stacks)

    f = stacks[idx].tb_frame
    global_values = f.f_globals
    local_values = f.f_locals
    while True:
        cmd = input(">> ").strip()
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
                print_all_var(local_values, filter_func=lambda x: not x.startswith("__"))
            elif cmd[-1] == "global":
                print_all_var(global_values, filter_func=lambda x: not x.startswith("__"))
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
        else:
            print("Invaild command : {}".format(cmd))

                
def print_var_func(var_name, global_values, local_values):
    if var_name in local_values:
        print("in locals: {} : {}".format(var_name, local_values[var_name]))
    elif var_name in global_values:
        print("in globals: {} : {}".format(var_name, global_values[var_name]))
    else:
        print("can not find the var : {}".format(var_name))
        

def print_all_var(values, filter_func=lambda x:True):
    keys = [key for key in values.keys() if filter_func(key)]
    print(";".join(keys))