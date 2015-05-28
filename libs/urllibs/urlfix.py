# !/usr/bin/dev python
# -*- coding:utf-8 -*-


def url_fix(target_url):
    return target_url if target_url.startswith('http') else 'http://' + target_url


# 之前想过对url的前缀www进行fix。。。发现想太多了
def url_fi1x(url):
    import urlparse
    target_url = url if url.startswith('http') else 'http://' + url
    # print target_url
    tmp = urlparse.urlparse(target_url)
    # print tmp
    parsed, fixed_url = list(tmp), tmp[0] + '://'
    if not parsed[1].startswith('www'):
        parsed[1] = 'www.' + parsed[1]
    for part in parsed[1:]:
        fixed_url += part
    return fixed_url


if __name__ == '__main__':
    import sys
    print url_fix(sys.argv[1])
