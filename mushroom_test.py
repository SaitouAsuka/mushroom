import mushroom
import requests


def hello(name:str="World", flag:bool=False):
    """
    This is a hello app.
    """
    print("Hello {}".format(name))
    if flag:
        print("This is True")


if __name__ == "__main__":
    mushroom.Mushroom(hello, timer=True)