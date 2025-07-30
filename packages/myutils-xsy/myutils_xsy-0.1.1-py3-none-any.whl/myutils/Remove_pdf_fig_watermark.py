'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2025-03-07 10:01:51
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-05-12 23:05:23
FilePath: /myutils/myutils/Remove_pdf_fig_watermark.py
Description: 

Copyright (c) 2025 by ${git_name_email}, All Rights Reserved. 
'''
# #%%

# %%
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def extract_all_images_from_page(page, page_num):
    """
    提取页面中的所有图片，返回列表，每项为 (xref, 临时文件路径, width, height)
    """
    images = page.get_images(full=True)
    images_info = []
    for image in images:
        xref, _, width, height, *_ = image
        # 提取图片数据
        img_data = page.parent.extract_image(xref)
        temp_img_path = f"temp_page_{page_num}_img_{xref}.png"
        with open(temp_img_path, "wb") as f:
            f.write(img_data["image"])
        images_info.append((xref, temp_img_path, width, height))
    return images_info

def show_images_confirmation(page_num, images_info):
    """
    弹出窗口，显示该页所有图片的缩略图，并提供复选框供用户勾选要删除的图片，
    使用滚动条以便查看所有图片，返回需要删除图片的 xref 列表
    """
    window = tk.Toplevel()
    window.title(f"第 {page_num + 1} 页 - 选择要删除的图片")
    window.geometry("400x600")  # 设置一个合适的窗口大小

    # 创建容器 Frame，用于放置 Canvas 和滚动条
    container = tk.Frame(window)
    container.pack(fill="both", expand=True)

    # 创建 Canvas 和滚动条
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # 在 Canvas 中创建一个 Frame，用作滚动区域
    scrollable_frame = tk.Frame(canvas)
    # 当 scrollable_frame 尺寸变化时，更新 Canvas 的滚动区域
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    check_vars = []  # 每项为 (BooleanVar, xref)

    for idx, (xref, temp_img_path, width, height) in enumerate(images_info):
        frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove", padx=5, pady=5)
        frame.pack(padx=5, pady=5, fill="x", expand=True)

        # 加载并生成缩略图
        try:
            img = Image.open(temp_img_path)
        except Exception as e:
            continue
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(frame, text=f"图片 {idx + 1}：{width}x{height}")
        label.pack()
        img_label = tk.Label(frame, image=img_tk)
        img_label.image = img_tk  # 保存引用
        img_label.pack()

        var = tk.BooleanVar(value=False)
        check = tk.Checkbutton(frame, text="删除", variable=var)
        check.pack()
        check_vars.append((var, xref))

    # 按钮区域，放在窗口底部，不在滚动区域中
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    selected_xrefs = []

    def on_confirm():
        nonlocal selected_xrefs
        selected_xrefs = [xref for var, xref in check_vars if var.get()]
        window.destroy()

    def on_cancel():
        window.destroy()

    tk.Button(btn_frame, text="确认删除选中的图片", command=on_confirm, fg="red").pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=10)

    window.wait_window()  # 等待窗口关闭
    return selected_xrefs

def confirm_and_remove_images(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    modified = False  # 记录是否有修改

    for page_num in range(len(doc)):
        page = doc[page_num]
        images_info = extract_all_images_from_page(page, page_num)

        if images_info:
            # 弹出窗口供用户选择要删除的图片
            selected_xrefs = show_images_confirmation(page_num, images_info)
            # 对选中的图片进行删除
            for xref in selected_xrefs:
                page.delete_image(xref)
                modified = True
            # 删除所有临时保存的图片文件
            for _, temp_img_path, _, _ in images_info:
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

    if modified:
        doc.save(output_pdf)
        messagebox.showinfo("完成", f"处理完成，已保存至:\n{output_pdf}")
    else:
        messagebox.showinfo("无修改", "没有删除任何图片。")

    doc.close()

def main():
    # 创建 Tkinter 主窗口并隐藏
    root = tk.Tk()
    root.withdraw()

    # 选择输入 PDF 文件
    input_file = filedialog.askopenfilename(
        title="选择要处理的 PDF 文件",
        filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")]
    )

    if input_file:
        # 选择输出 PDF 文件路径
        output_file = filedialog.asksaveasfilename(
            title="选择保存处理后的 PDF",
            defaultextension=".pdf",
            filetypes=[("PDF 文件", "*.pdf")]
        )
        if output_file:
            try:
                confirm_and_remove_images(input_file, output_file)
            except Exception as e:
                messagebox.showerror("错误", f"处理 PDF 时出错:\n{e}")
    else:
        messagebox.showwarning("警告", "未选择文件，程序已取消")

if __name__ == "__main__":
    main()
# %%
