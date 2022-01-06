from mushroom import Mushroom
import typing

def say(name, me="me"):
    print('Hello {}, this is {}.'.format(name, me))


def adder(a:typing.List[int]):
    print(a)


if __name__ == '__main__':
    app = Mushroom(say)
    app()