# myutils-xsy

✨ 一个包含多种实用功能的 Python 工具箱，支持图形化界面启动。常用功能包括 PDF 图片处理、Word 表格提取、批量重命名、GIS 地图浏览、日期计算等，适合日常办公和研究工作。

## 📦 安装

### ✅ 使用 PyPI 主站安装（推荐）

```bash
pip install myutils-xsy -i https://pypi.org/simple
```
⚠️ 新版本发布后，国内镜像（如清华）可能存在同步延迟。如遇安装失败，请切换回主站。。

### 🇨🇳 使用清华镜像安装（同步后可用）
```bash
pip install myutils-xsy -i https://pypi.tuna.tsinghua.edu.cn/simple
```
## 🚀 使用方法

**方式一：启动 GUI 工具箱**

```bash
myutils
```
将弹出一个带按钮的工具选择窗口。

**方式二：直接调用某个命令行工具（若已定义）**
```bash
date_calculator
word2excel
batch_print_pdf
batch_renamer
combine_images_vertically
```

## 📁 工具列表（持续更新中）

| 工具名称 | 命令名 | 描述 |
| -------- | ------ | ---- |
|日期计算器| `date_calculator` |	公历、农历、节假日转换与查询|
|Word 转 Excel| `word2excel` |	批量提取 Word 表格为 Excel|
|批量打印 PDF| `batch_print_pdf` |	一键打印多个 PDF 文件|
|批量重命名| `batch_renamer` |	根据规则批量重命名文件|
|图片纵向合并| `combine_images_vertically` |	将多张图片纵向拼接合成|
|图片合并工具| `combine_images` |	更多图片合并样式支持|
|GIS 地图浏览器| `gis_map` |	简易 GIS 图层浏览与查看|
|PDF 去文字水印| `remove_pdf_watermark` |	去除 PDF 中的文字水印|
|PDF 去图片水印| `remove_pdf_fig_watermark` |	去除 PDF 中嵌入的图片水印|

## 💡 开发者使用
你也可以从源代码运行：

```bash
git clone https://github.com/xushengyichn/myutils.git
cd myutils-xsy
pip install .
myutils
```
## 🛠 依赖项
本项目基于以下开源库：

`Pillow`, `PyMuPDF`, `tkcalendar`, `geopandas`, `fiona`, `folium`, `PyQt5`,` PySide6`, `python-docx`, `zhdate` 等
所有依赖会自动在安装时拉取。

## 📄 许可证
本项目使用 MIT License 开源。

🧑‍💻 作者
Shengyi Xu
GitHub: @xushengyichn







