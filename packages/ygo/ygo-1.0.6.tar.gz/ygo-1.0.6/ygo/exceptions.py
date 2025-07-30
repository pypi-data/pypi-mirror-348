# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2024/12/18 下午7:01
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

class WarnException(Exception):
    """自定义异常类，仅用于警告"""
    def __init__(self, message):
        super().__init__(message)  # 调用父类的构造函数