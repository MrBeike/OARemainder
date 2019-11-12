#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
使用自建的接口识别来自网络的验证码
需要配置参数：
    remote_url = "https://www.xxxxxxx.com/getImg"  验证码链接地址
    rec_times = 1  识别的次数
"""
import requests
from io import BytesIO
import json


def recognize_captcha(test_path, image_suffix):
    image_file_name = 'captcha.{}'.format(image_suffix)

    with open(test_path, "rb") as f:
        content = f.read()

    # RESTful API识别
    url = "http://127.0.0.1:6000/b"
    files = {'image_file': (image_file_name, BytesIO(content), 'application')}
    r = requests.post(url=url, files=files)

    # 识别结果
    predict_text = json.loads(r.text)["value"]
    return predict_text

def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)
    # 配置相关参数
    test_path = "captcha.jpg"  # 测试识别的图片路径
    image_suffix = sample_conf["image_suffix"]  # 文件后缀
    code = recognize_captcha(test_path, image_suffix)
    return code

