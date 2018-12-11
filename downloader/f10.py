#!/usr/bin/python3
#-*- coding:utf-8 -*-

import utils
import config
from crc import CRCMgr

class F10:
    """
    F10资讯
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.url = config.F10_URL
        self.codeMap = []

    def dispatch(self, stockcode):
        """
        分发股票代码
        """
        self.codeMap.append(stockcode)

    def start(self):
        """
        开始下载F10
        """
        crcmgr = CRCMgr(self.codeMap)
        crcmgr.load()

        for stockcode in self.codeMap:
            categories = self.reqCategory(stockcode)
            for key in categories:
                #key = "新股提示"
                category = key
                crc = categories[key]
                if crcmgr.sameas(stockcode, category, crc):
                    continue

                content = self.reqContent(stockcode, category)
                if content == "":
                    continue

                #sql = "INSERT INTO tb_f10(stockcode, category, content) VALUES ({0}, '{1}', '{2}')".format(stockcode, category, content)
                sql = "REPLACE INTO tb_f10(stockcode, category, content) VALUES ({0}, '{1}', '{2}')".format(stockcode, category, content)
                self.dbpool.execute(sql)
                crcmgr.update(stockcode, category, crc)
            break
        
        crcmgr.save()

    def reqCategory(self, stockcode):
        """
        请求分类
        参  数：7位股票代码
        返回值：股票分类列表
        """
        categories = {}
        url = self.makeCategoryURL(stockcode)

        ret = utils.req(url)
        if ret != "":   
            rows = ret.split('\r\n')
            for idx in range(len(rows)):
                if rows[idx] == "":
                    continue
                cols = rows[idx].split('|')
                if len(cols) < 3:
                    continue
                key = cols[0] #分类
                val = cols[1] #CRC
                categories[key] = val
        return categories

    def reqContent(self, stockcode, category):
        """
        请求F10内容
        参  数：7位股票代码、分类名
        返回值：F10资讯内容
        """
        url = self.makeContentURL(stockcode, category)
        content = utils.req(url)
        return content

    def makeCategoryURL(self, stockcode):
        prefix = utils.formatCode(stockcode)
        path = "[PREFIX]_lst.zData"
        path = path.replace("[PREFIX]", prefix)
        return self.url + path

    def makeContentURL(self, stockcode, category):
        prefix = utils.formatCode(stockcode)
        path = "[PREFIX]_[CATEGORY].zData"
        path = path.replace("[PREFIX]", prefix)
        path = path.replace("[CATEGORY]", category)
        return self.url + path

def CreateObjPool(dbpool, max_size):
    return [F10(dbpool) for i in range(max_size)]