#!/usr/bin/env Python
# coding=utf-8
import requests
import re
import random
import time
import sys    
from getip import get_ip
url = 'http://www.xicidaili.com/wt/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie':
        '_free_proxy_session=BAh7B0'
        'kiD3Nlc3Npb25faWQGOgZFVEkiJTZjNzMyYTI1ZTRhZjUwOWFhZmM0MzM3ZDE2OTgxYWE3BjsAVEk'
        'iEF9jc3JmX3Rva2VuBjsARkkiMW56dzJ1TEtEcnhKU295aUZJS0UwOEdrN0FPVTErVlZFNm8xTn'
        'IxaGRXRE09BjsARg%3D%3D--982dd8207a0b42a56678b7a98f0aa1aa02dd4429;'
        'Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1516428973,1516430797; '
        'Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1516436070',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/63.0.3239.132 '
        'Safari/537.36'
}


class download:
    def __init__(self):
        self.ip_list = []
        get_ip(url, headers, self.ip_list)
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get(self, url, timeout = 3, proxy = None, num_retries = 6):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA, 'Referer':'http://www.quanshuwang.com/'} #不赋值防爬虫
        if proxy == None:
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                if num_retries > 0:
                    # time.sleep(3)
                    print('proxy == None 获取网页出错。10秒后将获取倒数第：', num_retries, '次')
                    return self.get(url, timeout, num_retries - 1)
                else:
                    print("开始使用代理")
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.ip_list)).strip())
                    proxy = {'http': IP}
                    print("IP:",IP)
                    return self.get(url, timeout, proxy)
        else:
            try:
                IP = ''.join(str(random.choice(self.ip_list)).strip())
                proxy = {'http': IP}
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                if num_retries > 0:
                    time.sleep(3)
                    IP = ''.join(str(random.choice(self.ip_list)).strip())
                    proxy = {'http': IP}
                    print('proxy == you 正在更换代理，10S后将重新获取倒数第', num_retries, '次')
                    print('当前代理是：', proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print('代理失败，正在重试')
                    return self.get(url, 3)

request = download()
















