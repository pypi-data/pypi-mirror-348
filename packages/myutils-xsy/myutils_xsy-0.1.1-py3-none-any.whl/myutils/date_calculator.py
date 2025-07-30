'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2025-05-12 14:15:48
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-05-12 19:34:36
FilePath: /myutils/myutils/date_calculator.py
Description: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''



# %%
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from zhdate import ZhDate
import chinese_calendar as cc

# 星期映射
WEEKDAYS = {
    'zh': ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'],
    'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
}

# 多语言文本
LANG_TEXTS = {
    'zh': {
        'title': "🗓️ 日期计算器",
        'section1': "📅 日期间隔计算",
        'section2': "📆 日期推算",
        'start_date': "起始日期:",
        'end_date': "结束日期:",
        'base_date': "基准日期:",
        'offset_days': "偏移天数（可负）:",
        'btn_diff': "🧮 计算天数差",
        'btn_offset': "📅 推算日期",
        'diff_result': "两个日期相差：{days} 天",
        'offset_result': "推算结果：{date}",
        'week_info': "📌 {year}年第 {week} 周",
        'lunar_info': "🌙 农历：{lunar}",
        'holiday_info': "🎉 节日：{holiday}",
        'no_holiday': "🎉 节日：无",
        'error_date': "请确保日期格式正确，例如：2025-05-12",
        'error_int': "请输入整数天数（可为负数）",
        'lang_switch': "Switch to English"
    },
    'en': {
        'title': "🗓️ Date Calculator",
        'section1': "📅 Date Difference",
        'section2': "📆 Date Offset",
        'start_date': "Start Date:",
        'end_date': "End Date:",
        'base_date': "Base Date:",
        'offset_days': "Offset Days (±):",
        'btn_diff': "🧮 Calculate Difference",
        'btn_offset': "📅 Calculate Offset",
        'diff_result': "Days Between: {days} days",
        'offset_result': "Offset Result: {date}",
        'week_info': "📌 Week {week} of {year}",
        'lunar_info': "🌙 Lunar: {lunar}",
        'holiday_info': "🎉 Holiday: {holiday}",
        'no_holiday': "🎉 Holiday: None",
        'error_date': "Please enter a valid date (e.g., 2025-05-12)",
        'error_int': "Please enter a valid integer",
        'lang_switch': "切换为中文"
    }
}

current_lang = 'zh'

def get_text(key):
    return LANG_TEXTS[current_lang][key]

def get_date(entry_widget):
    value = entry_widget.get()
    return datetime.strptime(value, '%Y-%m-%d')

def format_date_with_weekday(date_obj):
    weekday_str = WEEKDAYS[current_lang][date_obj.weekday()]
    return f"{date_obj.strftime('%Y-%m-%d')} ({weekday_str})"

def calculate_difference():
    try:
        date1 = get_date(date1_entry)
        date2 = get_date(date2_entry)
        diff = abs((date2 - date1).days)
        result_text.set(get_text('diff_result').format(days=diff))
    except Exception:
        messagebox.showerror("Error", get_text('error_date'))

def calculate_offset():
    try:
        base_date = get_date(base_date_entry)
        days = int(entry_days.get())
        new_date = base_date + timedelta(days=days)
        formatted = format_date_with_weekday(new_date)
        week_num = new_date.isocalendar()[1]
        lunar = ZhDate.from_datetime(new_date).chinese()
        # 安全调用节假日查询
        try:
            on_holiday, holiday_name = cc.get_holiday_detail(new_date.date())
            holiday_display = get_text('holiday_info').format(holiday=holiday_name) if on_holiday else get_text('no_holiday')
        except Exception:
            holiday_display = get_text('no_holiday')  # 超出范围默认无节假日

        result_text2.set(get_text('offset_result').format(date=formatted))
        result_text_week.set(get_text('week_info').format(year=new_date.year, week=week_num))
        result_text_lunar.set(get_text('lunar_info').format(lunar=lunar))
        result_text_holiday.set(holiday_display)
    except ValueError:
        messagebox.showerror("Error", get_text('error_int'))
    except Exception:
        messagebox.showerror("Error", get_text('error_date'))

def switch_language():
    global current_lang
    current_lang = 'en' if current_lang == 'zh' else 'zh'
    update_ui_language()

