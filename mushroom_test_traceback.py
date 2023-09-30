import mushroom

class A:

    def __init__(self, a):
        self.a = a


def main(a:int, b:float=0):
    tmp = {"1" : [1,23]}
    mushroom.add_breakpoint()
    ta = A(8)
    print(a / b)


if __name__ == '__main__':
    mushroom.Mushroom(main, traceback=True, strict_mode=False)
