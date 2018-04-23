#!/usr/bin/env Python
# coding=utf-8
import re, operator, requests
from bs4 import BeautifulSoup
# from functools import reduce #列表去重已经优化
from enum import Enum, IntEnum, unique
from paqu import paqu

if __name__ == '__main__':
    # int_type = 1
    # str_bookid = 19999
    # str_bookname = "ssss"
    # str_chaptername = "1.12345"
    # str_content = "123456789"
    # table = "insert into novel_%d_chapter" \
    #         "(novel_id, novel_name, novel_chapter_name, chapter_content)" \
    #         "values('%d', '%s', '%s', '%s')" % \
    #         ( int_type,
    #           str_bookid, str_bookname, str_chaptername, str_content)
    # print(table)
    #http://www.quanshuwang.com/book/9/9055/9674266.html
    url = "http://www.quanshuwang.com/book/9/9055/9674266.html"
    # getChapterCentent(url)
    spider = paqu
    spider.run()






















