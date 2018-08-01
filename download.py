#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
def downimage(i):
    sess = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        "Connection": "keep-alive"}
    url = "http://wsxk.hust.edu.cn/randomImage.action"
    image = sess.get(url, headers=headers).content
    with open("./image/"+str(i) + ".jpg", "wb") as f:
        f.write(image)

if __name__ == "__main__":
    for i in range(10):
        downimage(i)