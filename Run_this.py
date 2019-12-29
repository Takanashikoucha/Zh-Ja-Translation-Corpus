# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2019-12-29 20:23:25
import re

import requests
from lxml import etree

# 最终列表
Zh_list = []
Ja_list = []

# 地址列表
url_list = []

# 进行遍历循环（当前最大页数为10）
for page_num in range(1, 11):
    page_num = str(page_num)
    url = "http://j.people.com.cn/95961/index" + page_num + ".html"
    r = requests.get(url)
    r.encoding = "utf-8"
    page_html = r.text
    paser = etree.HTML(page_html)
    url_list.append(paser.xpath("/html/body/div[6]/div[1]/div[3]//@href"))
print("地址获取完成")


# 分句函数
def gen_split(sents):
    sents_list = re.split('(。|！|\!|？|\?)', sents)
    new_sents = []
    for i in range(int(len(sents_list) / 2)):
        sent = sents_list[2 * i] + sents_list[2 * i + 1]
        new_sents.append(sent)
    return new_sents


# 下载函数
def download(url):
    r = requests.get("http://j.people.com.cn" + url)
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
    for indey, url in enumerate(item):
        print("Num:  " + str(indey + 1))
        download(url)

# 写入文件
with open("zh.txt", "a", encoding="utf-8") as f:
    for zh in Zh_list:
        f.writelines(zh + "\n")
    print("中文写入完成")
with open("ja.txt", "a", encoding="utf-8") as f:
    for ja in Ja_list:
        f.writelines(ja + "\n")
    print("日语写入完成")
