# -*- coding:utf-8 _*-  
""" 
@author: ronething 
@time: 2019-04-09 02:09
@mail: axingfly@gmail.com

Less is more.
"""

def get_value(data, keyname):
    # 定义获取 value 函数
    return data.get(keyname, '没有相关信息')
