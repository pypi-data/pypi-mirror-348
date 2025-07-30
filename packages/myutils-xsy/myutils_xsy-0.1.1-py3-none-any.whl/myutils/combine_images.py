'''
Author: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
Date: 2024-11-02 19:21:38
LastEditors: Shengyi Xu 54436848+xushengyichn@users.noreply.github.com
LastEditTime: 2025-02-10 14:19:07
FilePath: \WorkTools\combine_images.py
Description: 添加GUI选项，如设置行数或列数、添加边框等

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
# %%
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from tkinter import Canvas
import math

class ImageCombinerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("图片拼接工具")
        self.root.geometry("1200x700")
        self.folder_path = ""
        self.images = []
        self.image_files = []
        self.selected_images = []
        self.selected_indices = []
        self.thumbnails = []
        self.preview_size = (100, 100)
        self.preview_image = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主分割窗口 - 三个面板
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧参数设置面板
        self.params_frame = ttk.Frame(self.main_paned, width=200)
        self.create_params_panel()
        self.main_paned.add(self.params_frame)
        
        # 创建中间和右侧的分割窗口
        self.right_paned = ttk.PanedWindow(self.main_paned, orient=tk.HORIZONTAL)
        self.main_paned.add(self.right_paned)
        
        # 中间图片选择面板
        self.selection_frame = ttk.Frame(self.right_paned)
        self.create_selection_panel()
        self.right_paned.add(self.selection_frame)
        
        # 右侧预览面板
        self.preview_frame = ttk.Frame(self.right_paned)
        self.create_preview_panel()
        self.right_paned.add(self.preview_frame)
        
        # 状态栏
        self.status_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.status_var).pack(pady=5)

    def create_params_panel(self):
        """创建左侧参数设置面板"""
        # 文件夹选择
        folder_frame = ttk.LabelFrame(self.params_frame, text="文件夹选择", padding="5")
        folder_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(folder_frame, text="选择文件夹", command=self.browse_folder).pack(fill=tk.X)
        
        # 布局设置
        layout_frame = ttk.LabelFrame(self.params_frame, text="布局设置", padding="5")
        layout_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.layout_var = tk.StringVar(value="rows")
        ttk.Radiobutton(layout_frame, text="固定行数", variable=self.layout_var, 
                       value="rows").pack()
        ttk.Radiobutton(layout_frame, text="固定列数", variable=self.layout_var, 
                       value="cols").pack()
        
        ttk.Label(layout_frame, text="数值:").pack()
        self.value_var = tk.StringVar(value="2")
        ttk.Entry(layout_frame, textvariable=self.value_var).pack(fill=tk.X)
        
        # 边框设置
        border_frame = ttk.LabelFrame(self.params_frame, text="边框设置", padding="5")
        border_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.border_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(border_frame, text="添加边框", variable=self.border_var,
                       command=self.toggle_border_options).pack()
        
        ttk.Label(border_frame, text="边框宽度:").pack()
        self.border_width_var = tk.StringVar(value="2")
        self.border_width_entry = ttk.Entry(border_frame, textvariable=self.border_width_var,
                                          state="disabled")
        self.border_width_entry.pack(fill=tk.X)
        
        ttk.Label(border_frame, text="边框颜色:").pack()
        self.border_color_var = tk.StringVar(value="black")
        self.border_color_entry = ttk.Entry(border_frame, textvariable=self.border_color_var,
                                          state="disabled")
        self.border_color_entry.pack(fill=tk.X)
        
        # 操作按钮
        ttk.Button(self.params_frame, text="开始拼接", command=self.start_combining).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.params_frame, text="生成预览", command=self.update_preview).pack(fill=tk.X, padx=5, pady=5)

    def create_selection_panel(self):
        """创建中间图片选择面板"""
        # 创建滚动画布
        self.selection_canvas = Canvas(self.selection_frame, bg='white')
        scrollbar_y = ttk.Scrollbar(self.selection_frame, orient=tk.VERTICAL, command=self.selection_canvas.yview)
        scrollbar_x = ttk.Scrollbar(self.selection_frame, orient=tk.HORIZONTAL, command=self.selection_canvas.xview)
        
        self.selection_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 排序按钮
        sort_frame = ttk.Frame(self.selection_frame)
        sort_frame.pack(fill=tk.X, pady=5)
        ttk.Button(sort_frame, text="↑", command=lambda: self.move_selected(-1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(sort_frame, text="↓", command=lambda: self.move_selected(1)).pack(side=tk.LEFT, padx=2)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.selection_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建图片容器框架
        self.image_frame = ttk.Frame(self.selection_canvas)
        self.selection_canvas.create_window((0, 0), window=self.image_frame, anchor='nw')
        
        # 绑定鼠标滚轮事件
        self.selection_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def create_preview_panel(self):
        """创建右侧预览面板"""
        preview_label = ttk.Label(self.preview_frame, text="预览")
        preview_label.pack(pady=5)
        
        self.preview_canvas = Canvas(self.preview_frame, bg='white')
        scrollbar_y = ttk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        scrollbar_x = ttk.Scrollbar(self.preview_frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview)
        
        self.preview_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_preview(self):
        """更新预览窗口"""
        if not self.selected_images:
            messagebox.showerror("错误", "请选择要预览的图片")
            return

        try:
            value = int(self.value_var.get())
            if value <= 0:
                messagebox.showerror("错误", "行数或列数必须大于0")
                return

            border_width = int(self.border_width_var.get()) if self.border_var.get() else 0
            border_color = self.border_color_var.get() if self.border_var.get() else 'black'

            fixed_rows = value if self.layout_var.get() == "rows" else None
            fixed_cols = value if self.layout_var.get() == "cols" else None

            # 生成预览图
            preview = combine_images_grid(self.selected_images, fixed_rows=fixed_rows, 
                                       fixed_cols=fixed_cols, 
                                       border_width=border_width, 
                                       border_color=border_color)
            
            # 调整预览图大小以适应预览窗口
            preview_width = self.preview_canvas.winfo_width()
            preview_height = self.preview_canvas.winfo_height()
            
            if preview_width > 1 and preview_height > 1:  # 确保画布已经有有效尺寸
                ratio = min(preview_width/preview.width, preview_height/preview.height)
                new_size = (int(preview.width * ratio), int(preview.height * ratio))
                preview = preview.resize(new_size, Image.Resampling.LANCZOS)
            
            # 显示预览图
            self.preview_image = ImageTk.PhotoImage(preview)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(0, 0, image=self.preview_image, anchor="nw")
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("错误", f"生成预览时出错: {str(e)}")
                    
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        widget = event.widget
        if widget == self.selection_canvas:
            self.selection_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif widget == self.preview_canvas:
            self.preview_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def toggle_border_options(self):
        state = "normal" if self.border_var.get() else "disabled"
        self.border_width_entry.config(state=state)
        self.border_color_entry.config(state=state)
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title='选择图片文件夹')
        if folder_path:
            self.folder_path = folder_path
            self.load_images()
    
    def create_thumbnail(self, image):
        """创建缩略图"""
        # 计算缩放比例
        ratio = min(self.preview_size[0]/image.width, self.preview_size[1]/image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def load_images(self):
        # 清除现有图片
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        self.images = []
        self.image_files = []
        self.thumbnails = []
        self.selected_images = []
        self.selected_indices = []
        
        # 获取图片文件
        image_files = [f for f in os.listdir(self.folder_path) 
                      if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
        if not image_files:
            messagebox.showerror("错误", "文件夹中没有可用的图片")
            return
        
        image_files.sort()
        
        # 创建网格布局
        images_per_row = 2
        row = 0
        col = 0
        
        for idx, f in enumerate(image_files):
            try:
                # 加载图片
                image_path = os.path.join(self.folder_path, f)
                img = Image.open(image_path)
                
                # 创建缩略图
                thumb = self.create_thumbnail(img)
                photo = ImageTk.PhotoImage(thumb)
                
                # 创建图片框架
                frame = ttk.Frame(self.image_frame)
                frame.grid(row=row, column=col, padx=5, pady=5)
                
                # 创建复选框
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(frame, variable=var, 
                                   command=lambda idx=idx, img=img: self.toggle_selection(idx, img))
                cb.pack()
                
                # 显示图片
                label = ttk.Label(frame, image=photo)
                label.image = photo  # 保持引用
                label.pack()
                
                # 显示文件名
                ttk.Label(frame, text=f).pack()
                
                # 保存图片相关信息
                self.images.append(img)
                self.image_files.append(f)
                self.thumbnails.append(photo)
                
                # 更新网格位置
                col += 1
                if col >= images_per_row:
                    col = 0
                    row += 1
                
            except Exception as e:
                messagebox.showerror("错误", f"无法打开图片 {f}: {str(e)}")
        
        # 更新画布滚动区域
        self.image_frame.update_idletasks()
        self.selection_canvas.configure(scrollregion=self.selection_canvas.bbox("all"))
        
        self.status_var.set(f"已加载 {len(self.images)} 张图片")
    
    def toggle_selection(self, idx, img):
        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
            self.selected_images.remove(img)
        else:
            self.selected_indices.append(idx)
            self.selected_images.append(img)
        
        # 更新状态显示
        self.status_var.set(f"已选择 {len(self.selected_images)} 张图片")
    
    def move_selected(self, direction):
        """移动选中的图片位置"""
        if len(self.selected_indices) != 1:
            messagebox.showinfo("提示", "请选择单张图片进行移动")
            return

        idx = self.selected_indices[0]
        new_idx = idx + direction
        
        if 0 <= new_idx < len(self.images):
            # 交换图片位置
            self.images[idx], self.images[new_idx] = self.images[new_idx], self.images[idx]
            self.image_files[idx], self.image_files[new_idx] = self.image_files[new_idx], self.image_files[idx]

            # 更新选中索引
            self.selected_indices = [new_idx]

            # 重新生成缩略图并更新界面
            self.refresh_image_preview()
    
    def refresh_image_preview(self):
        """更新图片预览，不重新加载文件"""
        # 清空当前预览界面
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        images_per_row = 2
        row, col = 0, 0

        for idx, img in enumerate(self.images):
            try:
                # 重新创建缩略图
                thumb = self.create_thumbnail(img)
                photo = ImageTk.PhotoImage(thumb)

                # 创建图片框架
                frame = ttk.Frame(self.image_frame)
                frame.grid(row=row, column=col, padx=5, pady=5)

                # 创建复选框
                var = tk.BooleanVar(value=idx in self.selected_indices)
                cb = ttk.Checkbutton(frame, variable=var, 
                                command=lambda idx=idx, img=img: self.toggle_selection(idx, img))
                cb.pack()

                # 显示图片
                label = ttk.Label(frame, image=photo)
                label.image = photo  # 保持引用
                label.pack()

                # 显示文件名
                ttk.Label(frame, text=self.image_files[idx]).pack()

                # 重新调整网格
                col += 1
                if col >= images_per_row:
                    col = 0
                    row += 1

            except Exception as e:
                messagebox.showerror("错误", f"无法更新图片预览: {str(e)}")

        # 更新画布滚动区域
        self.image_frame.update_idletasks()
        # self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def start_combining(self):
        if not self.selected_images:
            messagebox.showerror("错误", "请选择要拼接的图片")
            return

        try:
            value = int(self.value_var.get())
            if value <= 0:
                messagebox.showerror("错误", "行数或列数必须大于0")
                return

            border_width = int(self.border_width_var.get()) if self.border_var.get() else 0
            border_color = self.border_color_var.get() if self.border_var.get() else 'black'

            fixed_rows = value if self.layout_var.get() == "rows" else None
            fixed_cols = value if self.layout_var.get() == "cols" else None

            combined_image = combine_images_grid(self.selected_images, fixed_rows=fixed_rows, 
                                            fixed_cols=fixed_cols, 
                                            border_width=border_width, 
                                            border_color=border_color)

            folder_name = os.path.basename(self.folder_path)
            if not folder_name:
                folder_name = os.path.basename(os.path.dirname(self.folder_path))

            output_filename = f'{folder_name}_combined.jpg'
            output_path = os.path.join(self.folder_path, output_filename)

            counter = 1
            while os.path.exists(output_path):
                output_filename = f'{folder_name}_combined_{counter}.jpg'
                output_path = os.path.join(self.folder_path, output_filename)
                counter += 1

            combined_image.save(output_path, quality=95)
            messagebox.showinfo("成功", f"拼接完成，已保存为 {output_filename}")

            # 刷新图片预览，使其反映新的行/列数
            # self.refresh_image_preview()

        except ValueError as e:
            messagebox.showerror("错误", f"输入值无效: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"拼接过程中出错: {str(e)}")


def combine_images_grid(images, fixed_rows=None, fixed_cols=None, border_width=0, border_color='black'):
    """将多张图像拼接成网格布局，可以指定固定行数或列数"""
    if not images:
        raise ValueError("没有图片可供处理")
        
    if fixed_rows and fixed_cols:
        raise ValueError("行数和列数不能同时指定，请只指定其中一个")
    elif not fixed_rows and not fixed_cols:
        raise ValueError("必须指定行数或列数其中之一")
        
    n_images = len(images)
    
    # 根据指定的行数或列数计算网格维度
    if fixed_rows:
        rows, cols = fixed_rows, (n_images + fixed_rows - 1) // fixed_rows
    else:
        cols, rows = fixed_cols, (n_images + fixed_cols - 1) // fixed_cols
        
    # 获取所有图片的原始尺寸
    original_sizes = [(img.width, img.height) for img in images]
    
    # 计算最佳的单元格尺寸
    aspect_ratios = [w/h for w, h in original_sizes]
    avg_aspect_ratio = sum(aspect_ratios) / len(aspect_ratios)
    
    max_width = max(w for w, _ in original_sizes)
    max_height = max(h for _, h in original_sizes)
    
    cell_width = max_width + 2 * border_width
    cell_height = max_height + 2 * border_width
    
    # 创建新图像
    grid_width = cell_width * cols
    grid_height = cell_height * rows
    new_image = Image.new('RGB', (grid_width, grid_height), 'white')
    
    # 将每张图像粘贴到网格中
    for idx, image in enumerate(images):
        if idx >= rows * cols:  # 如果图片数量超过网格数，忽略多余的图片
            break
            
        # 计算当前图片在网格中的位置
        row = idx // cols
        col = idx % cols
        
        target_width = max_width
        target_height = max_height
        img_aspect = image.width / image.height
        
        if img_aspect > avg_aspect_ratio:
            target_height = int(target_width / img_aspect)
        else:
            target_width = int(target_height * img_aspect)
            
        resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # 添加边框
        if border_width > 0:
            resized_image = ImageOps.expand(resized_image, border=border_width, fill=border_color)
        
        x = col * cell_width + (cell_width - resized_image.width) // 2
        y = row * cell_height + (cell_height - resized_image.height) // 2
        
        if resized_image.mode != 'RGB':
            resized_image = resized_image.convert('RGB')
            
        new_image.paste(resized_image, (x, y))
    
    return new_image

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageCombinerGUI(root)
    root.mainloop()
# %%
