# -*- coding: utf-8 -*-
#warning:This crawl just works for My Python Study, Not for commercial use
'''
#author : yaoshifeng
#time   : 2018.03.09 9:19
#version: 2.0
#function: crawl all the novels of the www.quanshuwang.com, 40 books every channel
'''
import urllib.request as urllib
# import urllib.request as urllib
import requests
import re
import os
import pymysql

STATIC_PATH = 'e:\python_demo\\novelapp\static'
PIC_PATH = STATIC_PATH + '\\' + "pic\\"

class sql():
    def __init__(self):
        self.cur
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='demo2',
        charset='utf8',
    )

    def connecttoMYSQL(self):
        self.cur = self.conn.cursor()
        return

    def disconnecttoMYSQL(self):
        self.cur = self.conn.commit()
        return

    def addChanneltoMYSQL(self, num, name):
        self.cur.execute(
            "insert into " \
            "novel_channel(channel_num, channel_name) " \
            "values('%s', '%s') % (num, name)"
        )
        self.cur.close()
        return
  
    def addNoveltoMYSQL(self, str_bookid, str_channelname, str_bookname, str_author):
        self.cur.execute(
            "insert into " \
            "novel_info(id, novel_name, author, channel_name) " \
            "values('%s', '%s', '%s', '%s') % (str_bookid, str_channelname, str_bookname, str_author)"
        )
        return

    def addPicStatustoMYSQL(self, str_bookid, str_picname, int_status):
        if str_picname.find("nocover") == -1:
            str_picname = "none"
        self.cur.execute(
            "insert into " \
            "novel_pic(id, novel_pic_name, status) " \
            "values('%s', '%s', '%d') % (str_bookid, str_picname, int_status)"
        )
        return


class no_name():
    def __init__(self, id):
        self.channel_num = id  #channel的num
    '''
    Name     : getNovelChannel()
    By       : Yao Shifeng
    Parameter: 
    Function : get urls of channels and channel name in a list element
    Return   : return a list[(url, channel_name), ...]
    Time     : 
    '''
    def getNovelChannel(self):
        html = urllib.urlopen("http://www.quanshuwang.com/").read().decode('gbk').encode('utf-8').decode('utf-8')
        ref = '<li><a href="(.*_1.html)">(.*?)</a></li>'
        channelList = re.findall(ref, html)
        print("urlList: ", channelList)
        return channelList

    '''
    Name     : getNovelUrl(url)
    By       : Yao Shifeng
    Parameter: url(url of channel)
    Function : get url of novel, novel name and author in a list element
    Return   : return a list[(url, novel_name, author), ...]
    Time     : 
    '''
    def getNovelUrl(self, url):
        if urllib.urlopen(url).code != 200:
            print("进入%s网页失败", url)
            return
        html = urllib.urlopen(url).read().decode("gbk").encode("utf8").decode("utf8")
        ref = 'src="(.*)" ' \
              'alt=".*?" width="120" height="150"></a>.*'\
              '<a target="_blank" title=".*?" href="(.*book_[0-9]{6}.html)" '\
              'class="clearfix stitle">(.*)</a>' \
              '作者：<a href=".*?">(.*?)</a><em class="c999 clearfix">'
        novelUrlList = re.findall(ref, html)
        pic_path = PIC_PATH + "%d\\" % (self.channel_num)
        # print(len(novelUrlList))
        for i in range(0, len(novelUrlList)):
            print(("正在下载第%d个图片") % (i))
            if os.path.exists(pic_path) == 0:
                os.mkdir(pic_path)
            else:
                try:
                    r = requests.get(novelUrlList[i-1][0])
                    r.raise_for_status()
                    # if r.status_code == 200:
                    with open(pic_path + "%d_%d.jpg" % (self.channel_num, i), "wb") as f:
                        f.write(r.content)
                    f.close()
                except:
                    print("第%d个照片爬取失败" % (i) )
        print("novelUrlList:", novelUrlList)
        return


test1 = no_name(0)
testchannel = test1.getNovelChannel()
testnovel = test1.getNovelUrl(testchannel[0][0])



















