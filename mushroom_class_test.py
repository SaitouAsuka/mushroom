import mushroom


class Main(object):
    """
    hello app
    """

    def __init__(self, name="me"):
        self.name = name

    def say_hello(self):
        """
        self intruduce
        """
        print("My name is {}".format(self.name))

    def say_bye(self, other):
        """
        say bye to other
        """
        print("Bye {}".format(other))


if __name__ == '__main__':
    mushroom.Mushroom(Main)