# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2020-03-08 04:54:00
import re
import time

import requests
from lxml import etree

starttime = time.time()

# 最终列表
Zh_list = []
Ja_list = []

# 地址列表
url_list = []

# 进行遍历循环（最大页数为10,每页20条）
s_get = requests.Session()
for page_num in range(1, 11):
    page_num = str(page_num)
    pageurl = "http://j.people.com.cn/95961/index" + page_num + ".html"
    r = s_get.get(pageurl)
    r.encoding = "utf-8"
    page_html = r.text
    paser = etree.HTML(page_html)
    for i in range(20):
        url_list.append(
            paser.xpath("/html/body/div[5]/div[1]/div[3]/div[" + str(i + 1) +
                        "]/h3/a/@href"))
        print("已添加路径数：" + str(len(url_list)))
    time.sleep(0.1)
    print("翻页等待0.1s")
print("地址获取完成")


# 分句函数
def gen_split(sents):
    sents_list = re.split(r"(。|！|\!|？|\?)", sents)
    new_sents = []
    for i in range(int(len(sents_list) / 2)):
        sent = sents_list[2 * i] + sents_list[2 * i + 1]
        new_sents.append(sent)
    return new_sents


s_download = requests.Session()


# 下载函数
def download(url):
    r = s_download.get("http://j.people.com.cn" + url[0])
    r.encoding = "utf-8"
    page_html = r.text
    paser = etree.HTML(page_html)
    result = paser.xpath("/html/body/div[5]/div[2]//p/text()")
    for i in result[::2]:
        new_i = i.replace("\n", "").replace("\t", "")
        for y in gen_split(new_i):
            Zh_list.append(y)
    for i in result[1::2]:
        new_i = i.replace("\n", "").replace("\t", "")
        for y in gen_split(new_i):
            Ja_list.append(y)


# 获取正文并分句存储
url_head = "http://j.people.com.cn"
for index, item in enumerate(url_list):
    print("Page:  " + str(index + 1))
    download(item)

# 写入文件
with open("zh.txt", "a", encoding="utf-8") as f:
    for zh in Zh_list:
        f.writelines(zh + "\n")
    print("中文写入完成")
with open("ja.txt", "a", encoding="utf-8") as f:
    for ja in Ja_list:
        f.writelines(ja + "\n")
    print("日语写入完成")


endtime = time.time()
print("程序执行时间: ", endtime - starttime)
