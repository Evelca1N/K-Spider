# !/usr/bin/dev python
# -*- coding:utf-8 -*-
# 
# ================================
# This is a spider prom project by c2in
# based on the requirement of Knowsec's recuitment
# 
# version : 1.07 beta        

# fucntion:
# keyword(YES) / deepth(YES) / threadpool(YES) / retrive_html(YES) / 
# information(YES) / sqlite_file & verboseness(NO) / Log_file(YES)

# May 28, 2015
# ================================

from libs.threadpool.threadpool import *
from libs.urllibs.urlfix import *
from libs.urllibs.urlcheck import *
from libs.fontcolor.colorama import *
from libs.urllibs.setlog import *

import urllib2
import sys
import optparse
import time
import pdb

_DEBUG = False


if __name__ == "__main__":

    # 初始化Qin，Qout队列,这里Qin和Qout队列每一个元素都是一个元组，
    # 由（site, deepth)构成
    # Qin, Qout = Queue.Queue(), Queue.Queue()

    # 解析传入的参数，并存入对应的位置
    parser = optparse.OptionParser('\
python K.py -u url --thread=10 --deep=2 --key=keyword')
    parser.add_option('-u',\
            dest='url', help='the url where put the crawlers on')
    parser.add_option('-d', '--deep', dest='deep', help='the deepth lovely \
crawlers dig, default deepth is 1', default=1, metavar='DEEPTH')
    parser.add_option('--thread', dest='thread_num', help='the number of \
thread for crawlers, default thread_num is 10', default=10)
    parser.add_option('-k', '--key', dest='keyword', help='the specifc \
keyword to retrieve with, default is the whole page')
    # parser.add_option('-f', '--file', dest='file', help='the file to \
                # save the crawled data')
    parser.add_option('-l', '--log', dest='log', help='the file to \
record the level of verboseness', default='Log')
    parser.add_option('-r', '--regex', dest='regex', \
            help='the regex pattern to be retrieved') 
    parser.add_option('--time', metavar='second', dest='wait_time', \
            help='time-wait between two request', default=0)

    (options, args) = parser.parse_args()
    if options.url:
        # 修正传递url时前面没有加schema的情况
        options.url = url_fix(options.url)
        print Style.BRIGHT + Fore.YELLOW + \
                    '[-] the parent url is : %s' % options.url,
        print Style.RESET_ALL + Fore.GREEN + Style.BRIGHT

        # 全局参数_DEBUG = True时进入调试模式
        if url_exists(options.url):
            if _DEBUG == True:
                pdb.set_trace()
                pass

            # log记录在特定文件中
            if options.log:
                LogFile(options.log, options.url)

            # 添加根网页，爬虫开始运作
            add_work(options.url)

            # 线程池开始运作
            make_and_start_thread_pool(options.thread_num, \
            options.deep, options.keyword, options.regex, options.wait_time)

            # 每隔5s输出爬虫情况,爬虫爬完退出,有一定延迟
            while not job_finished():
                information = get_crawlers_information()
                if options.deep == 1:
                    time.sleep(2)
                    break
                time.sleep(3)
        else:
            print Style.DIM + Fore.RED + Back.BLACK + \
                    '(i) url %s not accessible !' % options.url[7:],
            print Style.BRIGHT + Fore.YELLOW + Back.RESET
            parser.print_help()
            print Style.RESET_ALL
    else:
        print Style.BRIGHT + Fore.YELLOW
        parser.print_help()
        print Style.RESET_ALL
