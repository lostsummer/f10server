#!/usr/bin/python3
#-*- coding:utf-8 -*-

import json
import utils
import os

class CRC:
    """
    单个股票所有分类的CRC
    存储格式为json:{"分类0":"CRC",...,"分类N":"CRC"}
    """
    def __init__(self, code):
        self.code = code
        self.crcs = {}
    
    def load(self):
        path = self.getjsonPath()
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                d = json.load(f)
            for key in d.keys():
                self.crcs[key] = d[key]

    def save(self): 
        d = json.dumps(self.crcs)
        path = self.getjsonPath()
        with open(path, "w") as f:
            f.write(d)
        
    def get(self, category):
        if category in self.crcs.keys():
            return self.crcs[category]
        else:
            return None

    def update(self, category, newcrc):
        self.crcs[category] = newcrc

    def getjsonPath(self):
        return utils.getCRCPath() + self.code + ".json"


class CRCMgr:
    """
    CRC管理类
    存储为dict
    key是股票代码
    val为CRC对象
    """
    def __init__(self, codes):
        self.codes = codes
        self.crcs = {}
        self.needsave = False

    def load(self):
        for code in self.codes:
            crc = CRC(code)
            crc.load()
            self.crcs[code] = crc

    def save(self):
        if self.needsave:
            for key in self.crcs.keys():
                self.crcs[key].save()
            self.needsave = False

    def get(self, code, category):
        return self.crcs[code].get(category)

    def update(self, code, category, newcrc):
        self.crcs[code].update(category, newcrc)
        self.needsave = True

    def sameas(self, code, category, newcrc):
        oldcrc = self.get(code, category)
        return oldcrc==newcrc

    