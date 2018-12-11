#!/usr/bin/python3
#-*- coding:utf-8 -*-

"""
最大工作线程数
"""
MAX_WORKERS = 1

"""
数据库连接配置
"""
db_setting = {
    "host":"192.168.8.18", 
    "port":3306,
    "user":"root", 
    "password":"emoney",
    "dbname":"f10",
    "maxpoolsize":10
}

"""
F10数据请求地址
"""
F10_URL = 'https://stwebapp001sh.blob.core.chinacloudapi.cn/gaf10/'