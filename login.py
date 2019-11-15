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
        self.configPath = 'config.ini'
        self.captchaPath = 'captcha/0000_00000000.jpg'
        # 登录参数准备
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
        self.s = requests.session()
        self.s.headers = self.headers
        self.s.proxies = self.proxies
        self.config()

    # 读取用户配置信息
    def config(self):
        #  实例化configParser对象
        config = configparser.ConfigParser()
        # -read读取ini文件
        config.read(self.configPath, encoding='utf-8')
        # -get(section,option)得到section中option的值，返回为string类型
        self.username = config.get('userInfo', 'username')
        self.password = config.get('userInfo', 'password')
        self.loginUrl = config.get('web', 'loginUrl')
        # self.imgUrl = config.get('web', 'imgUrl')
        self.govRecvUrl = config.get('web', 'govRecvUrl')
        self.govConfUrl = config.get('web', 'govConfUrl')
        return

    # 将验证码写入文件
    def captchaDownload(self, data):
        with open(self.captchaPath, 'wb') as fp:
            fp.write(data)
        return

    # 准备登陆信息
    def dataMaker(self):
        s = self.s
        page = s.get(self.loginUrl)
        self.jessionId = s.cookies.items()[0][1]
        manual_cookies = RequestsCookieJar()
        manual_cookies.set('loginType', 'normal')
        s.cookies.update(manual_cookies)
        response = page.content
        soup = BeautifulSoup(response, "html.parser")
        lt = soup.find(name="input", attrs={"name": 'lt'}).get("value")
        execution = soup.find(name="input", attrs={"name": 'execution'}).get("value")
        imgUrl = 'http://59.203.198.99:8081/uc-server/imageServlet?now=%d' % (time.time() * 1000)
        imgcodeContent = s.get(imgUrl).content
        self.captchaDownload(imgcodeContent)
        while True:
            imgcode = main()
            print(imgcode)
            if len(str(imgcode)) == 4:
                break
            # 表单内容
        data = {
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit',
            'platform': '',
            'username': self.username,
            'password': self.password,
            'random': imgcode
        }
        return data

    def login(self):
        '''
        登陆模块：
        1.登陆政务通系统，通过session保存登陆状态。（TODO判断登陆是否成功）
        2.点击OA收文系统按钮，获取进一步登陆所需信息。（oaUrl）
        '''
        s = self.s
        # 1.登陆政务通系统
        zwtData = self.dataMaker()
        zwtPage = s.post(self.loginUrl, data=zwtData).content.decode('utf-8')
        print(zwtPage)
        # 2.点击OA收文系统按钮。
        oaPage = s.get('http://59.203.198.93/defaultroot/login.jsp?type=swbl').content.decode('utf-8')
        oaPageSoup = BeautifulSoup(oaPage, 'html.parser')
        domainAccount = oaPageSoup.find(name="input", attrs={"name": 'domainAccount'}).get("value")
        userAccount = oaPageSoup.find(name="input", attrs={"name": 'userAccount'}).get("value")
        userPassword = oaPageSoup.find(name="input", attrs={"name": 'userPassword'}).get("value")
        type = oaPageSoup.find(name="input", attrs={"name": 'type'}).get("value")
        localeCode = oaPageSoup.find(name="input", attrs={"name": 'localeCode'}).get("value")
        pkexit = oaPageSoup.find(name="input", attrs={"name": 'pkexit'}).get("value")
        oaData = {
            'domainAccount': domainAccount,
            'userAccount': userAccount,
            'userPassword': userPassword,
            'type': type,
            'localeCode': localeCode,
            'pkexit': pkexit
        }
        #3.登陆OA系统，





if __name__ == '__main__':
    oa = OARemainder()
    oa.login()
