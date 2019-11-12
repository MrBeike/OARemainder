#!usr/bin/python
# -*-coding:utf-8-*-

import requests
import time
import configparser
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from captcha_predict import main


class OARemainder:
    def __init__(self):
        self.configPath = 'captcha/config.ini'
        self.captchaPath = 'captcha/0000_00000000.jpg'
        # 登录参数准备
        self.loginUrl = 'http://59.203.198.99:8081/uc-server/login'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Host': '59.203.198.99:8081',
            'Referer': 'http://59.203.198.99:8081/uc-server/login'
        }
        # 系统代理（测试用）
        self.proxies = {
            'http': '127.0.0.1:8888',
            'https': '127.0.0.1:8888',
        }
        self.s = requests.session(headers=self.headers)

    # 读取用户配置信息
    def config(self):
        #  实例化configParser对象
        config = configparser.ConfigParser()
        # -read读取ini文件
        config.read(self.configPath, encoding='utf-8')
        # -get(section,option)得到section中option的值，返回为string类型
        self.username = config.get('userInfo', 'username')
        self.password = config.get('userInfo', 'password')
        return

    # 将验证码写入文件
    def captchaDownload(self, data):
        with open(self.capthchaPath, 'wb') as fp:
            fp.write(data)
        return

    # 准备登陆信息
    def dataMaker(self):
        s = self.s
        page = s.get(self.loginUrl)
        manual_cookies = RequestsCookieJar()
        manual_cookies.set('loginType', 'normal')
        print(page.status_code, s.cookies)
        s.cookies.update(manual_cookies)
        print(s.cookies)
        response = page.content
        soup = BeautifulSoup(response, "html.parser")
        lt = soup.find(name="input", attrs={"name": 'lt'}).get("value")
        execution = soup.find(name="input", attrs={"name": 'execution'}).get("value")
        imgUrl = 'http://59.203.198.99:8081/uc-server/imageServlet?now=%d' % (time.time() * 1000)
        imgcodeContent = s.get(imgUrl).content
        self.captchaDownload(imgcodeContent)
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
            'username': self.username,
            'password': self.password,
            'random': imgcode
        }
        return datas

    def login(self):
        s = self.s
        datas = self.dataMaker()
        response = s.post(self.loginUrl, datas=datas).content


if __name__ == '__main__':
    oa = OARemainder()
