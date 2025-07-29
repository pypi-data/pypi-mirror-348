# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2025/5/16 10:47
@author: ZhangYundi
@email: yundi.xxii@outlook.com
---------------------------------------------
"""

from dataclasses import dataclass

@dataclass
class ParseError(Exception):
    message: str

    def __str__(self):
        return f"ParseError(message={self.message})"

@dataclass
class CalculateError(Exception):
    message: str

    def __str__(self):
        return f"CalculateError(message={self.message})"

@dataclass
class PolarsError(Exception):
    message: str

    def __str__(self):
        return f"PolarsError(message={self.message})"