def update_ui_language():
    root.title(get_text('title'))
    label_sec1.config(text=get_text('section1'))
    label_sec2.config(text=get_text('section2'))
    label_start.config(text=get_text('start_date'))
    label_end.config(text=get_text('end_date'))
    label_base.config(text=get_text('base_date'))
    label_days.config(text=get_text('offset_days'))
    btn_diff.config(text=get_text('btn_diff'))
    btn_offset.config(text=get_text('btn_offset'))
    lang_btn.config(text=get_text('lang_switch'))

def main():
    global root
    global date1_entry, date2_entry, base_date_entry, entry_days
    global result_text, result_text2, result_text_week, result_text_lunar, result_text_holiday
    global label_sec1, label_sec2, label_start, label_end, label_base, label_days
    global btn_diff, btn_offset, lang_btn
    # 主窗口设置
    root = tk.Tk()
    root.title(get_text('title'))
    root.geometry("600x400")
    root.resizable(True, True)

    style = ttk.Style()
    style.theme_use('clam') 

    for i in range(12):
        root.rowconfigure(i, weight=1)
    for j in range(2):
        root.columnconfigure(j, weight=1)

    today = datetime.today().strftime('%Y-%m-%d')

    # === 日期差部分 ===
    label_sec1 = ttk.Label(root, text=get_text('section1'), font=('Arial', 11, 'bold'))
    label_sec1.grid(row=0, column=0, columnspan=2, pady=(10, 4))

    label_start = ttk.Label(root, text=get_text('start_date'))
    label_start.grid(row=1, column=0, sticky='e', padx=10)
    date1_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    date1_entry.set_date(today)
    date1_entry.grid(row=1, column=1, sticky='we', padx=10)

    label_end = ttk.Label(root, text=get_text('end_date'))
    label_end.grid(row=2, column=0, sticky='e', padx=10)
    date2_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    date2_entry.set_date(today)
    date2_entry.grid(row=2, column=1, sticky='we', padx=10)

    btn_diff = ttk.Button(root, text=get_text('btn_diff'), command=calculate_difference)
    btn_diff.grid(row=3, column=0, columnspan=2, pady=5)

    result_text = tk.StringVar()
    entry_result = ttk.Entry(root, textvariable=result_text, state="readonly", foreground="blue", font=('Arial', 10))
    entry_result.grid(row=4, column=0, columnspan=2, sticky='we', padx=10)

    # === 日期推算部分 ===
    label_sec2 = ttk.Label(root, text=get_text('section2'), font=('Arial', 11, 'bold'))
    label_sec2.grid(row=5, column=0, columnspan=2, pady=(15, 4))

    label_base = ttk.Label(root, text=get_text('base_date'))
    label_base.grid(row=6, column=0, sticky='e', padx=10)
    base_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    base_date_entry.set_date(today)
    base_date_entry.grid(row=6, column=1, sticky='we', padx=10)

    label_days = ttk.Label(root, text=get_text('offset_days'))
    label_days.grid(row=7, column=0, sticky='e', padx=10)
    entry_days = ttk.Entry(root)
    entry_days.insert(0, "0")
    entry_days.grid(row=7, column=1, sticky='we', padx=10)

    btn_offset = ttk.Button(root, text=get_text('btn_offset'), command=calculate_offset)
    btn_offset.grid(row=8, column=0, columnspan=2, pady=5)

    result_text2 = tk.StringVar()
    entry_result2 = ttk.Entry(root, textvariable=result_text2, state="readonly", foreground="green", font=('Arial', 10))
    entry_result2.grid(row=9, column=0, columnspan=2, sticky='we', padx=10)

    result_text_week = tk.StringVar()
    entry_result_week = ttk.Entry(root, textvariable=result_text_week, state="readonly", foreground="gray", font=('Arial', 10))
    entry_result_week.grid(row=10, column=0, columnspan=2, sticky='we', padx=10)

    result_text_lunar = tk.StringVar()
    entry_result_lunar = ttk.Entry(root, textvariable=result_text_lunar, state="readonly", foreground="purple", font=('Arial', 10))
    entry_result_lunar.grid(row=11, column=0, columnspan=2, sticky='we', padx=10)

    result_text_holiday = tk.StringVar()
    entry_result_holiday = ttk.Entry(root, textvariable=result_text_holiday, state="readonly", foreground="orange", font=('Arial', 10))
    entry_result_holiday.grid(row=12, column=0, columnspan=2, sticky='we', padx=10)

    # === 多语言切换按钮 ===
    lang_btn = ttk.Button(root, text=get_text('lang_switch'), command=switch_language)
    lang_btn.grid(row=13, column=0, columnspan=2, pady=(10, 10))
    root.mainloop()
    
if __name__ == "__main__":
    main()
# %%