import os
import time
import requests

for i in range(1,130):
    url = f"https://cdn.sunofbeaches.com/emoji/{i}.png"
    res = requests.get(url)
    print(res.content)