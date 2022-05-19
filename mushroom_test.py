import mushroom
import requests


def hello(nums:int=3, name:str="World", flag_a:bool=False):
    """
    This is a hello app.
    """
    print("Hello {}".format(name))
    print("times:{}".format(nums))
    if flag_a:
        print("This is True")


if __name__ == "__main__":
    mushroom.Mushroom(hello, timer=True)