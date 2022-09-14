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

## 参数缩写
除了提供长参数外，mushroom还可以提供对应的短参数方便使用。
短参数的构建规则为：
- 参数的首字母为改长参数的短参数，譬如 `-a` 是 `--alpha`的短参数。
- 参数如果由多个单词和下划线组成，则每个单词的首字母拼接后便是短参数。譬如`-fa` 是`--flag_alpha`的短参数。
- 出现短参数冲突时，有两种调整的方法`number`和`letter`
    - `number`主要是在重复的短参数后面加个数字用作区分。目前默认是number，尚未在模块中开放修改参数。
    - `letter`主要是出现重复的短参数后，搜索尚为使用的单字母作为该参数的短参数。

## 参数说明
可以在main入口文档里面写入@para字段，然后给自己的option加上标注。
```
# mushroom_test.py
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
```
然后在命令行输入
```SHELL
> python mushroom_test.py -h

usage: mushroom_test.py [-h] [--nums NUMS] [--name NAME] [--flag_a]

    This is a hello app.

    @para:name:人名
    @para:nums:重复次数
    @para:flag_a:一个flag


optional arguments:
  -h, --help            show this help message and exit
  --nums NUMS, -n NUMS  重复次数, default:3, type:int
  --name NAME, -n2 NAME
                        人名, default:World, type:str
  --flag_a, -fa         一个flag, deafult:False, it will be True if it's applied.
```

# TODO list
- mushroom需要改成单例模式
- 识别main入口文档中parameter字段，然后给option加注释。
- 用inspect模块重写整个模块（待定）。