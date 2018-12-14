# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:daly

import hashlib

def md5(text):                    #传一个文本，转化为密文
    m = hashlib.md5()             #实例化对象
    m.update(text.encode('utf-8'))#字符串变字节
    return m.hexdigest()

if __name__ =='__main__':
    text = "daly"
    v = md5(text)
    print(v)