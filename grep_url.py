import mushroom
import requests


def fetch(url:str, timeout:int=5):
    r = requests.get(url, timeout=timeout)
    print(r.status_code)


if __name__ == "__main__":
    mushroom.Mushroom(fetch)

