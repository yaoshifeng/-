#!/usr/bin/env Python
# coding=utf-8
import urllib.request as urllib
import requests, re, operator
from bs4 import BeautifulSoup
# from functools import reduce #列表去重已经优化
from enum import Enum, IntEnum, unique
from download import request
from connect_mysql import sql


@unique
class Novel_Type(IntEnum):
    XUANHUAN =  1   #玄幻魔法
    WUXIA    =  2   #武侠修真
    CHUNAI   =  3   #纯爱耽美
    DUSHI    =  4   #都市言情
    ZHICHANG =  5   #职场校园
    CHUANYUE =  6   #穿越重生
    LISHI    =  7   #历史军事
    WANGYOU  =  8   #网游动漫
    KONGBU   =  9   #恐怖灵异
    KEHUAN   = 10   #科幻小说
    MEIWEN   = 11   #没问名著

@unique
class Novel_Info(IntEnum):
    ID     = 0
    NAME   = 1
    TYPE   = 2
    SERI   = 3
    AUTHOR = 4
    URL    = 5
    SUM    = 6


url = 'http://www.quanshuwang.com'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) " \
                   "AppleWebKit/537.36 (KHTML, like Gecko) " \
                   "Chrome/58.0.3029.110 " \
                   "Safari/537.36"
}




def getHTMLText(url, code="utf-8"): #获取网页源码 默认code是utf-8
    try:
        r = request.get(url, 3)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("获取网页源代码失败")


def getTypeUrl(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            yield re.findall(r"http://www.quanshuwang.com/list/[0-1]?[0-9]_1.html", i.attrs['href'])[0]
        except:
            continue
    raise StopIteration


#优化list查重，避免数据过大list内存泄露
def getEveryNovelurl(url):
    href = ""
    html = getHTMLText(url, code="gbk")
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', target='_blank')
    for i in a:
        try:
            temp = re.findall(r"http://www.quanshuwang.com/book_[0-9]*.html", i.attrs['href'])[0]
            if operator.eq(href, temp) is False:
                href = temp
                yield temp
        except:
            continue
    raise StopIteration


def getChapterCenter(url):
    html = getHTMLText(url, code="gbk")
    r = r"style5\(\);</script>(.*)<script type=\"text/javascript\">style6\(\)"
    return re.findall(r, html, re.S)

def getNovelInformation(url):
    print("成功进来了:", url)
    html = getHTMLText(url, code="gbk")
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find_all('meta', property="og:image")[0].attrs['content']
    temp_type = soup.find_all('meta', property="og:novel:category")[0].attrs['content']
    novel_author = soup.find_all('meta', property="og:novel:author")[0].attrs['content']
    novel_name = soup.find_all('meta', property="og:novel:book_name")[0].attrs['content']
    novel_seri = soup.find_all('meta', property="og:novel:status")[0].attrs['content']
    novel_update_time = soup.find_all('meta', property = "og:novel:update_time")[0].attrs['content']
    novel_chapter_name = \
        soup.find_all('meta', property="og:novel:latest_chapter_name")[0].attrs['content']
    novel_chapter_url = \
        soup.find_all('meta', property="og:novel:latest_chapter_url")[0].attrs['content']
    novel_chapter_content = getChapterCenter(novel_chapter_url)
    print(img_url)
    print(temp_type)
    print(novel_author)
    print(novel_name)
    print(novel_seri)
    print(novel_update_time)
    print(novel_chapter_name)
    print(novel_chapter_url)
    print(novel_chapter_content)


if __name__ == '__main__':
    mysql = sql
    try:
        for i in getTypeUrl(url): #捕获12个小说类型的url
            print("novel_url_type: ", i)
            for j in getEveryNovelurl(i):
                getNovelInformation(j)
    except:
        print("程序异常结束")





















