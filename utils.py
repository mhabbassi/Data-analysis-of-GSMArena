import requests
import time
import random


def get_url_data(url, tryCount=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    random.seed(14)
    time.sleep(random.randint(a=2, b=6))
    response = requests.get(url=url, headers=headers, timeout=5000)
    if response.status_code == 200:
        return response.text
    else:
        if tryCount < 5:
            time.sleep(2)
            return get_url_data(url=url, tryCount=tryCount + 1)
        return None


def is_not_none_or_empty(value):
    return (
        value is not None
        and value != ""
        and str(value).strip() != "-"
        and str(value) != "None"
    )
