#!/usr/bin/python3
#-*- coding:utf-8 -*-

import json

class CodeMap:
    """
    码表
    """
    def req(self):
        """
        请求码表
        """
        with open("codemap.json", encoding='utf-8') as f:
            d = json.load(f)
        keys = []
        for key in d.keys():
            if key.startswith('0') or key.startswith('1'):
                keys.append(key)
        return keys