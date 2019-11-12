#!usr/bin/python
# -*-coding:utf-8-*-

import requests
from requests.cookies import RequestsCookieJar
import time
from bs4 import BeautifulSoup
from captcha_predict import main

# 登录参数准备
loginUrl = 'http://59.203.198.99:8081/uc-server/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Host': '59.203.198.99:8081',
    'Referer': 'http://59.203.198.99:8081/uc-server/login'
}
# 系统代理（测试用）
proxies = {
    'http': '127.0.0.1:8888',
    'https': '127.0.0.1:8888',
}


# 验证码四位数字 去空格 识别为空处理[未完成]
def captchaDownload(data):
    with open('captcha/0000_00000000.jpg', 'wb') as fp:
        fp.write(data)
    return


def dataMaker(s):
    # page = s.get(loginUrl)
    # manual_cookies = RequestsCookieJar()
    # manual_cookies.set('loginType', 'normal')
    # print(page.status_code, s.cookies)
    # s.cookies.update(manual_cookies)
    # print(s.cookies)
    # response = page.content
    # soup = BeautifulSoup(response, "html.parser")
    # lt = soup.find(name="input", attrs={"name": 'lt'}).get("value")
    # execution = soup.find(name="input", attrs={"name": 'execution'}).get("value")
    # imgUrl = 'http://59.203.198.99:8081/uc-server/imageServlet?now=%d' % (time.time() * 1000)
    # imgcodeContent = s.get(imgUrl).content
    # captchaDownload(imgcodeContent)
    while True:
        imgcode = main()
        if len(str(imgcode)) == 4:
            break
        # 表单内容
    datas = {
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'platform': '',
        'username': '370705',
        'password': '050094',
        'random': imgcode
    }
    return datas


def login():
    s = requests.session()
    s.headers = headers
    dataMaker(s)


# s.proxies = proxies


if __name__ == '__main__':
    login()
