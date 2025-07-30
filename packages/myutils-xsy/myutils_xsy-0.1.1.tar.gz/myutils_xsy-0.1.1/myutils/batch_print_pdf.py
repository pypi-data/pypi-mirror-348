import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import win32print

# ========== UI 输入 ==========
def ask_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="选择PDF所在的文件夹")

def ask_duplex():
    root = tk.Tk()
    root.withdraw()
    return messagebox.askyesno("打印设置", "是否使用双面打印？")

# ========== 设置双面打印 ==========
def set_duplex_mode(printer_name, duplex):
    try:
        # 获取打印机句柄
        printer_handle = win32print.OpenPrinter(printer_name)
        # 正确调用 GetPrinter，需要传入句柄，不是字符串
        printer_info = win32print.GetPrinter(printer_handle, 2)
        devmode = printer_info["pDevMode"]
        devmode.Duplex = 2 if duplex else 1  # 2=双面, 1=单面
        win32print.SetPrinter(printer_handle, 2, {"pDevMode": devmode}, 0)
        win32print.ClosePrinter(printer_handle)
    except Exception as e:
        print("设置双面打印失败，可能打印机不支持：", e)

# ========== SumatraPDF 打印 ==========
def print_with_sumatra(pdf_path, printer_name, sumatra_path):
    try:
        subprocess.run([
            sumatra_path,
            "-print-to", printer_name,
            "-silent",
            pdf_path
        ], check=True)
    except Exception as e:
        print(f"打印失败: {os.path.basename(pdf_path)}，错误：{e}")

# ========== 主函数 ==========
def batch_print():
    folder = ask_folder()
    if not folder:
        print("未选择文件夹，退出。")
        return

    duplex = ask_duplex()
    printer_name = win32print.GetDefaultPrinter()
    print(f"使用打印机：{printer_name}")
    set_duplex_mode(printer_name, duplex)

    # === 替换为你的 SumatraPDF 路径（请确认）===
    sumatra_path = r"C:\Users\xushe\AppData\Local\SumatraPDF\SumatraPDF.exe"
    if not os.path.exists(sumatra_path):
        print("未找到 SumatraPDF，请检查路径。")
        return

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("该文件夹下没有PDF文件。")
        return

    for pdf in pdf_files:
        full_path = os.path.abspath(os.path.join(folder, pdf))
        print(f"正在打印: {full_path}")
        print_with_sumatra(full_path, printer_name, sumatra_path)

# ========== 运行 ==========
if __name__ == "__main__":
    batch_print()
