from __future__ import absolute_import
from types import FunctionType as function
from mushroom.func_parser import func_parser



def Mushroom(func):
    """
    one command type console app
    """
    if isinstance(func, function):
        func_parser(func)