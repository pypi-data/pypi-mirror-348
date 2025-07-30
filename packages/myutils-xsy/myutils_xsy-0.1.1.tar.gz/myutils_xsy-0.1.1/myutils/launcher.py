'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2025-05-12 23:14:11
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-05-12 23:29:40
FilePath: /myutils/myutils/launcher.py
Description: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
# myutils/launcher.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys
import json
import os
import shutil

def load_tools():
    import importlib.resources
    try:
        with importlib.resources.files("myutils").joinpath("tools.json").open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        config_path = os.path.join(os.path.dirname(__file__), "tools.json")
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

TOOLS = load_tools()

def run_tool(command):
    try:
        if shutil.which(command):
            subprocess.Popen([command])
        else:
            subprocess.Popen([sys.executable, "-m", f"myutils.{command}"])
    except Exception as e:
        messagebox.showerror("错误", f"无法启动 {command}：\n{e}")

def main():
    root = tk.Tk()
    root.title("MyUtils 工具箱")
    root.geometry("480x600")
    root.minsize(400, 400)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Tool.TButton", font=("Microsoft YaHei", 11), padding=10)
    style.map("Tool.TButton",
              background=[("active", "#e6f2ff")],
              relief=[("pressed", "sunken")])

    # 顶部标题
    title_label = ttk.Label(root, text="请选择要执行的工具：", font=("Microsoft YaHei", 16))
    title_label.pack(pady=10)

    # 滚动区域容器
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 动态生成按钮（两列布局）
    cols = 2
    for i, (name, cmd) in enumerate(TOOLS.items()):
        btn = ttk.Button(scrollable_frame, text=name, style="Tool.TButton",
                         command=lambda c=cmd: run_tool(c))
        btn.grid(row=i // cols, column=i % cols, padx=10, pady=10, sticky="ew")

    for c in range(cols):
        scrollable_frame.columnconfigure(c, weight=1)

    # 底部退出按钮
    exit_btn = ttk.Button(root, text="退出工具箱", style="Tool.TButton", command=root.quit)
    exit_btn.pack(pady=10, padx=20, fill="x")

    root.mainloop()
