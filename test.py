# import sqlite3


# class DataBase:
#     def __init__(self, sql):
#         '''
#         :param sql --a dict of sql commands.
#         include  the command to create table/add data to the table as well as define the datebase filename.
#         '''
#         self.sql = sql
#         self.conn = sqlite3.connect(self.sql['db_name'])
#         self.create_table()

#     def create_table(self):
#         try:
#             self.conn.execute(self.sql['create_table'])
#             self.conn.commit()
#         except:
#             print('create table failed')
#             return False

#     def add_data(self, data):
#         '''
#         :param data --a dict or list.
#         :return: None
#         '''
#         data = data
#         sql = self.sql['add_data']
#         sql = eval(sql)
#         self.conn.execute(sql[0], sql[1])
#         self.conn.commit()
#         return

#     def read_data(self):
#         '''
#         :return: data --a table like  structure list
#         '''
#         try:
#             cur = self.conn.cursor()
#             cur.execute(self.sql['read_data'])
#             data = cur.fetchall()
#             self.conn.commit()
#             return data
#         except sqlite3.OperationalError as e:
#             print("没有保存的数据", e)
#             return False

#     def close(self):
#         try:
#             self.conn.close()
#         except:
#             return


# user_create = '''
# CREATE TABLE IF NOT EXISTS oa(
# id       INTEGER  PRIMARY KEY,
# name  NOT NULL ,
# accessory   NOT NULL,
# keyword NOT NULL,
# flag     NOT NULL);
# '''
# # user_add_data  = '\"replace into user(account,passwd,name) values ({loginId},{passwd},{name})\"'
# user_add_data = '\"REPLACE INTO USER (ACCOUNT,PASSWD,NAME) VALUES (?,?,?)\",(data["loginId"], data["passwd"], data["name"])'
# user_read_data = 'select * from user'
# userSQL = {'db_name': 'userinfo.db', 'create_table': user_create, 'add_data': user_add_data,
#            'read_data': user_read_data}
import hashlib
pw ='050094'
print(hashlib.md5(pw.encode(encoding='utf-8')).hexdigest().upper())

# http://59.203.198.22:8086/defaultroot/public/download/download.jsp?FileName=2020022419504463978337936.xlsx&verifyCode=F35DDE0D55FileName00&name=青阳县应对新冠肺炎疫情支持中小微企业责任清单.xlsx&path=govdocumentmanager


import demjson

str = "{result: 'success', data: {pager: {pageCount: 1, recordCount: 1}, data: [{'id': '379850306', 'documentSendFileByteNumber': '青科经信〔2019〕183号','documentSendFileTitle': '关于填报2019年中国声谷首台（套）创新产品免费示范应用计划的通知', 'documentSendFileWriteOrg': '节能与综合利用科','createdTime': '2019-11-13 00:00:00', 'createdEmp': '23409802', 'createdOrg': '23409770', 'sendFileLink': '','sendFileOverSee': '0', 'sendFileUserId': '379859013', 'goldGridId': '1573612387930', 'isReaded': '1','outSeeType': '', 'orgId': '23598744', 'documentWordType': '.doc', 'tableId': '23631466', 'handOutTime': '','sendToMyRange': '', 'recivedDate': '2019-11-13 10:54:50', 'empId': '23598786', 'isSyncToInfomation': '0','sendFileDraft': '刘自渊', 'accessoryName': '附件1 关于填报2019年中国声谷首台套创新产品免费示范应用计划的通知.pdf|附件2 示范应用计划申报表.xlsx','accessorySaveName': '2019111310323347757243457.pdf|2019111310323733651319778.xlsx', 'canDownload': '1','verifyCode1': '2A0479BD10FileName00', 'verifyCode': '766B2AFF46id00'}]}}"

json = demjson.decode(str)

if json['result'] == 'success':
    json = json['data']
    record = json['pager']['recordCount']
    if record == 0:
        msg = '无未读收文'
    else:
        msg = '未读收文{}封'.format(record)
    print(msg)
    docSet_info = json['data']


    for i in range(record):
        doc_info = docSet_info[i]
        if doc_info['accessoryName'] != '':

    print(doc_info_data)

