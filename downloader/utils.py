#!/usr/bin/python3
#-*- coding:utf-8 -*-

'''
依赖库：
    requests
'''

import requests
import time
import os
from io import BytesIO

MAX_RETRIES = 3

def req(url, maxretries=MAX_RETRIES):
    """
    请求
    参  数：url地址，maxretries最大重试次数
    返回值：请求的内容，或者空
    备  注：请求失败，最大重试次数内会每隔0.3秒尝试重试一次
    """
    retries = 0
    ret = None

    while retries < maxretries:
        ret = request(url)
        if ret == None:
            retries = retries + 1
            time.sleep(0.3)
            continue
        else:
            break

    if ret == None:
        ret = ""
    return ret

def request(url):
    with requests.get(url) as r:
        if r.status_code != 200:
            return None

        if r.headers['Content-Encoding']=='gzip':
            return BytesIO(r.content).read().decode()
        else:
            return r.text

def formatCode(stockcode):
    """
    格式化股票代码
    参  数：7位股票代码
    返回值：0开头的返回szXXXXXX，1开头的返回shXXXXXX，否则返回原来的7位
    """
    MARKET_SZ = '0'
    MARKET_SH = '1'

    ret = ""
    if stockcode.startswith(MARKET_SZ):
        ret = stockcode.replace(MARKET_SZ, 'sz', 1)
    elif stockcode.startswith(MARKET_SH):
        ret = stockcode.replace(MARKET_SH, 'sh', 1)
    else:
        ret = stockcode
    return ret

def getCRCPath():
    curpath = os.getcwd() + "/crc/"
    return curpath