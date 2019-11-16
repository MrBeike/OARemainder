# -*- coidng:utf-8 -*-

import os
import re

import demjson
import requests
import win32com.client as wc
from bs4 import BeautifulSoup
from docx import Document


'''
OARemainder:OA收文系统提醒及收文工具。
#工作流程：登陆--获取收文信息(自动巡检)-'-'-'-发现未读信息--自动下载(正文+附件)--关键词检测--通知用户(收文数量+文件名+关键词命中情况)
#编码计划：1.完成收文自动检测+简单提醒(数量+文件名)
'''


class OARemainder:
    def __init__(self):
        self.s = requests.session()
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            # 'Host': '59.203.198.99:8081',
            # 'Referer': 'http://59.203.198.99:8081/uc-server/login'
        }
        self.login()
        self.working_path = os.getcwd()
        self.download_folder = '通知文件下载'

    def login(self):
        '''
        登陆OA收文系统。#TODO 账户密码读取？写入配置文件？判断是否存在？
        :param ：
        :return login_statue: 登陆状态 bool
        '''
        s = self.s
        login_data = {
            'domainAccount': 'whir',
            'userAccount': '370705',
            'userPassword': 'AD3063E152DA7ADD01DA30FEDDE3013F',
            'type': 'swbl',
            'localeCode': 'zh_CN',
            'pkexit': '1',
        }
        login_url = 'http://59.203.198.93/defaultroot/Logon!logon.action'
        login_response = s.post(login_url, data=login_data)
        if login_response.status_code == 200:  # TODO 判断条件 & login_response.content.decode('utf-8') == 'something'
            login_statue = True
        return login_statue

    def docSet(self, type):
        '''
        查询“我的收文”(type=myRecv)和“机要收文”(type=confRecv)中未读文件，返回json字典。
        :param type: 收文类别。
        :return json : 收文所有信息（包括正文名称、下载地址、附件等信息）
        '''
        while True:
            s = self.s
            docSet_url = {'myRecv': 'http://59.203.198.93/defaultroot/GovRecvDocSet!notReadData.action',
                          'confRecv': 'http://59.203.198.93/defaultroot/GovConfRecvDoc!notReadData.action'
                          }
            docSet_data = {
                'tag': 'notRead',
                'queryTitle': '',
                'queryOrg': '',
                'queryNumber': '',
                'queryBeginDate': '',
                'queryEndDate': '',
                'pageSize': '15',
                'orderByFieldName': '',
                'orderByType': '',
                'startPage': 1,
                'pageCount': '1',
                'recordCount': '0'
            }
            docSet_response = s.post(docSet_url[type], data=docSet_data).content.decode('utf-8')
            json = demjson.decode(docSet_response)
            if json['result'] == 'success':
                json_data = json['data']
                break
        print(json_data)
        return json_data

    def jsonParser(self, json):
        '''
        通过解析到的文件json信息，获取正文及附件下载信息。
        :param json:
        :return download_sets:所有文件下载信息 list
        '''
        s = self.s
        docSet_info = json['data']
        # 获取未读信息数量，遍历获取信息
        record = json['pager']['recordCount']
        # 构建所有收文信息list
        download_sets = []
        for i in range(record):
            doc_info = docSet_info[i]

            # 0.构建单个收文下载信息列表list
            download_set = []

            # 1.判断并获取附件下载信息
            if doc_info['accessoryName'] != '':
                accessory_page_data = {
                    'sendFileUserId': doc_info['sendFileUserId'],
                    'empId': doc_info['empId'],
                    'p_wf_tableId': doc_info['tableId'],
                    'p_wf_recordId': doc_info['id']  # 待确认
                }
                accessory_page_url = 'http://59.203.198.93/defaultroot/GovDocSendProcess!viewfile.action'
                accessory_response = s.get(accessory_page_url, data=accessory_page_data).content
                accessory_response_soup = BeautifulSoup(accessory_response, 'html.parser')
                accessory_download_info = accessory_response_soup.findAll(name="a", attrs={
                    "href": re.compile(r"^http://59.203.198.22:8086/defaultroot/public/download/download.jsp?")})

                for i in range(len(accessory_download_info)):
                    accessory_download_url = accessory_download_info[i].get('href')
                    accessory_download_name = accessory_download_info[i].get_text().strip()
                accessory_download_set = {
                    'download_url': accessory_download_url,
                    'download_name': accessory_download_name
                }
                download_set.append(accessory_download_set)

            # 2.获取正文下载信息
            download_data = {
                'verifyCode': doc_info['verifyCode1'],
                'FileName': doc_info['goldGridId'] + doc_info['documentWordType'],
                'name': doc_info['documentSendFileTitle'] + doc_info['documentWordType'],
                'path': 'govdocumentmanager'
            }
            stringlist = []
            for k, v in download_data.items():
                string = '='.join((k, v))
                stringlist.append(string)
                strings = '&'.join(stringlist)
            doc_download_url = 'http://59.203.198.22:8086/defaultroot/public/download/download.jsp?' + strings
            doc_download_name = doc_info['documentSendFileTitle'] + doc_info['documentWordType']
            doc_download_set = {
                'download_url': doc_download_url,
                'download_name': doc_download_name
            }
            download_set.append(doc_download_set)
        download_sets.append(download_set)
        print(download_sets)
        return download_sets

    def docDownload(self, download_sets):
        '''
        解析获取到的下载信息，下载文件，并进行消息提示。
        :param download_sets: 下载文件信息集合 [[{'download_url':url,'download_name':name},{},...]...]
        :return :
        '''
        s = self.s
        for i in range(len(download_sets)):
            download_set = download_sets[i]
            if not os.path.exists(self.download_folder):
                os.mkdir(self.download_folder)
            download_path = os.path.join(self.working_path, self.download_folder,
                                         download_set[-1]['download_name'].split('.')[0])
            for j in range(len(download_set)):
                download_dict = download_set[j]
                download_response = s.get(download_dict['download_url']).content
                with open(download_path + download_dict['download_name'], 'wb') as download_file:
                    download_file.write(download_response)
        return

    # TODO 是遍历文件夹 还是在docDownload功能中保存已下载文件信息，读取操作。
    def docSearch(self, filename, keyword):
        #TODO 读取db文件获取信息，进行转换+打开+搜索
        #TODO 软件是否安装影响本部分程序功能，Try...还是有软件要求。
        #doc文件另存为docx
        word = wc.Dispatch("Word.Application")
        # wps文件另存为docx
        wps = wc.Dispatch('wps.application')
        kwps = wc.Dispatch('kwps.application')
        doc = word.Documents.Open(filename)
        # 上面的地方只能使用完整绝对地址，相对地址找不到文件，且，只能用“\\”，不能用“/”，哪怕加了 r 也不行，涉及到将反斜杠看成转义字符。
        doc.SaveAs(r"", 12)
        # 注意SaveAs会打开保存后的文件，有时可能看不到，但后台一定是打开的
        doc.Close
        word.Quit
        #2.打开文档
        document = Document(filename)
        # 读取每段内容
        lines = [paragraph.text for paragraph in document.paragraphs]
        # 输出并观察结果[-1表示未找到]
        for line in lines:
            text = line.strip()
            if text.find(keyword) != -1:
                flag = True
                break
            else:
                flag = False

    # TODO 通知内容{通知名称，正文是否命中关键词，附件是否命中关键词（如果有），提供文件夹连接}
    def notify(self, json):
        '''
        解析json数据，获取信息系数量record,
        :param json: 获取的json['data']数据
        :return: docSet_info  dict
        '''
        record = json['pager']['recordCount']
        if record == 0:
            msg = '无未读收文'
        else:
            msg = '未读收文{}封'.format(record)
        return msg

    # TODO 是否能通过ftp检索文件名直接下载文件
    def ftp(self):
        '''
        <!--<object classid="clsid:A7EE3B4B-DB6C-4957-A904-DD7EA2BB3DCB"
	id="ActiveFormX2" width="1" height="1" codebase="public/jsp/pdown.cab#version=1.0.19.0">
	<param name="Color" value="15592680">
	<param name="ftpuser" value="ftpuser">
	<param name="ftppwd" value="178whir?!">
	<param name="ftpport" value="21">
	<param name="dddd" value="65432">
	<param name="ftphost" value="59.203.198.22">
	<param name="curpath" value="govdocumentmanager">
</object>-->

        '''
        return


oa = OARemainder()
json = oa.docSet('myRecv')
download_set = oa.jsonParser(json)
oa.docDownload(download_set)
