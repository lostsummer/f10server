#!/usr/bin/python3
#-*- coding:utf-8 -*-
"""
功  能：F10资讯数据落库
依赖库：
    1）requests
        a、pip install requests

    2）pymysqlpool
        a、源代码：
            https://github.com/luvvien/pymysqlpool

        b、安装方式： 
            python setup.py install
"""

from codemap import CodeMap
from dbpool import MySQLPool
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import config
import f10
import os
import utils

def initenv():
    path = utils.getCRCPath()
    existed = os.path.exists(path)
    if not existed:
        os.mkdir(path)

def main():
    #初始化环境
    initenv()

    dbconf = config.db_setting
    max_workers = config.MAX_WORKERS
    dbpool = MySQLPool(host=dbconf["host"], port=dbconf["port"], user=dbconf["user"], password=dbconf["password"], dbname=dbconf["dbname"]) 
    f10pool = f10.CreateObjPool(dbpool, max_workers)

    #请求码表，并均分股票代码给"下载对象"
    codeMap = CodeMap().req()
    #codeMap = ["1000001"]
    for i in range (len(codeMap)):
        code = codeMap[i]
        f10pool[i%max_workers].dispatch(code)

    #将"下载对象"放到线程池执行，并等待任务执行完成
    alltasks = []
    threadpool = ThreadPoolExecutor(max_workers=max_workers)
    for i in range(max_workers):
        task = threadpool.submit(f10pool[i].start())
        alltasks.append(task)
    wait(alltasks, return_when='ALL_COMPLETED')

if __name__ == '__main__':
    main()
    