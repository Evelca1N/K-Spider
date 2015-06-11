# !/usr/bin/dev python
# -*- coding:utf-8 -*-
# 线程池模块

import threading
import Queue
import urllib2
import requests
import pdb
import re
from bs4 import BeautifulSoup
from random import randint

from libs.fontcolor.colorama import *
from libs.urllibs.randomAgent import agentList


finished_flag = False   # Flag telling if the spider is stop crawling
Qin = Queue.Queue()     # Queue of uncrawled site
Pool = []               # Thread Pool
deepth_of_crawlers_go = 0   # Deepth of spiders go
spared_thread = 0           # spared_thread
thread_pool_size = 0        # Size of thread pool
informations = {'page':0, 'deepth':0}   # Informations turple
href_list = []          # List of finished url
search_keyword = ''     # Search Keyword
regex_pattern = ''      # Regex pattenr used for matching the specific data
_DEBUG = False          # Debug mode switcher
active_count = 0


headers = {'User-Agent': '',
           'Cookie': ''}


def get_all_from_queue(queue):
    try:
        while True:
            yield queue.get_nowait()
    except Queue.Empty as e:
        filePoint = open('Log', 'a')
        filePoint.write('\n[!] exception at threadpool.py Line 40')
        filePoint.write('\nException : %s\n' % e)
        raise StopIteration


def title_check(title):
    return title[title.rfind('/') + 1:]


def start_crawling_retrieve_html(target_url, now_deepth):
    """Returns the soup_html which conntains the link ref"""

    # fake User-Agent headers to escape from anti-crawling 
    headers['User-Agent'] = agentList[randint(0, len(agentList) - 1)]
    request = requests.get(target_url, headers=headers)
    raw_html = request.content
    soup_html = BeautifulSoup(raw_html, from_encoding='gb18030')
    
    # 有时页面并没有title标签，之前未经过处理所以当title标签唯恐的时候会返回一个异常
    try:
        title = title_check(soup_html.title.string)
    except:
        title = 'None'

    try:
        # 关键字不存在的情况下直接返回, 就算当前页面不含关键字仍然
        # 往当前页面的下级页面进行搜索
        global search_keyword, regex_pattern
        if search_keyword and search_keyword not in raw_html:
            return soup_html
        # 取回当前site的html之后对rePattern进行检查，有匹配的话就保存下来
        if regex_pattern:
            regexPattern(regex_pattern, raw_html)

    except Exception as e:
        filePoint = open('Log', 'a')
        filePoint.write('\n[!] exception at threadpool.py Line 74')
        filePoint.write('\nException : %s\n' % e)
        file_point.close()

    try:
        global active_count
        file_point = open('output/deep%s/"%s".html' % (now_deepth, active_count), 'w')#\
                                # % (now_deepth, title[:70]), 'w')           
        active_count += 1

        # 将爬取到的html数据按照htlm<title>中内容保存到output文件夹
        try:
            # raw_html = raw_html.encode('utf-8')
            file_point.write(raw_html)
            file_point.close()
        except Exception as e:
            filePoint = open('Log', 'a')
            filePoint.write('\n[!] exception at threadpool.py Line 89')
            filePoint.write('\nException : %s\n' % e)
            file_point.close()

    except Exception as e:
        filePoint = open('Log', 'a')
        filePoint.write('\n[!] exception at threadpool.py Line 95')
        filePoint.write('\nException : %s\n' % e)

    return soup_html
    pass


def add_next_deepth_to_queue(soup_html, now_deepth, target_url):
    links = set()
    for link in soup_html.find_all('a'):
        try:
            if link['href'].startswith('http://') \
                        or link['href'].startswith('https://'):
                links.add(link['href'])
            elif link['href'].startswith('/'):
                links.add(target_url + link['href'])

        except Exception as e:
            filePoint = open('Log', 'a')
            filePoint.write('\n[!] exception at threadpool.py Line 112')
            filePoint.write('\nException : %s\n' % e)
    
    for link in links:
        # Qin.put((link, now_deepth))
        add_work(link, now_deepth)


