'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2025-05-12 21:53:07
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-05-12 21:57:22
FilePath: /myutils/tests/test_date_calculator.py
Description: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
# %%
from datetime import datetime
from myutils import date_calculator

def test_format_date_with_weekday():
    date = datetime(2025, 5, 12)  # Monday
    date_calculator.current_lang = 'zh'
    zh = date_calculator.format_date_with_weekday(date)
    assert zh == "2025-05-12 (星期一)"
    
    date_calculator.current_lang = 'en'
    en = date_calculator.format_date_with_weekday(date)
    assert en == "2025-05-12 (Monday)"

# %%
