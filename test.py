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