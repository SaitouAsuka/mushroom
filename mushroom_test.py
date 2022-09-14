import mushroom


def hello(nums:int=3, name:str="World", flag_a:bool=False):
    """
    This is a hello app.

    @para:name:人名
    @para:nums:重复次数
    @para:flag_a:一个flag
    """
    print("Hello {}".format(name))
    print("times:{}".format(nums))
    if flag_a:
        print("This is True")


if __name__ == "__main__":
    mushroom.Mushroom(hello, timer=True)