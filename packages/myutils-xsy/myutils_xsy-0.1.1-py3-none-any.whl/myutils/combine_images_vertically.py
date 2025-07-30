'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2024-11-02 19:21:38
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2024-11-02 19:21:57
FilePath: \Tools\combine_images_vertically.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
# %%
import os
from tkinter import Tk, filedialog
from PIL import Image

def combine_images_vertically(images):
    """将多张图像垂直拼接成一张图像"""
    # 计算拼接后图像的总高度和最大宽度
    total_height = sum(image.height for image in images)
    max_width = max(image.width for image in images)

    # 创建新图像
    new_image = Image.new('RGB', (max_width, total_height))

    # 将每张图像粘贴到新图像中
    current_height = 0
    for image in images:
        new_image.paste(image, (0, current_height))
        current_height += image.height

    return new_image

def main():
    # 创建 Tkinter 根窗口
    Tk().withdraw()  # 隐藏主窗口

    # 弹出文件夹选择对话框
    folder_path = filedialog.askdirectory(title='选择图片文件夹')
    if not folder_path:
        print("未选择文件夹。")
        return

    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
    images = [Image.open(os.path.join(folder_path, f)) for f in image_files]

    if not images:
        print("文件夹中没有可用的图片。")
        return

    # 拼接图像
    combined_image = combine_images_vertically(images)

    # 保存拼接后的图像
    combined_image.save(os.path.join(folder_path, 'combined_image.jpg'))
    print("拼接完成，保存为 combined_image.jpg")

if __name__ == '__main__':
    main()

# %%
