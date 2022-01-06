from __future__ import absolute_import
from types import FunctionType as function
from mushroom.func_parser import func_parser



def Mushroom(func):
    """
    one command type console app
    """
    rslt = None
    if isinstance(func, function):
        rslt = func_parser(func)


    if rslt:
        # 如果return就会执行输出
        print(rslt)