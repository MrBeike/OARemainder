#!usr/bin/python
# -*-coding:utf-8-*-

# pip install python-docx
# import docx
# path = "append/***.docx"
# file = docx.Document(path)
# for p in file.paragraphs:
#     print(p.text)


# 查看了网上的各种方法，大部分还是接受将doc文件强制另存为docx文件（使用代码转换，而不是直接修改后缀），在读取即可，需要另外安装win32com模块，注意就是直接使用 pip install win32com 安装不成功，需要用
# python -m pip install pypiwin32

import docx
import win32com.client as wc

# doc文件另存为docx
word = wc.Dispatch("Word.Application")
wps = wc.Dispatch('wps application') #kwps
doc = word.Documents.Open(r"G:\\OARemainder\\通知文件下载\\关于做好2019年度综合绩效考核相关工作的通知关于做好2019年度综合绩效考核相关工作的通知.doc")
# 上面的地方只能使用完整绝对地址，相对地址找不到文件，且，只能用“\\”，不能用“/”，哪怕加了 r 也不行，涉及到将反斜杠看成转义字符。
doc.SaveAs(r"G:\\OARemainder\\通知文件下载\\关于做好2019年度综合绩效考核相关工作的通知关于做好2019年度综合绩效考核相关工作的通知.docx", 12, False, "", True, "",
           False, False, False,
           False)  # 转换后的文件,12代表转换后为docx文件
# doc.SaveAs(r"F:\\***\\***\\appendDoc\\***.docx", 12)#或直接简写
# 注意SaveAs会打开保存后的文件，有时可能看不到，但后台一定是打开的
doc.Close
word.Quit

path = "appendDoc/***.docx"
file = docx.Document(path)
for p in file.paragraphs:
    print(p.text)

# 没有具体实现了解，只当看了下，需要安装库 pdfminer 使用
