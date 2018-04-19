import urllib.request
from bs4 import BeautifulSoup
import threading
import time  
import random
import socket

ip_list = []
ip_ok = []
lock = threading.Lock() #建立一个锁
url = 'http://www.xicidaili.com/wt/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTZjNzMyYTI1ZTRhZjUwOWFhZmM0MzM3ZDE2OTgxYWE3BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMW56dzJ1TEtEcnhKU295aUZJS0UwOEdrN0FPVTErVlZFNm8xTnIxaGRXRE09BjsARg%3D%3D--982dd8207a0b42a56678b7a98f0aa1aa02dd4429; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1516428973,1516430797; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1516436070',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def get_ip(url, headers, ip_list=[]):
    '''
    :param url:     代理网站
    :param headers: http访问头文件
    :param iplist:  保存ip的列表
    :return:        无
    '''
    for page in range(6, 9):
        print("page: ", page)
        url=url + str(page)
        request = urllib.request.Request(url=url, headers=headers)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print("page: ", page, ' ', e.code)
            return
        except urllib.error.URLError as e:
            print("page: ", page, ' ', e.reason)
            return
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {'id':'ip_list'})
        trs = table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 0:
                # print(tds[1].get_text(), tds[2].get_text())
                ip_list.append(tds[1].get_text())# + '+' + tds[2].get_text())
        time.sleep(random.choice(range(1, 3)))


def test(ip):
    socket.setdefaulttimeout(5) #设置全局超时时间
    url = "http://www.mzitu.com/xinggan/"  # 打算爬取的网址
    try:
        proxy = {'http':ip }
        proxy_support = urllib.request.ProxyHandler
        opener = urllib.request.build_opener(proxy_support)
        opener.addheaders = [("User-Agent",
                              "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/63.0.3239.132 Safari/537.3")]
        urllib.request.install_opener(opener)
        res = urllib.request.urlopen(url).read()
        lock.acquire()
        print(proxy, "is OK")
        ip_ok.append(proxy)
        lock.release()

    except Exception as e:
        lock.acquire()
        print(proxy, "is EOR")
        lock.release()


if __name__ == '__main__':
    get_ip(url, headers, ip_list)
    print(ip_list)
    #多线程验证
    threads = []
    for ip in ip_list:
        thread = threading.Thread(target = test, args=(ip, ))
        threads.append(thread)
        thread.start()

    #阻塞主进程， 等待所有子进程结束
    for thread in threads:
        thread.join()
    print(ip_ok)
