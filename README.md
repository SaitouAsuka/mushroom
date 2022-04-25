# mushroom
A simple tool for generate the console app

# Installation

## Install from source code
To install Mushroom from source, first clone the repository and then run: 
```SHELL
python setup.py install
```

## Install from pypi
Or install from pypi through command below:
```PYTHON
pip install mushroom-cli
```

# Basic Usage

You can make your script automatically to be a console app like this:
```PYTHON
import mushroom

def hello(name:str="World"):
    print("Hello {}".format(name))

if __name__ == "__main__":
    mushroom.Mushroom(hello)
```
Or using mushroom in this way(decorator).
```PYTHON
import mushroom

@mushroom.mushroom()
def hello(name:str="World"):
    print("Hello {}".format(name))

if __name__ == "__main__":
    hello()
```
Then you can use it like this:

```SHELL
python hello.py --help # print the help documentation
python hello.py --name David # Hello David
python hello.py # Hello World
```

# Detailed

## 一般用法
该模块只需要引入后直接作用与主入口函数后，便可以识别主入口函数的变量并且生成对应的命令行。

> New:增加了修饰器的使用方式

所以需要主函数在定义传入变量是注明是什么类型的变量,跟例子展示的一样。
没有注明则认为是str类型。

## bool类型
此外该模块也可以支持bool类型的变量，譬如
```PYTHON
import mushroom

def hello(flag:bool=True):
    if flag:
        print("Hello World.")
    else:
        print("Nothing happened.")

if __name__ == "__main__":
    mushroom.Mushroom(hello)
```
这个时候只需要
```SHELL
python hello.py --flag # Nothing happend.
python hello.py # Hello World.
```
因为默认的flag是True,所以传入flag参数的时候则为否。反之亦然。
bool类型的变量只需要 --flag即可

## list类型
也有可能存在需要传入多个参数的情况。这个时候只需要让多参数的变量类型标注为List。
```PYTHON
from typing import List
import mushroom

def my_sum(nums:List[int]):
    return sum(nums)

if __name__ == "__main__":
    mushroom.Mushroom(my_sum)
```
这样可以在命令行中执行：
```SHELL
python sum.py --nums 1 2 3 # 6
```
此外，如果List里面没有标明是什么类型的话，默认为int

## 函数的help doc
如果希望展示自己编写脚本的说明，只需要在编写的时候写对应的文档即可。
```PYTHON
def my_func():
    """
    some document
    """
    pass
```

## 修饰类进行多命令利用

如果有子命令的话，可以构建一个类并且对此进行修饰使用。
```PYTHON
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
```
这个时候 *say_hello* 和 *say_bye* 是 这个脚本的子命令。
当然也可以用修饰器的模式。
```PYTHON
import mushroom


@mushroom.mushroom()
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
    Main()
```


# 其他功能
## 计时
可以对程序的耗时进行计算，只需要将参数timer设置为True即可。
```PYTHON
import mushroom

# @mushroom.mushroom(timer=True)
def hello(name:str="World"):
    print("Hello {}".format(name))

if __name__ == "__main__":
    mushroom.Mushroom(hello, timer=True)
```


# TODO list
- mushroom需要改成单例模式