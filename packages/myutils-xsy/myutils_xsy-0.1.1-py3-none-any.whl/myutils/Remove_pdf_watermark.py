'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2025-03-06 16:19:02
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-03-07 10:39:54
FilePath: \WorkTools\Remove_pdf_watermark.py
Description: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
#%% 
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import fitz  # PyMuPDF

def detect_watermarks(pdf_path, threshold=0.5):
    """
    使用 PyMuPDF 识别 PDF 可能的水印文本
    
    参数:
    pdf_path (str): PDF 文件路径
    threshold (float): 认为是水印的页面占比阈值（0~1）
    
    返回:
    list: 可能的水印文本列表
    """
    try:
        doc = fitz.open(pdf_path)
        all_texts = []
        page_count = len(doc)

        for page in doc:
            text = page.get_text("text")
            lines = text.split('\n')
            all_texts.extend(lines)

        doc.close()

        text_counter = Counter(all_texts)
        potential_watermarks = []
        threshold_count = threshold * page_count

        for text, count in text_counter.items():
            if count >= threshold_count and len(text.strip()) > 0:
                potential_watermarks.append(text.strip())

        return potential_watermarks
    except Exception as e:
        raise Exception(f"检测水印时出错: {str(e)}")


def remove_text_watermarks(input_file, output_file, watermark_texts):
    """
    使用 PyMuPDF 重新生成页面，移除水印文本
    
    参数:
    input_file (str): 输入 PDF 文件路径
    output_file (str): 输出 PDF 文件路径
    watermark_texts (list): 需要移除的水印文本列表
    """
    try:
        doc = fitz.open(input_file)

        for page in doc:
            for watermark_text in watermark_texts:  # 遍历每个水印文本
                text_instances = page.search_for(watermark_text)  # 查找水印文本位置
                for inst in text_instances:
                    page.add_redact_annot(inst)  # 标记需要移除的文本
            page.apply_redactions()  # 应用移除操作

        doc.save(output_file)
        doc.close()

        return output_file
    except Exception as e:
        raise Exception(f"移除水印时出错: {str(e)}")



def select_watermarks(detected_watermarks):
    """
    让用户选择要移除的水印，增加输入框控制默认勾选的水印长度
    
    参数:
    detected_watermarks (list): 检测到的可能水印列表
    
    返回:
    list: 用户选择要移除的水印列表
    """
    if not detected_watermarks:
        return []
    
    select_window = tk.Toplevel()
    select_window.title("选择要移除的水印")
    select_window.geometry("600x450")
    
    tk.Label(select_window, text="检测到以下可能的水印文本，请选择要移除的内容:", pady=10).pack()
    
    length_frame = tk.Frame(select_window)
    tk.Label(length_frame, text="默认勾选长度大于:").pack(side=tk.LEFT)
    length_var = tk.StringVar(value="20")  # 默认值为20
    length_entry = tk.Entry(length_frame, textvariable=length_var, width=5)
    length_entry.pack(side=tk.LEFT)
    length_frame.pack(pady=5)
    
    frame = tk.Frame(select_window)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
    scrollbar.config(command=canvas.yview)
    
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor='nw')
    
    var_dict = {}
    for text in detected_watermarks:
        display_text = text if len(text) < 50 else text[:47] + "..."
        var = tk.IntVar()
        var_dict[text] = var
        tk.Checkbutton(content_frame, text=display_text, variable=var, anchor='w', width=70).pack(fill='x', padx=20)
    
    def update_selection():
        """更新默认勾选的水印"""
        try:
            threshold_length = int(length_var.get())
            for text, var in var_dict.items():
                var.set(1 if len(text) > threshold_length else 0)
        except ValueError:
            messagebox.showwarning("输入错误", "请输入有效的数字！")
    
    tk.Button(length_frame, text="应用", command=update_selection).pack(side=tk.LEFT, padx=5)
    
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"), width=580, height=300)
    canvas.pack(fill=tk.BOTH)
    frame.pack(fill=tk.BOTH, expand=True)
    
    selected_watermarks = []
    
    def on_confirm():
        nonlocal selected_watermarks
        selected_watermarks = [text for text, var in var_dict.items() if var.get() == 1]
        select_window.destroy()
    
    tk.Button(select_window, text="确认", command=on_confirm, pady=5).pack(pady=20)
    select_window.wait_window()
    
    return selected_watermarks



def main():
    root = tk.Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(
        title="选择要处理的PDF文件",
        filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
    )

    if not input_file:
        messagebox.showinfo("操作取消", "未选择文件，程序退出")
        return

    try:
        messagebox.showinfo("处理中", "正在分析PDF文件，检测可能的水印...")
        potential_watermarks = detect_watermarks(input_file)

        if not potential_watermarks:
            messagebox.showinfo("结果", "未检测到可能的水印文本")
            return

        selected_watermarks = select_watermarks(potential_watermarks)

        if not selected_watermarks:
            messagebox.showinfo("操作取消", "未选择任何水印文本，程序退出")
            return

        default_output = os.path.splitext(input_file)[0] + "_无水印.pdf"
        output_file = filedialog.asksaveasfilename(
            title="保存处理后的PDF文件",
            defaultextension=".pdf",
            initialfile=os.path.basename(default_output),
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )

        if not output_file:
            messagebox.showinfo("操作取消", "未指定输出文件，程序退出")
            return

        messagebox.showinfo("处理中", "正在移除水印，请稍候...")
        result_file = remove_text_watermarks(input_file, output_file, selected_watermarks)

        messagebox.showinfo("完成", f"水印移除完成，文件已保存至:\n{result_file}")

    except Exception as e:
        messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")

    root.destroy()


if __name__ == "__main__":
    main()

# %%
