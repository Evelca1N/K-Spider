# !/usr/bin/dev python
# -*- coding:utf-8 -*-

import requests


headers = {
        """
        'Host': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10;\
 rv:38.0) Gecko/20100101 Firefox/38.0',
        'Cookie': '
        """
        'Connection': 'keep-alive'
}


# 这里默认返回值为3xx的时候也存在网页
def url_exists(target_url):
    try:
        req = requests.head(target_url, timeout=5, headers=headers)
        # print req.status_code
        if req.status_code / 100 in (2, 3):
            return True
    except Exception as e:
        print e
        pass
    return False

if __name__ == "__main__":
    import sys
    print url_exists(sys.argv[1])
    print 'wrote done'
