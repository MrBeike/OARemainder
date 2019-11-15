import requests
import demjson


class OARemainder:
    def __init__(self):
        self.s = requests.session()
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            # 'Host': '59.203.198.99:8081',
            # 'Referer': 'http://59.203.198.99:8081/uc-server/login'
        }

    def login(self):
        '''
        登陆OA收文系统。（TODO账户密码读取？写入配置文件？判断是否存在？）
        :param ：（TODO）
        :return: login_statue(bool)
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
        if login_response.status_code == 200 & login_response.content.decode('utf-8') == 'something':
            login_statue = True
        return login_statue

    def docSet(self, type):
        '''
        查询“我的收文”(type=myRecv)和“机要收文”(type=confRecv)中未读文件，返回json字典。
        :param type: 收文类别。
        :return: json 收文所有信息（包括正文名称、下载地址、附件等信息）
        '''
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
        return json

    def docDownload(self, json):
        '''
        通过查询到的文件json信息，下载正文及附件。
        :param json:
        :return:
        '''
        s = self.s
       