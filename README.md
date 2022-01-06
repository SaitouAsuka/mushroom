# mushroom
A simple tool for generate the console app

# installation
To install Mushroom from source, first clone the repository and then run: python setup.py install

# Basic Usage

You can make your script automatically to be a console app like this:
```PYTHON
import mushroom

def hello(name="World"):
    print("Hello {}".format(name))

if __name__ == "__main__":
    mushroom.Mushroom(hello)
```
Then you can use it like this:

```SHELL
python hello.py --help # print the help documentation
python hello.py --name David # Hello David
python hello.py # Hello World
```


# TODO list
- 模块多命令模式没有实现
- mushroom需要改成单例模式