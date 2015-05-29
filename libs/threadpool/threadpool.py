# !/usr/bin/dev python
# -*- coding:utf-8 -*-
# 线程池模块

import threading
import Queue
from bs4 import BeautifulSoup
import urllib2
import requests
import pdb


finished_flag = False
Qin = Queue.Queue()
Pool = []
deepth_of_crawlers_go = 0
spared_thread = 0
thread_pool_size = 0
informations = {'page':0, 'deepth':0}
href_list = []
search_keyword = ''
_DEBUG = False
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0'}

filePoint = open('Log', 'a')


def get_all_from_queue(queue):
    try:
        while True:
            yield queue.get_nowait()
    except Queue.Empty as e:
        filePoint.write('[!] exception at threadpool.py Line 33\n')
        filePoint.write('\nException : %s' % e)
        raise StopIteration


def title_check(title):
    try:
        return title[title.rfind('/') + 1:]
    except:
        return 'None'


def start_crawling_retrieve_html(target_url, now_deepth):
    # print target_url
    save_flag = True
    request = requests.get(target_url, headers=headers)
    raw_html = request.content
    soup_html = BeautifulSoup(raw_html, from_encoding='gb18030')
    title = soup_html.title.string
    title = title_check(title)

    # 关键字不存在的情况下直接返回
    global search_keyword
    if search_keyword:
        if search_keyword not in raw_html:
            return soup_html

    try:
        file_point = open('output/deep%s/"%s".html' % (now_deepth, title[:70]), 'w')           # 将爬取到的html数据按照htlm<title>中内容保存到output文件夹
        try:
            raw_html = raw_html.encode('utf-8')
            file_point.write(raw_html)
            file_point.close()
        except Exception as e:
            filePoint.write('[!] exception at threadpool.py Line 67\n')
            filePoint.write('\nException : %s' % e)
            file_point.close()

    except Exception as e:
        filePoint.write('[!] exception at threadpool.py Line 72\n')
        filePoint.write('\nException : %s' % e)

    return soup_html
    pass


def add_next_deepth_to_queue(soup_html, now_deepth, target_url):
    links = set()
    for link in soup_html.find_all('a'):
        try:
            if link['href'].startswith('http://') or link['href'].startswith('https://'):
                links.add(link['href'])
            elif link['href'].startswith('/'):
                links.add(target_url + link['href'])
        except Exception as e:
            filePoint.write('[!] exception at threadpool.py Line 88\n')
            filePoint.write('\nException : %s' % e)
    
    for link in links:
        # Qin.put((link, now_deepth))
        add_work(link, now_deepth)


def do_work_from_queue():
    global informations
    # global spared_crawlers
    while True:

        try:
            target_url, now_deepth = Qin.get(block=True, timeout=6)      
            # 此处可能等待,爬虫从Qin中得到信息元组(target_url, deepth),
            # 另外这里有一点要提一下，timeout需要根据当前网络状况适当调整
        except Queue.Empty:
            global spared_thread, thread_pool_size
            if spared_thread >= int(thread_pool_size):
                try:
                    stop_and_free_thread_pool()
                except NameError as e:
                    filePoint.write('[!] exception at threadpool.py Line 67\n')
                    filePoint.write('\nException : %s' % e)
                break

            spared_thread += 1
            # print '(i)spared thread [%s], total thread [%s], active thread[%s]' % (spared_thread, int(thread_pool_size), threading.activeCount())

            continue

        # print '[-]crawlers are at %s , deepth:[%s]' % (target_url, now_deepth)
        informations['page'], informations['deepth'] = informations['page'] + 1, now_deepth if now_deepth > informations['deepth'] else informations['deepth']

        try:
            soup_html = start_crawling_retrieve_html(target_url, now_deepth)
        except Exception as e:
            filePoint.write('[!] exception at threadpool.py Line 127\n')
            filePoint.write('\nException : %s' % e)
            # print 'position 5 with target_url : ' + target_url

        # 当前深度等于爬取最大深度时，
        # 不再把当前深度的下一深度链接放入待爬取队列中
        # 而是直接从队列中取下一个待爬取内容, 
        # 此处考虑直接用break跳出循环的话等于终止了线程，所以使用continue
        if now_deepth == int(deepth_of_crawlers_go):          
            # spared_crawlers += 1
            # print 'spared crawlers[%s]' % spared_crawlers
            # if spared_crawlers == 5:
            #     pass
                # break_all()
            continue
        now_deepth += 1
        add_next_deepth_to_queue(soup_html, now_deepth, target_url)
        

def make_and_start_thread_pool(number_of_thread_in_pool=5, deepth=1, keyword='', deamons=True):
    global deepth_of_crawlers_go, thread_pool_size, search_keyword
    deepth_of_crawlers_go, thread_pool_size, search_keyword = deepth, number_of_thread_in_pool, keyword

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
    print '[-] Totally %s page crawled, deepest deepth is %s' % (informations['page'], informations['deepth'])
    pass   
        

if __name__ == "__main__":
    Qin = Queue.Queue()
    Qout = Queue.Queue()
    Pool = []
    add_work('http://www.hao123.com', 0)
    deepth_of_crawlers_go = 2
    make_and_start_thread_pool()

