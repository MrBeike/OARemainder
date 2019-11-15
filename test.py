import requests
import demjson
s = requests.session()
data = {
    'domainAccount': 'whir',
    'userAccount': '370705',
    'userPassword': 'AD3063E152DA7ADD01DA30FEDDE3013F',
    'type': 'swbl',
    'localeCode': 'zh_CN',
    'pkexit': '1',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    # 'Host': '59.203.198.99:8081',
    # 'Referer': 'http://59.203.198.99:8081/uc-server/login'
}

url = 'http://59.203.198.93/defaultroot/Logon!logon.action'

response = s.post(url, headers=headers, data=data)
# print(response.status_code, response.content.decode('utf-8')

#“我的收文”中未读查询，返回json.
notreadUrl = 'http://59.203.198.93/defaultroot/GovRecvDocSet!notReadData.action?tag=notRead&queryTitle=&queryOrg=&queryNumber=&queryBeginDate=&queryEndDate=&pageSize=15&orderByFieldName=&orderByType=&startPage=1&pageCount=1&recordCount=0'
notreadresponse = s.post(notreadUrl,headers=headers).content.decode('utf-8')
print(notreadresponse,type(notreadresponse))
json = demjson.decode(notreadresponse)

#“机要收文”中未读查询，返回json.
notreadUrl2 = ' http://59.203.198.93/defaultroot/GovConfRecvDoc!notReadData.action?tag=notRead&queryTitle=&queryOrg=&queryNumber=&queryBeginDate=&queryEndDate=&pageSize=15&orderByFieldName=&orderByType=&startPage=1&pageCount=1&recordCount=0'

pdf = 'http://59.203.198.22:8086/defaultroot/public/download/download.jsp?FileName=2019111216151339301503334.pdf&amp;verifyCode=B2A0C3D279FileName00&amp;name=2019.11.12%E5%85%B3%E4%BA%8E%E4%B8%BE%E5%8A%9E%E5%85%A8%E5%8E%BF%E2%80%9C%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD%E2%80%9D%E4%B8%BB%E9%A2%98%E6%95%99%E8%82%B2%E7%9F%A5%E8%AF%86%E7%AB%9E%E8%B5%9B%E5%86%B3%E8%B5%9B%E7%9A%84%E9%80%9A%E7%9F%A5%283%29.pdf&amp;path=govdocumentmanager" target="_blank" style="cursor:hand"><font size="4">2019.11.12关于举办全县“不忘初心、牢记使命”主题教育知识竞赛决赛的通知(3).pdf'
response = s.get(pdf,headers=headers)
print(response.status_code,response.content)