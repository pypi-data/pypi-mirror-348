'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2025-05-12 19:29:10
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-05-12 21:49:35
FilePath: /myutils/myutils/__init__.py
Description: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
# myutils/__init__.py

"""
myutils - A utility toolkit including a date calculator GUI.

Author: Shengyi Xu
"""

from . import date_calculator

__version__ = "0.1.0"
__all__ = ["date_calculator"]

def run():
    """Start the date calculator GUI."""
    date_calculator.main()
