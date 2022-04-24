import mushroom
import requests


@mushroom.mushroom()
def fetch(url:str, timeout:int=5):
    """
    A simple tool for testing ping and fetching url.
    """
    r = requests.get(url, timeout=timeout)
    print(r.status_code)


if __name__ == "__main__":
    fetch()

