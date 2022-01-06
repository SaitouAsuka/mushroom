from __future__ import absolute_import
from types import FunctionType as function
from mushroom.func_parser import func_parser



class Mushroom(object):
    """
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            Mushroom._instance = object.__new__(cls)
        return Mushroom._instance

    def __init__(self, func:function):
        """
        """
        self.func = func

    def __call__(self):
        """
        """
        if isinstance(self.func, function):
            func_parser(self.func)