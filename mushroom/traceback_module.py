from collections import namedtuple
import inspect
import traceback
from mushroom.traceback_terminal import TracebackTerminal


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
    terminal = TracebackTerminal()
    terminal.setup(stacks[::-1])
    terminal.cmdloop()


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
    
    terminal = TracebackTerminal()
    terminal.setup(stacks[::-1], isBreakpoint=True)
    terminal.cmdloop()
    print("="*30)    
        