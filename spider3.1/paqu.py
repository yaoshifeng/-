import re, operator, os, time
from bs4 import BeautifulSoup
# from functools import reduce #列表去重已经优化
from enum import IntEnum, unique
from download import request
# import requests
import threading
from connect_mysql import sql

IO_lock = threading.Lock()             #建立一个IO锁
MYSQL_infolist_lock = threading.Lock() #建立一个存info数据库的锁
MYSQL_chaplist_lock = threading.Lock() #建立一个存chap数据库的锁
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
    ...
    WEIZHI   = 0   #未知小说

@unique
class Novel_Info(IntEnum):
    BOOK_ID= 0      #书ID
    TYPE   = 1      #类型
    NAME   = 2      #书名
    SERI   = 3      #状态（连载，完本，太监）
    AUTHOR = 4      #作者名字
    UPDATE = 5      #书更新时间
    SUM    = 6      #简介
    ...


url = r'http://www.quanshuwang.com'
server_path = r"C:\Users\Smile\Desktop\项目主要\django-project-novel\demo2"

class spider_class:
    def __init__(self):
        #临时变量
        self.__temp_id   = 0  #__temp开头的都是临时变量，暂时不知道python怎么实现c的static功能！！！
        self.__temp_type = 0
        self.__temp_path = ""
        #类属性
        self.__id = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__maxbook = 10000
        self.__mysql = sql
        self.__type_dict = dict(
            玄幻魔法= Novel_Type['XUANHUAN'].value, 武侠修真= Novel_Type['WUXIA'].value,
            纯爱耽美= Novel_Type['CHUNAI'].value,   都市言情= Novel_Type['DUSHI'].value,
            职场校园= Novel_Type['ZHICHANG'].value, 穿越重生= Novel_Type['CHUANYUE'].value,
            历史军事= Novel_Type['LISHI'].value,    网游动漫= Novel_Type['WANGYOU'].value,
            恐怖灵异= Novel_Type['KONGBU'].value,   科幻小说= Novel_Type['KEHUAN'].value,
            美文名著= Novel_Type['MEIWEN'].value,
            未知类型= Novel_Type['WEIZHI'].value
        )
        self.__seri_dict = dict(
            连载= 0,
            全本= 1,
            太监=-1
        )

    def getHTMLText(self, url, code="utf-8"): #获取网页源码 默认code是utf-8
        try:
            r = request.get(url)
            r.raise_for_status()
            r.encoding = code
            return r.text
        except:
            print(u"获取网页源代码失败 code = %d", r.status_code)

    def getTypeUrl(self, url):
        html = self.getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('a')
        for i in a:
            try:
                yield re.findall(r"http://www.quanshuwang.com/list/[0-1]?[0-9]_1.html", i.attrs['href'])[0]
            except:
                continue
        raise StopIteration

    #优化list查重，避免数据过大list内存泄露
    def getEveryNovelurl(self, url):
        href = ""
        html = self.getHTMLText(url, code="gbk")
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('a', target='_blank')
        for i in a:
            try:
                temp = re.findall(r"http://www.quanshuwang.com/book_[0-9]*.html", i.attrs['href'])[0]
                print(temp)
                if operator.eq(href, temp) is False:
                    href = temp
                    yield temp
            except:
                # print(u"服务器代理出现未知错误getEveryNovelurl")
                continue
        raise StopIteration

    def getChapterCentent(self, url):
        html = self.getHTMLText(url, code="gbk")
        r = r"style5\(\);</script>(.*)<script type=\"text/javascript\">style6\(\)"
        r1 = re.findall(r"var chapter_name = \"(.*)\";", html, re.S)
        r2 = re.findall(r, html, re.S)
        return [r1[0], r2[0]]

    def getChapterList(self, url):
        href = ""
        html = self.getHTMLText(url, code="gbk")
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('a')
        for i in a:
            try:
                temp = re.findall(r"http://www.quanshuwang.com/book/.*.html", i.attrs['href'])[0]
                if operator.eq(href, temp) is False:
                    href = temp
                    yield temp
            except:
                # print(u"服务器代理出现未知错误getChapterList")
                continue
        raise StopIteration

    def getNovelInformation(self, url):
        # print(u"成功进来了:", url)
        html = self.getHTMLText(url, code="gbk")
        soup = BeautifulSoup(html, 'html.parser')
        #image_function
        img_url = self.get_image_url(soup)
        #novel_type_function
        novel_type, novel_id = self.get_novel_type(soup)
        #get_author_function
        novel_author = self.get_novel_author(soup)
        #get_book_name_function
        novel_name = self.get_novel_name(soup)
        #get_seri_function
        novel_seri = self.get_novel_status(soup)
        #get_update_function
        novel_update_time = self.get_novel_updatetime(soup)

        IO_lock.acquire()
        self.build_novel_pic_folder(novel_type, novel_id, img_url)
        # print(u"小说文件夹创建完成")
        IO_lock.release()
        time.sleep(2)

        # MYSQL_infolist_lock.acquire()
        list = [
            #和Novel_Info的枚举一一对应
            novel_id,               #书ID
            novel_type,             #书类型
            novel_name,             #书名
            novel_seri,             #状态
            novel_author,           #作者
            novel_update_time,      #更新时间
            u"暂无简介",            #简介——暂时没弄
                ]
        # self.mysql_save_infolist(list)
        # print(u"存入infolist完毕")
        # MYSQL_infolist_lock.release()
        time.sleep(2)

        MYSQL_chaplist_lock.acquire()
        novel_url = self.get_novel_chapter_url(soup)
        for __url in self.getChapterList(novel_url):
            list_2 = []
            list_2 = self.getChapterCentent(__url)
            print(list_2)
            self.mysql_save_chaplist(list, list_2)
            pass
        MYSQL_chaplist_lock.release()
        time.sleep(2)


    def mysql_save_infolist(self, list):
        self.__mysql.addNoveltoMYSQL(
            # 和Novel_Info的枚举一一对应
            list[Novel_Info["BOOK_ID"].value],
            list[Novel_Info["TYPE"].value],
            list[Novel_Info["NAME"].value],
            list[Novel_Info["SERI"].value],
            list[Novel_Info["AUTHOR"].value],
            list[Novel_Info["UPDATE"].value],
            list[Novel_Info["SUM"].value],
        )

    def mysql_save_chaplist(self, list, list_2):
        self.__mysql.addchaptertoMYSQL(
            # 和Novel_Info的枚举一一对应
            list[Novel_Info["TYPE"].value   ],
            list[Novel_Info["BOOK_ID"].value],
            list[Novel_Info["NAME"].value   ],
            list_2[0],
            list_2[1]
            # list[Novel_Info["CHAPTER"].value],
            # list[Novel_Info["CONTENT"].value][0],#find_all搜索后小说放在list中[0]提取一下 find也可以 不想改了..
        )

    def build_novel_pic_folder(self, novel_type, novel_id, img_url):
        if novel_type == 0:
            return
        self.chdir_novel_pic_main_path()
        self.mkdir_type_folder(novel_type)
        self.mkdir_unit_folder(novel_id)
        self.mkdir_novel_folder(novel_id, img_url)

    def mkdir_type_folder(self, novel_type):
        if not os.path.exists(str(novel_type)):
            os.mkdir(str(novel_type))
        os.chdir(str(novel_type))

    def mkdir_unit_folder(self, novel_id):
        # print("In mkdir_unit_folder-----")

        if not os.path.exists(str(novel_id // 100)):
            os.mkdir(str(novel_id // 100))
        os.chdir(str(novel_id // 100))

    def mkdir_novel_folder(self, novel_id, url):
        # print("In mkdir_novel_folder-----")
        if not os.path.exists(str(novel_id)):
            os.mkdir(str(novel_id))
        os.chdir(str(novel_id))
        self.save_pic(novel_id, url)

    def chdir_novel_pic_main_path(self):
        # print("In chdir_novel_pic_main_path-----")
        novel_pic_main_path = server_path + "\\novel_pic"
        print(novel_pic_main_path)
        if not os.path.exists(novel_pic_main_path):
            os.mkdir(novel_pic_main_path)
        os.chdir(novel_pic_main_path)

    def book_id(self, novel_type):
        # print("type:",novel_type)
        book_id = novel_type * self.__maxbook + self.__id[novel_type] #预计每个类型书存10000本 如果不够改成100000
        self.__id[novel_type] += 1
        return book_id

    #例子http://img.quanshuwang.com/image/159/159426/159426s.jpg
    def save_pic(self, novel_id, url):
        # print(u'开始保存', url)
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open("%ds.jpg" % (novel_id), "wb") as f:
                f.write(r.content)
            f.close()
        except:
            print("%d照片爬取失败", novel_id)

    def start_spider(self):
        try:
            threads = []
            for novel_type_url in self.getTypeUrl(url):  # 捕获12个小说类型的url
                for novel_url in self.getEveryNovelurl(novel_type_url):
                    thread = threading.Thread(target=self.getNovelInformation, args=(novel_url,))
                    threads.append(thread)
                    thread.start()
            for thread in threads:
                thread.join()
                threads.pop(thread)
        except:
            print(u"程序异常结束")

    def get_image_url(self, soup):
        try:
            if len(soup.find_all('meta', property="og:image")) != 0:
                img_url = soup.find_all('meta', property="og:image")[0].attrs['content']
                if "nocover" not in img_url:
                    return img_url
                else:
                    return "暂时无图"
            else:
                return None
        except:
            print(u"爬取图片url出现异常")
            raise Exception

    def get_novel_type(self, soup):
        try:
            if len(soup.find_all('meta', property="og:novel:category")) != 0:
                temp_type = soup.find_all('meta', property="og:novel:category")[0].attrs['content']
                novel_type = self.__type_dict.get(temp_type, 0)
                return novel_type, self.book_id(novel_type)
            else:
                return None, None
        except:
            print(u"爬取小说类型出现异常")
            raise Exception

    def get_novel_author(self, soup):
        try:
            if len(soup.find_all('meta', property="og:novel:author")) != 0:
                novel_author = soup.find_all('meta', property="og:novel:author")[0].attrs['content']
                if len(novel_author) != 0:
                    return novel_author
                else:
                    return "未知作者"
            else:
                return None
        except:
            print(u"爬取作者出现异常")
            raise Exception

    def get_novel_name(self, soup):
        try:
            if len(soup.find_all('meta', property="og:novel:book_name")) != 0:
                novel_name = soup.find_all('meta', property="og:novel:book_name")[0].attrs['content']
                if len(novel_name) != 0:
                    return novel_name
                else:
                    return "未知书名"
            else:
                return None
        except:
            print(u"爬取书名出现异常")
            raise Exception

    def get_novel_status(self, soup):
        try:
            if len(soup.find_all('meta', property="og:novel:status")) != 0:
                temp_seri = soup.find_all('meta', property="og:novel:status")[0].attrs['content']
                return self.__seri_dict.get(temp_seri, -1)
            else:
                return None
        except:
            print(u"爬取状态出现异常")
            raise Exception

    def get_novel_updatetime(self, soup):
        try:
            if len(soup.find_all('meta', property="og:novel:update_time")) != 0:
                novel_update_time = soup.find_all('meta', property="og:novel:update_time")[0].attrs['content']
                if len(novel_update_time) != 0:
                    return novel_update_time
                else:
                    return "未知时间"
            else:
                return None
        except:
            print(u"爬取更新时间出现异常")
            raise Exception

    def get_novel_chapter_url(self, soup):
        try:
            if len(soup.find_all('a', attrs={'class':'reader'})) != 0:
                novel_url = soup.find_all('a', attrs={'class':'reader'})[0].attrs['href']
                return novel_url
            else:
                return None
        except:
            print(u"获取小说链接异常")
            raise Exception

    def run(self):
        if not os.path.exists(server_path):
            print(u"django项目路径错误或没有该项目")
            raise Exception
        #开始爬取
        self.start_spider()


if __name__ == "__main__":
    print(Novel_Type['XUANHUAN'].value)

paqu = spider_class()