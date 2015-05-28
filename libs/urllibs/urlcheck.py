# !/usr/bin/dev python
# -*- coding:utf-8 -*-

import requests


# 这里默认返回值为3xx的时候也存在网页
def url_exists(target_url):
    try:
        req = requests.head(target_url)
        if req.status_code / 100 in (2, 3):
            return True
        # elif req.status_code / 100 == 3:
            # req = requests.get(target_url)
            # if req.status_code == 200:
                # return True
    except Exception as e:
        # print e
        pass
    return False

if __name__ == "__main__":
    import sys
    print url_exists(sys.argv[1])
