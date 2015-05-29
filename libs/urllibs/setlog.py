# !/usr/bin/dev python
# -*- coding:utf-8 -*-

from datetime import datetime
import sys


def LogFile(logFile, target_url):
    filePoint = open('{}'.format(logFile), 'a')
    filePoint.write('----------------------------\n\n')
    for i in sys.argv:
        filePoint.write(i + ' ')
    filePoint.write('\n')
    filePoint.write('[*] Crawling URL : {} at :{}\n\n'.format(target_url, str(datetime.now())[: -7]))
    filePoint.close()