def do_work_from_queue():
    global informations
    global active_count

    while True:

        try:
            target_url, now_deepth = Qin.get(block=True, timeout=3)

            # active_count += 1
            # print 'Active count %s' % active_count
            # 此处可能等待,爬虫从Qin中得到信息元组(target_url, deepth),
            # 另外这里有一点要提一下，timeout需要根据当前网络状况适当调整
        except Queue.Empty:
            global spared_thread, thread_pool_size
            if spared_thread >= int(thread_pool_size):
                try:
                    stop_and_free_thread_pool()
                except NameError as e:
                    # filePoint = open('Log', 'a')
                    # filePoint.write('\n[!] exception at \
                                # threadpool.py Line 138')
                    # filePoint.write('\nException : %s\n' % e)
                    pass
                # break

            spared_thread += 1
            """
            print '(i)spared thread [%s], total thread [%s], \
                    active thread[%s]' % (spared_thread, \
                    int(thread_pool_size), threading.active_count())
            """
            # active_count -= 1
            continue

        informations['page'], informations['deepth'] = \
          informations['page'] + 1, now_deepth \
          if now_deepth > informations['deepth'] else informations['deepth']

        try:
            soup_html = start_crawling_retrieve_html(target_url, now_deepth)
        except Exception as e:
            filePoint = open('Log', 'a')
            filePoint.write('\n[!] exception at threadpool.py Line 169')
            filePoint.write('\nException : %s\n' % e)
            # print 'position 5 with target_url : ' + target_url
            # active_count -= 1
            continue
        # active_count -= 1
        # 当前深度等于爬取最大深度时，
        # 不再把当前深度的下一深度链接放入待爬取队列中
        # 而是直接从队列中取下一个待爬取内容, 
        # 此处考虑直接用break跳出循环的话等于终止了线程，所以使用continue
        # 去队列里面取下一个任务
        if now_deepth == int(deepth_of_crawlers_go):          
            continue
        now_deepth += 1
        add_next_deepth_to_queue(soup_html, now_deepth, target_url)


def regexPattern(regex, raw_html):
    pattern = re.compile(regex)
    matches = pattern.finditer(raw_html)
    groupNum = 1
    parenthesePattern = re.compile(r'(?<!\\)\(.+?\)')
    groupNum += len(parenthesePattern.findall(regex))
    matches = pattern.finditer(raw_html)

    print Fore.RED +  '[*]Accroding Regex Pattern, %s Group Found\
 Regex Matches Are Shown Below:' % groupNum
    for match in matches:
        for i in xrange(1, groupNum):
            print Fore.RED + Style.DIM + match.group(i) + Style.BRIGHT + \
                                                    Fore.GREEN,
        print 


def make_and_start_thread_pool(number_of_thread_in_pool=5, \
                    deepth=1, keyword='', regex='',deamons=True):
    global deepth_of_crawlers_go, thread_pool_size
    global search_keyword, regex_pattern
    deepth_of_crawlers_go, thread_pool_size= deepth, number_of_thread_in_pool
    search_keyword, regex_pattern = keyword, regex

    for i in range(int(number_of_thread_in_pool)):
        new_thread = threading.Thread(target=do_work_from_queue)
        new_thread.setDaemon(deamons)
        Pool.append(new_thread)
        new_thread.start()


def add_work(target_url, deepth=1):
    if target_url not in href_list:
        href_list.append(target_url)
        Qin.put((target_url, deepth))
        # rint href_list, len(href_list)
    else:
        return False


def stop_and_free_thread_pool():
    global Pool, finished_flag
    try:
        for existing_thread in Pool:
            # 这里有一个threading版本引发的问题,join()有可能报错升级可以解决
            existing_thread.join()
    except:
            # print 'positon 7'
            pass
    del Pool
    finished_flag = True
    filePoint.close()


def job_finished():
    global finished_flag
    return finished_flag


def get_crawlers_information():
    global informations, Pool
    # print 'Total page{}'.format(len(Pool))
    print '[-] Totally %s page crawled, deepest deepth is %s'\
            % (informations['page'], informations['deepth'])
    pass   
        

if __name__ == "__main__":
    Qin = Queue.Queue()
    Qout = Queue.Queue()
    Pool = []
    add_work('http://www.hao123.com', 0)
    deepth_of_crawlers_go = 2
    make_and_start_thread_pool()
