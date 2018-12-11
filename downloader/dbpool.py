#!/usr/bin/python3
#-*- coding:utf-8 -*-

"""
依赖库：
    pymysqlpool
    
源代码：
    https://github.com/luvvien/pymysqlpool

安装方式： 
    python setup.py install
"""
from pymysqlpool import ConnectionPool

class MySQLPool:
    def __init__(self, host, port, user, password, dbname, maxpoolsize=20):
        self.config = {
            'pool_name': 'test',
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': dbname,
            'max_pool_size':maxpoolsize
        }

    def ConnectionPool(self):
        pool = ConnectionPool(**self.config)
        pool.connect()
        return pool

    def execute(self, sql):
        with self.ConnectionPool().connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()