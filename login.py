#!usr/bin/python
# -*-coding:utf-8-*-

import requests
from requests.cookies import RequestsCookieJar
import time
from bs4 import BeautifulSoup
import numpy as np
import torch
from torch.autograd import Variable
import captcha_setting
import my_dataset
from captcha_cnn_model import CNN

def main():
    cnn = CNN()
    cnn.eval()
    cnn.load_state_dict(torch.load('model.pkl'))
    print("load cnn net.")

    predict_dataloader = my_dataset.get_predict_data_loader()

    for i, (images, labels) in enumerate(predict_dataloader):
        image = images
        vimage = Variable(image)
        predict_label = cnn(vimage)

        c0 = captcha_setting.ALL_CHAR_SET[np.argmax(predict_label[0, 0:captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c1 = captcha_setting.ALL_CHAR_SET[np.argmax(predict_label[0, captcha_setting.ALL_CHAR_SET_LEN:2 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c2 = captcha_setting.ALL_CHAR_SET[np.argmax(predict_label[0, 2 * captcha_setting.ALL_CHAR_SET_LEN:3 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c3 = captcha_setting.ALL_CHAR_SET[np.argmax(predict_label[0, 3 * captcha_setting.ALL_CHAR_SET_LEN:4 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]

        c = '%s%s%s%s' % (c0, c1, c2, c3)
        print(c)
    return c





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
    with open('captcha.jpg', 'wb') as fp:
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
    imgcode = main()
    print(imgcode)
    # 表单内容
    # datas = {
    #     'lt': lt,
    #     'execution': execution,
    #     '_eventId': 'submit',
    #     'platform': '',
    #     'username': '370705',
    #     'password': '050094',
    #     'random': imgcode
    # }
    # return datas
    return



def login():
    s = requests.session()
    s.headers = headers
    dataMaker(s)
# s.proxies = proxies


if __name__ == '__main__':
    login()