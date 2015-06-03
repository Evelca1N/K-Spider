# K-Spider
a spider based on the requirement of KnownSec recuitment

spider.py -u url -d deep -f logfile --testself -thread number --dbfile filepath --key=”HTML5”

##参数说明：##
```
-u 指定爬虫开始地址

-d 指定爬虫深度

--thread 指定线程池大小，多线程爬取页面，可选参数，默认10

--key 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面

-l 日志记录文件，可选参数，默认log文件记录日孩子

-r --regex 正则抓取支持，可以通过正则来对网站的特定内容进行抓取
```
