# !/usr/bin/dev python
# -*- coding:utf-8 -*-
# =======================
# `urlexist` Module used for determine if a url exists
# =======================
# >>> import httpExists
# >>> httpExists.httpExists('http://www.python.org/')
# True
# >>> httpExists.httpExists('http://www.python.org/PenguinOnTheTelly')
# Status 404 Not Found : http://www.python.org/PenguinOnTheTelly
# False
# =======================

import httplib, urlparse, sys


def urlexist(url):
    host, path = urlparse.urlsplit(url)[1:3]
    if ':' in host:
        host, port = host.split(':')
        try:
            port = int(port)
        except ValueError:
            print 'invalid port number %r' % port
            return False
    else:
        port = None
    try:
        conn = httplib.HTTPConnection(host, port=port)
        conn.request('HEAD', path)
        res = conn.getresponse()
        if res.status == 200:
            retval = True
        else:
            print '[*]status %d %s:%s ' % (res.status, res.reason, url)
            retval = False
    except Exception as e:
        print e.__class__, e, url
        retval = False
    return retval


def _test():
    import doctest, urlexist
    return doctest.testmod(urlexist)
    
if __name__ == "__main__":
    _test()
    url = raw_input('[*]examing url:\n')
    url = url if url.startswith('http') else 'http://' + url
    if urlexist(url):
        print 'yes'
    else:
        print 'no'
