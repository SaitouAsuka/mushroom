import mushroom
import requests


def hello(name="World"):
    print("Hello {}".format(name))


if __name__ == "__main__":
    mushroom.Mushroom(hello)