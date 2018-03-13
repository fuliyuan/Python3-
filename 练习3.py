#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time

超时 = 5
socket.setdefaulttimeout(超时)


class 爬图类:
    # 睡眠时长
    __睡眠时长 = 0.1
    __用时 = 0
    __起始用时 = 0
    __计数器 = 0
    标题 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # 间隔 下载图片时间间隔
    def __init__(self, 间隔=0.1):
        self.睡眠时长 = 间隔

    # 获取后缀名
    def 获取后缀名(self, 后缀名):
        我的 = re.search(r'\.[^\.]*$', 后缀名)
        if 我的.group(0) and len(我的.group(0)) <= 5:
            return 我的.group(0)
        else:
            return '.jpeg'

    # 获取引用，用于生成引用
    def 获取引用(self, 网址):
        解析 = urllib.parse.urlparse(网址)
        if 解析.scheme:
            return 解析.scheme + '://' + 解析.netloc
        else:
            return 解析.netloc

        # 保存图片
    def 保存图片(self, 读取数据, 字段):
        if not os.path.exists("./" + 字段):
            os.mkdir("./" + 字段)
        # 判断名字是否重复，获取图片长度
        self.__计数器 = len(os.listdir('./' + 字段)) + 1
        for 图片信息 in 读取数据['imgs']:

            try:
                time.sleep(self.睡眠时长)
                后缀 = self.获取后缀名(图片信息['objURL'])
                # 指定UA和引用，减少403
                引用 = self.获取引用(图片信息['objURL'])
                开启工具 = urllib.request.build_opener()
                开启工具.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', 引用)
                ]
                urllib.request.install_opener(开启工具)
                # 保存图片
                urllib.request.urlretrieve(图片信息['objURL'], './' + 字段 + '/' + str(self.__计数器) + str(后缀))
            except urllib.error.HTTPError as 网址出错:
                print(网址出错)
                continue
            except Exception as 出错:
                time.sleep(1)
                print(出错)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("小黄图+1,已有" + str(self.__计数器) + "张小黄图")
                self.__计数器 += 1
        return

    # 开始获取
    def 获取图片(self, 字段='宇宙'):
        搜索 = urllib.parse.quote(字段)
        # 开始 int 图片数
        开始 = self.__起始用时
        while 开始 < self.__用时:

            网址 = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + 搜索 + '&cg=girl&pn=' + str(
                开始) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.睡眠时长)
                请求 = urllib.request.Request(url=网址, headers=self.标题)
                页码 = urllib.request.urlopen(请求)
                读取 = 页码.read().decode('unicode_escape')
            except UnicodeDecodeError as 解码错误:
                print(解码错误)
                print('-----解码错误:', url)
            except urllib.error.URLError as 解码错误:
                print(解码错误)
                print("-----网址出错:", url)
            except socket.超时 as 解码错误:
                print(解码错误)
                print("-----套接字超时:", url)
            else:
                # 解析json
                读取数据 = json.loads(读取)
                self.保存图片(读取数据, 字段)
                # 读取下一页
                print("下载下一页")
                开始 += 10
            finally:
                页码.close()
        print("下载任务结束")
        return

    def 起始(self, 字段, 爬取页码=1, 起始页码=1):
        """
        爬虫入口
        :param 字段: 抓取的关键词
        :param 爬取页码: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param 起始页码:起始页数
        :return:
        """
        self.__起始用时 = (起始页码 - 1) * 60
        self.__用时 = 爬取页码 * 60 + self.__起始用时
        self.获取图片(字段)


if __name__ == '__main__':
    爬图 = 爬图类(0.05)  # 抓取延迟为 0.05

    # 爬图.起始('宇宙', 10, 2)  # 抓取关键词为 “美女”，总数为 1 页（即总共 1*60=60 张），起始页码为 2
    爬图.起始('宇宙', 1, 1)  # 抓取关键词为 “二次元 美女”，总数为 1 页（即总共 10*60=600 张），起始抓取的页码为 1
    # 爬图.起始('宇宙', 5)  # 抓取关键词为 “帅哥”，总数为 5 页（即总共 5*60=300 张）