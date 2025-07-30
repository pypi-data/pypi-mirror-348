import os  # 文件存在性检查用
import sys
import fitz  # PyMuPDF
import re
import json
from html import unescape as html_unescape

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QListWidget, QLabel, QLineEdit, QSplitter, QMessageBox,
    QScrollArea, QSizePolicy, QComboBox, QInputDialog, QTextEdit, QDialog, QListWidgetItem, QCheckBox, QRubberBand, QGridLayout  # ← 添加在这里
)
from PyQt5.QtCore import Qt, QCoreApplication, QRectF, QRect, QPoint, QSize
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QFontMetrics, QKeySequence
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QMenu, QAction
import clipboard
from myutils.utils import render_html, extract_variables_with_defaults


VAR_PATTERN = re.compile(r"{{\s*(\w+)(?:\s*\|\s*default\((['\"])?(.*?)\2?\))?\s*}}")


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_callback = None
        self.select_mode = False
        self.drag_start = None
        self.drag_end = None
        self.selection_callback = None

    def enable_selection(self, enable):
        self.select_mode = enable
        self.update()

    def mousePressEvent(self, event):
        if self.select_mode and event.button() == Qt.LeftButton:
            self.drag_start = event.pos()
            self.drag_end = event.pos()
            self.update()
        elif self.click_callback:
            self.click_callback(event)

    def mouseMoveEvent(self, event):
        if self.select_mode and self.drag_start:
            self.drag_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.select_mode and self.drag_start and self.drag_end:
            rect = QRect(self.drag_start, self.drag_end).normalized()
            if self.selection_callback:
                self.selection_callback(rect)
            self.drag_start = None
            self.drag_end = None
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.select_mode and self.drag_start and self.drag_end:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(QRect(self.drag_start, self.drag_end))
            painter.end()


class ConflictDialog(QDialog):
    def __init__(self, changes):
        super().__init__()
        self.setWindowTitle("字段冲突确认")
        self.setMinimumSize(600, 400)
        self.selected_vars = set()
        self.checkboxes = []

        layout = QVBoxLayout(self)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        for chg in changes:
            cb = QCheckBox(f"{chg['var']}: 旧值='{chg['old']}' → 新值='{chg['new']}'")
            cb.setChecked(False)
            self.checkboxes.append((cb, chg))
            self.scroll_layout.addWidget(cb)

        self.scroll.setWidget(self.scroll_content)
        layout.addWidget(self.scroll)

        btn_layout = QHBoxLayout()
        btn_yes = QPushButton("确认更新所选")
        btn_no = QPushButton("全部保留旧值")
        btn_yes.clicked.connect(self.accept)
        btn_no.clicked.connect(self.reject)
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)
        layout.addLayout(btn_layout)

        # 添加鼠标框选逻辑
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.scroll_content)
        self.origin = None

        self.scroll_content.mousePressEvent = self.start_rubber_band
        self.scroll_content.mouseMoveEvent = self.move_rubber_band
        self.scroll_content.mouseReleaseEvent = self.end_rubber_band

    def start_rubber_band(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def move_rubber_band(self, event):
        if self.origin:
            rect = QRect(self.origin, event.pos()).normalized()
            self.rubber_band.setGeometry(rect)

    def end_rubber_band(self, event):
        if self.origin:
            rect = self.rubber_band.geometry()
            for cb, _ in self.checkboxes:
                cb_rect = cb.geometry().translated(cb.parentWidget().mapTo(self.scroll_content, QPoint(0, 0)))
                if rect.intersects(cb_rect):
                    cb.setChecked(not cb.isChecked())  # 切换勾选状态
            self.rubber_band.hide()
            self.origin = None

    def get_selections(self):
        return [chg for cb, chg in self.checkboxes if cb.isChecked()]

class FullPagePreviewDialog(QDialog):
    def __init__(self, pdf_path, page_index, bbox, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"预览：{os.path.basename(pdf_path)} 第 {page_index + 1} 页")

        # 获取屏幕宽高
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.resize(int(screen_width * 0.5), int(screen_height * 0.8))

        layout = QVBoxLayout(self)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.scroll.setWidget(self.label)

        # 渲染 PDF 页面并保存原始图像
        self.original_pixmap = self.render_pdf(pdf_path, page_index, bbox)

        # 自动按窗口宽度计算缩放比例
        if not self.original_pixmap.isNull():
            available_width = int(screen_width * 0.5) - 40  # 留出边距
            self.scale = available_width / self.original_pixmap.width()
        else:
            self.scale = 1.0  # fallback

        self.update_pixmap()

    def render_pdf(self, pdf_path, page_index, bbox):
        doc = fitz.open(pdf_path)
        page = doc[page_index]
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)

        if bbox:
            painter = QPainter(pixmap)
            pen = QPen(Qt.red, 2)
            painter.setPen(pen)
            margin = 1.0  # 1pt margin
            expanded = fitz.Rect(
                bbox.x0 - margin, bbox.y0 - margin,
                bbox.x1 + margin, bbox.y1 + margin
            )
            x0 = expanded.x0 * zoom
            y0 = expanded.y0 * zoom
            w = expanded.width * zoom
            h = expanded.height * zoom
            painter.drawRect(QRectF(x0, y0, w, h))
            painter.end()

        return pixmap

    def update_pixmap(self):
        if self.original_pixmap:
            width = int(self.original_pixmap.width() * self.scale)
            height = int(self.original_pixmap.height() * self.scale)
            scaled = self.original_pixmap.scaled(
                width, height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled)
            self.label.adjustSize()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            old_pos = self.label.mapFromGlobal(event.globalPos())

            old_pixmap_size = self.label.pixmap().size()

            if event.angleDelta().y() > 0:
                self.scale *= 1.1
            else:
                self.scale *= 0.9
            self.scale = max(0.1, min(self.scale, 5.0))  # 限制缩放范围

            self.update_pixmap()

            new_pixmap_size = self.label.pixmap().size()
            scale_ratio_x = new_pixmap_size.width() / old_pixmap_size.width()
            scale_ratio_y = new_pixmap_size.height() / old_pixmap_size.height()

            new_x = old_pos.x() * scale_ratio_x - self.scroll.viewport().width() / 2
            new_y = old_pos.y() * scale_ratio_y - self.scroll.viewport().height() / 2

            self.scroll.horizontalScrollBar().setValue(int(new_x))
            self.scroll.verticalScrollBar().setValue(int(new_y))

            event.accept()
        else:
            super().wheelEvent(event)



class SearchResultDialog(QDialog):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("匹配结果选择")
        self.resize(1000, 700)
        self.selected_result = None

        layout = QVBoxLayout(self)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(10)

        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        self.card_widgets = []  # 记录每个卡片widget和对应结果


        for idx, res in enumerate(results):
            col_count = 3  # 每行 3 个
            row = idx // col_count
            col = idx % col_count

            image_label = QLabel()
            image_label.setPixmap(res["image"])
            image_label.setScaledContents(True)
            image_label.setFixedSize(200, 120)
            image_label.setCursor(Qt.PointingHandCursor)

            def make_click_fn(r):
                def open_preview(event):
                    self.selected_result = r

                    # 设置所有卡片为未选中样式
                    for card_widget, _ in self.card_widgets:
                        card_widget.setStyleSheet("QWidget { border: 2px solid lightgray; border-radius: 4px; }")

                    # 给当前卡片加红色高亮
                    for card_widget, result in self.card_widgets:
                        if result == r:
                            card_widget.setStyleSheet("QWidget { border: 3px solid red; border-radius: 6px; }")
                            break

                    preview = FullPagePreviewDialog(r["pdf_path"], r["page"], r["bbox"], self)
                    preview.exec_()
                return open_preview


            image_label.mousePressEvent = make_click_fn(res)

            caption = QLabel(f"{res['pdf']} 第 {res['page']+1} 页\n{res['text']}")
            caption.setAlignment(Qt.AlignCenter)
            caption.setWordWrap(True)

            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(image_label)
            card_layout.addWidget(caption)
            card_layout.setContentsMargins(5, 5, 5, 5)
            card_layout.setSpacing(4)

            card.setStyleSheet("QWidget { border: 2px solid lightgray; border-radius: 4px; }")  # 默认样式
            self.card_widgets.append((card, res))  # 保存卡片与数据的对应关系
            card.mousePressEvent = self.make_card_click_fn(res) 
            self.grid.addWidget(card, row, col)

        btn = QPushButton("确认当前选择")
        btn.clicked.connect(self.accept_selection)
        layout.addWidget(btn)

    def select_result(self, result):
        self.selected_result = result

        for card_widget, r in self.card_widgets:
            if r == result:
                card_widget.setStyleSheet("QWidget { border: 3px solid red; border-radius: 6px; }")
            else:
                card_widget.setStyleSheet("QWidget { border: 2px solid lightgray; border-radius: 4px; }")

    def make_card_click_fn(self, result):
        def handle_card_click(event):
            self.select_result(result)  # 只选择，不弹出预览
        return handle_card_click
    
    def accept_selection(self):
        if self.selected_result:
            self.accept()
        else:
            QMessageBox.warning(self, "未选择", "请先点击一个结果缩略图进行选择。")

class PreviewWindow(QDialog):
    def __init__(self, template_path, data, table_data, template_vars, parent=None):
        super().__init__(parent)
        self.setWindowTitle("格式签报预览")
        self.resize(800, 600)
        self.template_path = template_path
        self.template_vars = template_vars

        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # ✅ 添加导出按钮（仅导出为 txt）
        export_btn = QPushButton("导出为文本文件")
        export_btn.clicked.connect(self.export_rendered_text)
        layout.addWidget(export_btn)
        self.data = data
        self.template_vars = template_vars


        self.update_preview(data, table_data)

    def update_preview(self, data, table_data):
        try:
            with open(self.template_path, encoding="utf-8") as f:
                template_text = f.read()

            context = {}
            for k, v in data.items():
                if self.template_vars.get(k, {}).get("type") == "checkbox":
                    context[k] = bool(v)
                else:
                    context[k] = v
            for name, rows in table_data.items():
                context[name] = []
                for row in rows:
                    context[name].append({k: v for k, v in row.items()})

            html = render_html(template_text, context, self.template_vars)
            self.text_edit.setHtml(html)

        except Exception as e:
            self.text_edit.setPlainText(f"渲染失败：{e}")
        
    def export_rendered_text(self):
        html = self.text_edit.toHtml()

        # 🔍 立即检测是否存在红色字段
        has_red = re.search(
            r'color\s*:\s*(red|#f00|#ff0000|rgb\(255,\s*0,\s*0\))',
            html, re.IGNORECASE
        )

        if has_red:
            reply = QMessageBox.question(
                self,
                "包含默认内容",
                "检测到未填写字段（红色高亮），是否一并导出？\n\n"
                "点击“是”将保留这些默认值\n点击“否”将删除默认值内容\n点击“取消”将中止导出",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.No
            )

            if reply == QMessageBox.Cancel:
                return  # 🛑 用户取消导出，直接返回

            if reply == QMessageBox.No:
                # ❌ 删除红色字段
                html = re.sub(
                    r'<span style="[^"]*color\s*:\s*(red|#f00|#ff0000|rgb\(255,\s*0,\s*0\))[^"]*">.*?</span>',
                    '',
                    html,
                    flags=re.IGNORECASE | re.DOTALL
                )

        # ✅ 再弹出保存对话框（确认保存路径）
        path, _ = QFileDialog.getSaveFileName(self, "保存文本文件", "", "文本文件 (*.txt)")
        if not path:
            return

        # ✅ 转换为纯文本
        plain_text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
        plain_text = re.sub(r'<style.*?>.*?</style>', '', plain_text, flags=re.DOTALL | re.IGNORECASE)
        plain_text = re.sub(r'<[^>]+>', '', plain_text)
        plain_text = html_unescape(plain_text)


        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(plain_text.strip())
            QMessageBox.information(self, "导出成功", f"内容已保存到：\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"无法保存文本文件：{e}")



class PDFFieldChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF签报字段识别确认工具")
        self.resize(1200, 700)

        self.template_vars = {}
        self.detected_values = {}
        self.var_to_pos = {}

        self.pdf_doc = None
        self.pdf_text_pages = []
        self.pdf_image_cache = {}
        self.pdf_cache = {}
        self.current_pdf_path = None

        self.current_page = 0
        self.current_highlight = None

        self.zoom_factor = 2
        self.scale_ratio = 1.0

        self.selecting = False
        self.pdf_selector = QComboBox()
        self.select_button = QPushButton("开始选词")
        self.field_aliases = {} 
        self.init_ui()
        
        self.table_data = {}  # 存储所有 list 表格数据
        self.list_definitions = {}  # 从模板中提取的 list 结构字段定义


    def init_ui(self):
        # 顶部按钮区
        top_layout = QHBoxLayout()
        self.load_tmpl_btn = QPushButton("加载模板")  # ← 用 self. 保存引用
        self.load_tmpl_btn.clicked.connect(self.load_template)

        self.load_alias_btn = QPushButton("加载别名")
        self.load_alias_btn.clicked.connect(self.load_aliases)

        load_pdf_btn = QPushButton("加载PDF")
        load_pdf_btn.clicked.connect(self.load_pdf)

        self.select_button.clicked.connect(self.toggle_selection_mode)
        self.pdf_selector.currentIndexChanged.connect(self.switch_pdf_from_selector)

        restore_btn = QPushButton("恢复状态")
        save_btn = QPushButton("保存状态")
        restore_btn.clicked.connect(self.import_state)
        save_btn.clicked.connect(self.export_state)

        preview_btn = QPushButton("生成预览")
        preview_btn.clicked.connect(self.show_preview_window)
        
        top_layout.addWidget(self.load_tmpl_btn)
        top_layout.addWidget(self.load_alias_btn)
        top_layout.addWidget(load_pdf_btn)
        top_layout.addWidget(self.select_button)
        top_layout.addWidget(self.pdf_selector)
        top_layout.addWidget(restore_btn)
        top_layout.addWidget(save_btn)
        top_layout.addWidget(preview_btn)
        
        # PDF显示区（左边）
        self.page_image = ClickableLabel()
        self.page_image.setAlignment(Qt.AlignCenter)
        self.page_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.page_image.click_callback = self.handle_pdf_click

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.page_image)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.page_label = QLabel("第 0 页")
        self.prev_btn = QPushButton("← 上一页")
        self.next_btn = QPushButton("下一页 →")
        self.prev_btn.clicked.connect(self.show_prev_page)
        self.next_btn.clicked.connect(self.show_next_page)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.page_label)
        nav_layout.addWidget(self.next_btn)

        self.pdf_filename_label = QLabel("")
        self.pdf_filename_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.pdf_filename_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.pdf_filename_label.setStyleSheet("QLabel { color: gray; }")

        left_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.pdf_filename_label)
        left_layout.addLayout(title_layout)
        left_layout.addWidget(self.scroll_area)
        left_layout.addLayout(nav_layout)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # 右边：字段识别 + 表格填写 tab
        self.var_list = QListWidget()
        self.var_input = QTextEdit()
        self.var_input.setFixedHeight(80)
        self.var_input.setPlaceholderText("点击字段，然后点击或框选页面中的文字")
        self.export_btn = QPushButton("导出为JSON")
        self.export_btn.clicked.connect(self.export_json)
        # self.save_btn = QPushButton("保存修改")
        # self.save_btn.clicked.connect(self.save_field_edit)
        self.research_btn = QPushButton("重新查找当前字段")
        self.research_btn.clicked.connect(self.research_variable)

        self.var_list.itemClicked.connect(self.display_variable_match)

        self.right_tab = QTabWidget()

        # Tab1: 字段识别
        self.recog_tab = QWidget()
        self.recog_scroll = QScrollArea()
        self.recog_scroll.setWidgetResizable(True)

        self.recog_container = QWidget()
        self.recog_layout = QVBoxLayout(self.recog_container)
        self.recog_scroll.setWidget(self.recog_container)

        self.recog_tab.setLayout(QVBoxLayout())
        self.recog_tab.layout().addWidget(QLabel("识别到的字段"))
        self.recog_tab.layout().addWidget(self.var_list)
        self.recog_tab.layout().addWidget(QLabel("编辑值："))
        self.recog_tab.layout().addWidget(self.recog_scroll)
        self.recog_layout.addWidget(self.var_input)  # 初始值
        self.recog_tab.layout().addWidget(self.research_btn)
        self.recog_tab.layout().addWidget(self.export_btn)

        # recog_layout.addWidget(QLabel("识别到的字段"))
        # recog_layout.addWidget(self.var_list)
        # recog_layout.addWidget(QLabel("编辑值："))
        # recog_layout.addWidget(self.var_input)
        # recog_layout.addWidget(self.research_btn)
        # recog_layout.addWidget(self.export_btn)

        # Tab2: 表格填写
        self.table_tab = QWidget()
        self.table_tab_layout = QVBoxLayout(self.table_tab)
        self.table_tab_layout.setContentsMargins(5, 5, 5, 5)

        self.right_tab.addTab(self.recog_tab, "字段识别")
        self.right_tab.addTab(self.table_tab, "表格填写")

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_tab)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # 主区域：左右分割
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)    # ✅ PDF 左边
        splitter.addWidget(right_widget)   # ✅ 字段/表格右边
        splitter.setSizes([int(self.width() * 0.65), int(self.width() * 0.35)])

        # 外层布局
        outer = QVBoxLayout(self)
        outer.addLayout(top_layout)
        outer.addWidget(splitter)
        self.setLayout(outer)
        self.var_inputs = {}  # 记录每个变量对应的输入控件


            
    def show_preview_window(self):
        if not hasattr(self, "template_path") or not os.path.exists(self.template_path):
            QMessageBox.warning(self, "未加载模板", "请先加载模板文件再预览。")
            return

        # 获取当前表格数据
        table_data_dict = {}
        for list_name, table in self.table_data.items():
            rows = []
            for r in range(table.rowCount()):
                row_data = {}
                for c in range(table.columnCount()):
                    item = table.item(r, c)
                    val = item.text().strip() if item else ""
                    row_data[table.horizontalHeaderItem(c).text()] = val
                rows.append(row_data)
            table_data_dict[list_name] = rows

        if hasattr(self, "preview_window") and self.preview_window.isVisible():
            self.preview_window.update_preview(self.detected_values, table_data_dict)
            self.preview_window.raise_()
        else:
            self.preview_window = PreviewWindow(self.template_path, self.detected_values, table_data_dict, self.template_vars, self)
            self.preview_window.show()
            
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "退出确认",
            "是否在退出前保存当前状态？",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self.export_state()
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:  # Cancel
            event.ignore()
            
    def load_aliases(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择字段别名文件", "", "JSON 文件 (*.json)")
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                self.field_aliases = json.load(f)
            self.alias_file_path = path
            alias_name = os.path.basename(path)
            self.load_alias_btn.setText(f"已加载别名：{alias_name}")
            self.load_alias_btn.setToolTip(path)
            # QMessageBox.information(self, "加载成功", f"已成功加载别名文件：{alias_name}")
        except Exception as e:
            QMessageBox.critical(self, "加载失败", f"别名文件解析失败：\n{e}")


    def toggle_selection_mode(self):
        self.selecting = not self.selecting
        if self.selecting:
            self.select_button.setText("退出选词")
            self.page_image.enable_selection(True)
            self.page_image.selection_callback = self.handle_selection_rectangle
        else:
            self.select_button.setText("开始选词")
            self.page_image.enable_selection(False)
            self.page_image.selection_callback = None

    def handle_selection_rectangle(self, rect):
        if not self.pdf_doc:
            return
        page = self.pdf_doc[self.current_page]
        x0 = rect.left() / self.scale_ratio / self.zoom_factor
        y0 = rect.top() / self.scale_ratio / self.zoom_factor
        x1 = rect.right() / self.scale_ratio / self.zoom_factor
        y1 = rect.bottom() / self.scale_ratio / self.zoom_factor
        sel_rect = fitz.Rect(x0, y0, x1, y1)
        words = page.get_text("words")
        selected = [w[4] for w in words if fitz.Rect(w[:4]).intersects(sel_rect)]
        selected_text = " ".join(selected)
        cleaned = re.sub(r"[\s\u3000]+", "", selected_text)  # 删除换行、制表、全角空格等
        self.var_input.setText(cleaned.strip())
        # self.var_input.setText(selected_text.strip())

    def load_template(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择模板", "", "模板文件 (*.txt *.j2)")
        if not path:
            return
        with open(path, encoding='utf-8') as f:
            content = f.read()
        self.template_path = path

        # ✅ 使用通用函数提取变量信息（包括 default 和 type）
        self.template_vars = extract_variables_with_defaults(content)

        # ✅ 提取 list 类型字段的字段定义
        self.list_definitions = {
            k: v["fields"]
            for k, v in self.template_vars.items()
            if v.get("type") == "list"
        }
        # ✅ 初始化空数据（防止 build_table_tab 出错）
        for list_name in self.list_definitions:
            self.table_data[list_name] = [{"{}".format(f): "" for f in self.list_definitions[list_name]}]

        self.list_definitions = {}
        list_pattern = re.compile(r"{#\s*type:list name:(\w+)\s+fields:([\w,]+)\s*#}")
        MATCH_PATTERN = re.compile(r"{#\s*match:(before|after)\s*#}\s*{{\s*(\w+)")

        self.match_rules = {}  # 新增字典
        for m in MATCH_PATTERN.finditer(content):
            direction, var = m.group(1), m.group(2)
            self.match_rules[var] = direction  # 记录匹配方向
        for match in list_pattern.finditer(content):
            name, fields = match.group(1), match.group(2).split(",")
            self.list_definitions[name] = fields
            self.table_data[name] = [{"{}".format(f): "" for f in fields}]
        # 非列表字段（普通变量）
        # for m in VAR_PATTERN.finditer(content):
        #     var, default = m.group(1), m.group(3) or ""
        #     if var not in self.template_vars:
        #         self.template_vars[var] = default
        self.template_vars = extract_variables_with_defaults(content)
        self.update_var_list()
        self.build_table_tab()
        tmpl_name = os.path.basename(path)
        self.load_tmpl_btn.setText(f"已加载模板：{tmpl_name}")
        self.load_tmpl_btn.setToolTip(path)
    
    def build_table_tab(self):
        from functools import partial
        # 清空旧内容
        for i in reversed(range(self.table_tab_layout.count())):
            widget = self.table_tab_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for list_name, fields in self.list_definitions.items():
            label = QLabel(f"📝 {list_name}")
            self.table_tab_layout.addWidget(label)

            table = QTableWidget(5, len(fields))
            table.setHorizontalHeaderLabels(fields)
            table.setEditTriggers(QAbstractItemView.AllEditTriggers)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.setContextMenuPolicy(Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(partial(self.show_table_context_menu, table, list_name))
            table.setSelectionMode(QAbstractItemView.ExtendedSelection)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.keyPressEvent = self.make_table_keypress_handler(table)

            # ✅ 绑定 cellChanged 信号触发预览刷新
            table.cellChanged.connect(self.handle_table_change)

            # 初始化数据
            for r, row_data in enumerate(self.table_data.get(list_name, [])):
                for c, field in enumerate(fields):
                    item = QTableWidgetItem(row_data.get(field, ""))
                    table.setItem(r, c, item)

            self.table_tab_layout.addWidget(table)
            self.table_data[list_name] = table  # 用控件代替数据

    def handle_table_change(self, row, column):
        if hasattr(self, "preview_window") and self.preview_window.isVisible():
            self.refresh_preview()

    def make_table_keypress_handler(self, table):
        def handler(event):
            if event.matches(QKeySequence.Paste):
                self.paste_into_table(table)
            else:
                super(type(table), table).keyPressEvent(event)
        return handler

    def show_table_context_menu(self, table, list_name, pos):
        menu = QMenu()
        paste_action = QAction("粘贴", self)
        paste_action.triggered.connect(lambda: self.paste_into_table(table))
        add_row_action = QAction("添加一行", self)
        add_row_action.triggered.connect(lambda: table.insertRow(table.rowCount()))
        del_row_action = QAction("删除所选行", self)
        del_row_action.triggered.connect(lambda: self.delete_selected_rows(table))
        menu.addAction(del_row_action)
        menu.addAction(paste_action)
        menu.addAction(add_row_action)
        menu.exec_(table.mapToGlobal(pos))

    def delete_selected_rows(self, table):
        selected_rows = sorted(set(index.row() for index in table.selectedIndexes()), reverse=True)
        for row in selected_rows:
            table.removeRow(row)
        if hasattr(self, "preview_window") and self.preview_window.isVisible():
            self.refresh_preview()

    def paste_into_table(self, table):
        text = QApplication.clipboard().text()
        if not text:
            return

        rows = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if not rows:
            return

        # 解析为二维数组
        data = [row.split("\t") for row in rows]

        start_row = table.currentRow()
        start_col = table.currentColumn()
        if start_row == -1:
            start_row = 0
        if start_col == -1:
            start_col = 0

        # 确保有足够的行数
        required_rows = start_row + len(data)
        while table.rowCount() < required_rows:
            table.insertRow(table.rowCount())

        for r_offset, row in enumerate(data):
            for c_offset, val in enumerate(row):
                target_row = start_row + r_offset
                target_col = start_col + c_offset
                if target_col < table.columnCount():
                    item = QTableWidgetItem(val.strip())
                    table.setItem(target_row, target_col, item)
        if hasattr(self, "preview_window") and self.preview_window.isVisible():
            self.refresh_preview()

                        
    def ask_page_ranges(self, total_pages):
        reply = QMessageBox.question(self, "选择导入方式",
                                     "是否仅导入部分页码？（适用于大文件）",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return list(range(total_pages))  # 全部导入

        text, ok = QInputDialog.getText(self, "选择页码范围",
                                        f"请输入页码，如 1-3,5（总共 {total_pages} 页）:")
        if not ok or not text.strip():
            return None
        page_indices = set()
        try:
            parts = text.strip().split(",")
            for part in parts:
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    page_indices.update(range(start-1, end))
                else:
                    page_indices.add(int(part)-1)
            return sorted(i for i in page_indices if 0 <= i < total_pages)
        except Exception:
            QMessageBox.warning(self, "格式错误", "输入格式不正确，请重新输入，如：1-3,5")
            return None

    def load_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF文件 (*.pdf)")
        if not path:
            return

        doc = fitz.open(path)
        selected_pages = self.ask_page_ranges(len(doc))
        if selected_pages is None:
            return

        if path in self.pdf_cache:
            existing = self.pdf_cache[path]
            all_indices = sorted(set(existing['page_indices'] + selected_pages))
            all_pages_text = [doc[i].get_text() for i in all_indices]

            self.pdf_cache[path] = {
                'doc': doc,
                'pages_text': all_pages_text,
                'page_indices': all_indices
            }
        else:
            pages_text = [doc[i].get_text() for i in selected_pages]
            self.pdf_cache[path] = {
                'doc': doc,
                'pages_text': pages_text,
                'page_indices': selected_pages
            }
            self.pdf_selector.addItem(path)

        self.pdf_selector.setCurrentText(path)
        self.switch_pdf_to(path)
        self.detect_variables(path)


    def switch_pdf_from_selector(self):
        path = self.pdf_selector.currentText()
        self.switch_pdf_to(path)

    def switch_pdf_to(self, path):
        if not path or path not in self.pdf_cache:
            return
        self.pdf_doc = self.pdf_cache[path]['doc']
        self.pdf_text_pages = self.pdf_cache[path]['pages_text']
        self.current_pdf_path = path
        self.pdf_image_cache.clear()
        self.selected_indices = self.pdf_cache[path].get("page_indices", list(range(len(self.pdf_doc))))
        self.current_page = self.selected_indices[0]
        self.show_page(self.current_page)
        filename = os.path.basename(path)
        metrics = QFontMetrics(self.pdf_filename_label.font())

        # 控制最大宽度为 200 像素以内，中间省略
        elided_text = metrics.elidedText(filename, Qt.ElideMiddle, 200)

        self.pdf_filename_label.setText(elided_text)
        self.pdf_filename_label.setToolTip(filename)  # 鼠标悬浮显示完整路径


    def research_variable(self):
        item = self.var_list.currentItem()
        if not item:
            QMessageBox.warning(self, "未选择字段", "请先在左侧列表中选择一个字段。")
            return
        var = item.text().split("=")[0].strip()
        aliases = self.field_aliases.get(var, [var])
        results = []

        for pdf_path, cache in self.pdf_cache.items():
            doc = cache["doc"]
            text_pages = cache["pages_text"]
            page_indices = cache["page_indices"]
            for i, text in zip(page_indices, text_pages):
                for alias in aliases:
                    val, match_text, value_text = self.find_value_by_alias(var, alias, text)
                    if val:
                        page = doc[i]
                        bbox = page.search_for(match_text) 
                        if bbox:
                            rect = bbox[0]
                            zoom = self.zoom_factor
                            extra_left = rect.width * 1.5
                            extra_right = rect.width * 1.5
                            extra_bottom = rect.height * 2.0
                            extra_top = rect.height * 2.0

                            # 创建一个新矩形，扩大原bbox的范围
                            expanded_rect = fitz.Rect(
                                max(0, rect.x0 - extra_left),
                                max(0, rect.y0 - extra_top), 
                                min(page.rect.x1, rect.x1 + extra_right),
                                min(page.rect.y1, rect.y1 + extra_bottom)
                            )
                            mat = fitz.Matrix(zoom, zoom)
                            pix = page.get_pixmap(matrix=mat, clip=expanded_rect)
                            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                            pixmap = QPixmap.fromImage(img)
                            results.append({
                                "pdf": os.path.basename(pdf_path),
                                "pdf_path": pdf_path,
                                "page": i,
                                "text": match_text,
                                "value": val,
                                "bbox": rect,
                                "image": pixmap
                            })

        if not results:
            QMessageBox.information(self, "未找到", "未找到匹配结果。")
            return

        dlg = SearchResultDialog(results, self)
        if dlg.exec_() == QDialog.Accepted and dlg.selected_result:
            r = dlg.selected_result
            self.detected_values[var] = r["value"]
            self.var_to_pos[var] = {
                "pdf_path": r["pdf_path"],
                "page_index": r["page"],
                "match_text": r["text"],
                "bbox": r["bbox"]
            }
            self.update_var_list()
            self.var_input.setText(r["value"])
            self.switch_pdf_to(r["pdf_path"])
            self.show_page(r["page"], highlight_bbox=r["bbox"])
        
        if hasattr(self, "preview_window") and self.preview_window.isVisible():
            self.refresh_preview()
    
    
    def find_value_by_alias(self, var, alias, text):
        """
        返回 (value, full_match_text, value_text_for_bbox)
        """
        direction = self.match_rules.get(var, "before")
        if direction == "after":
            pattern = rf"([^\n，。；\s]+)\s*{re.escape(alias)}"
        else:
            pattern = rf"{re.escape(alias)}[:：]?\s*([^\n，。；\s]+)"
        match = re.search(pattern, text)
        if match:
            return match.group(1), match.group(0), match.group(1)  # value, match_text, value_text
        return None, None, None

        
    def detect_variables(self, path):
        changes = []
        selected_indices = self.pdf_cache[path].get("page_indices", list(range(len(self.pdf_doc))))

        for var in self.template_vars:
            aliases = self.field_aliases.get(var, [var])  # 如果没有别名就使用自己
            for i, text in zip(selected_indices, self.pdf_text_pages):
                for alias in aliases:
                    new_value, match_text, value_text = self.find_value_by_alias(var, alias, text)
                    if new_value:
                        page = self.pdf_doc[i]
                        areas = page.search_for(match_text)  # 🔍 用值来查找 bbox
                        bbox = areas[0] if areas else None

                        old_value = self.detected_values.get(var)
                        if old_value is not None and old_value != new_value:
                            changes.append({
                                "var": var,
                                "old": old_value,
                                "new": new_value,
                                "page_index": i,
                                "match_text": match_text,
                                "bbox": bbox
                            })
                        elif old_value is None:
                            self.detected_values[var] = new_value
                            self.var_to_pos[var] = {
                                "pdf_path": path,
                                "page_index": i,
                                "match_text": match_text,
                                "bbox": bbox
                            }
                        break  # 只取第一个匹配页

        if changes:
            dlg = ConflictDialog(changes)
            result = dlg.exec_()
            if result == QDialog.Accepted:
                selected = dlg.get_selections()
                for chg in selected:
                    var = chg["var"]
                    self.detected_values[var] = chg["new"]
                    self.var_to_pos[var] = {
                        "pdf_path": path,
                        "page_index": chg["page_index"],
                        "match_text": chg["match_text"],
                        "bbox": chg["bbox"]
                    }

        self.update_var_list()

    def update_var_list(self):
        self.var_list.clear()
        self.var_inputs.clear()
        for var in self.template_vars:
            val = self.detected_values.get(var, "")
            self.var_list.addItem(f"{var} = {val}")
            
            # 构建对应输入控件
            var_type = self.template_vars.get(var, {}).get("type", "singleline")
            if var_type == "checkbox":
                cb = QCheckBox()
                cb.setChecked(bool(val))
                cb.stateChanged.connect(self.save_field_edit)
                self.var_inputs[var] = cb
            else:
                te = QTextEdit()
                te.setPlainText(str(val))
                te.textChanged.connect(self.save_field_edit)
                self.var_inputs[var] = te


    def show_page(self, page_index, highlight_bbox=None):
        if not self.pdf_doc:
            return
        if 0 <= page_index < len(self.pdf_doc):
            self.current_page = page_index
            self.current_highlight = highlight_bbox
            page = self.pdf_doc[page_index]

            zoom = self.zoom_factor
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            original_pixmap = QPixmap.fromImage(img)

            available_width = self.scroll_area.width() - 20
            if available_width <= 0:
                available_width = 800
            self.scale_ratio = available_width / original_pixmap.width()
            scaled_height = int(original_pixmap.height() * self.scale_ratio)
            scaled_pixmap = original_pixmap.scaled(available_width, scaled_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            if highlight_bbox:
                painter = QPainter(scaled_pixmap)
                pen = QPen(Qt.red, 1)
                painter.setPen(pen)
                margin_pdf_units = 1.0  # 单位是 PDF 坐标系中的 point，1.0 大约是 1/72 英寸
                # 扩展 bbox
                expanded_bbox = fitz.Rect(
                    highlight_bbox.x0 - margin_pdf_units,
                    highlight_bbox.y0 - margin_pdf_units,
                    highlight_bbox.x1 + margin_pdf_units,
                    highlight_bbox.y1 + margin_pdf_units,
                )
                x0 = expanded_bbox.x0 * zoom * self.scale_ratio
                y0 = expanded_bbox.y0 * zoom * self.scale_ratio
                w = expanded_bbox.width * zoom * self.scale_ratio
                h = expanded_bbox.height * zoom * self.scale_ratio
                painter.drawRect(QRectF(x0, y0, w, h))
                painter.end()

            self.page_image.setPixmap(scaled_pixmap)
            self.page_image.setFixedSize(scaled_pixmap.size())
            self.page_label.setText(f"第 {page_index + 1} 页")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_page(self.current_page, self.current_highlight)

    def show_prev_page(self):
        if not self.pdf_doc:
            return
        idx = self.selected_indices.index(self.current_page)
        if idx > 0:
            self.show_page(self.selected_indices[idx - 1])
            
    def show_next_page(self):
        if not self.pdf_doc:
            return
        idx = self.selected_indices.index(self.current_page)
        if idx < len(self.selected_indices) - 1:
            self.show_page(self.selected_indices[idx + 1])

    def display_variable_match(self, item):
        var = item.text().split("=")[0].strip()

        # ✅ 若未初始化字段编辑区域的滚动容器，直接返回（防止错误）
        if not hasattr(self, "recog_scroll"):
            return

        scroll_bar = self.recog_scroll.verticalScrollBar()
        old_scroll_pos = scroll_bar.value()

        # 清除旧编辑器
        for i in reversed(range(self.recog_layout.count())):
            widget = self.recog_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # 添加新编辑器
        editor = self.var_inputs.get(var)
        if editor:
            self.var_input = editor
            self.recog_layout.addWidget(editor)

        # 恢复滚动位置
        scroll_bar.setValue(old_scroll_pos)

        # ✅ 跳转到 PDF 对应位置
        info = self.var_to_pos.get(var)
        if not info:
            return
        pdf_path = info["pdf_path"]
        if pdf_path != self.current_pdf_path:
            self.switch_pdf_to(pdf_path)
        self.show_page(info["page_index"], highlight_bbox=info["bbox"])


    def handle_pdf_click(self, event):
        if not self.pdf_doc or self.selecting:
            return
        click_point = event.pos()
        page = self.pdf_doc[self.current_page]
        x = click_point.x() / self.scale_ratio / self.zoom_factor
        y = click_point.y() / self.scale_ratio / self.zoom_factor
        words = page.get_text("words")
        for w in words:
            x0, y0, x1, y1, word = w[:5]
            if x0 <= x <= x1 and y0 <= y <= y1:
                # self.var_input.setText(word)
                cleaned = re.sub(r"[\s\u3000]+", "", word)  # \s 匹配所有空白，\u3000是全角空格
                self.var_input.setText(cleaned)
                break

    def save_field_edit(self):
        current_item = self.var_list.currentItem()
        if not current_item:
            return
        var = current_item.text().split("=")[0].strip()
        editor = self.var_inputs.get(var)
        if isinstance(editor, QCheckBox):
            val = editor.isChecked()
        else:
            val = editor.toPlainText().strip()
        self.detected_values[var] = val
        # self.update_var_list()
        current_item.setText(f"{var} = {val}")
        if hasattr(self, "preview_window") and self.preview_window.isVisible():
            self.refresh_preview()


    def refresh_preview(self):
        table_data_dict = {}
        for list_name, table in self.table_data.items():
            rows = []
            for r in range(table.rowCount()):
                row_data = {}
                for c in range(table.columnCount()):
                    item = table.item(r, c)
                    val = item.text().strip() if item else ""
                    row_data[table.horizontalHeaderItem(c).text()] = val
                rows.append(row_data)
            table_data_dict[list_name] = rows

        # ✅ 保留预览窗口的滚动条位置
        scroll_bar = self.preview_window.text_edit.verticalScrollBar()
        scroll_pos = scroll_bar.value()

        self.preview_window.update_preview(self.detected_values, table_data_dict)

        # ✅ 恢复滚动条位置
        scroll_bar.setValue(scroll_pos)

    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存JSON文件", "", "JSON文件 (*.json)")
        if not path:
            return
        # 合并识别值与表格数据
        final_data = dict(self.detected_values)  # 复制识别数据
        for list_name, table in self.table_data.items():
            rows = []
            for r in range(table.rowCount()):
                row_data = {}
                empty = True
                for c in range(table.columnCount()):
                    item = table.item(r, c)
                    val = item.text().strip() if item else ""
                    if val:
                        empty = False
                    row_data[table.horizontalHeaderItem(c).text()] = val
                if not empty:
                    rows.append(row_data)
            final_data[list_name] = rows

        with open(path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        QMessageBox.information(self, "完成", "已成功导出 JSON 文件")

    def export_state(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存当前状态", "", "状态文件 (*.json)")
        if not path:
            return

        pdf_cache_serializable = {}
        for pdf_path, pdf_data in self.pdf_cache.items():
            pdf_cache_serializable[pdf_path] = {
                "page_indices": pdf_data["page_indices"],
                "pages_text": pdf_data["pages_text"],
            }

        state = {
            "template_vars": self.template_vars,
            "detected_values": self.detected_values,
            "var_to_pos": {
                var: {
                    **info,
                    "bbox": [info["bbox"].x0, info["bbox"].y0, info["bbox"].x1, info["bbox"].y1]
                    if info.get("bbox") else None
                }
                for var, info in self.var_to_pos.items()
            },
            "pdf_cache": pdf_cache_serializable,
            "current_pdf_path": self.current_pdf_path,
            "alias_file_path": self.alias_file_path,
            "table_data": {
                list_name: [
                    {
                        table.horizontalHeaderItem(c).text(): (table.item(r, c).text() if table.item(r, c) else "")
                        for c in range(table.columnCount())
                    }
                    for r in range(table.rowCount())
                ]
                for list_name, table in self.table_data.items()
            },
            "list_definitions": self.list_definitions,
            "template_path": self.template_path,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        QMessageBox.information(self, "完成", "状态已保存")


    def import_state(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择状态文件", "", "状态文件 (*.json)")
        if not path:
            return
        with open(path, encoding="utf-8") as f:
            state = json.load(f)

        # 还原字段和变量位置
        self.template_vars = state.get("template_vars", {})
        self.list_definitions = state.get("list_definitions", {})  # ✅ 加这一行
        self.table_data.clear()
        saved_table_data = state.get("table_data", {})
        for list_name, rows in saved_table_data.items():
            self.table_data[list_name] = rows
        self.detected_values = state.get("detected_values", {})
        self.var_to_pos = {}
        raw_var_to_pos = state.get("var_to_pos", {})
        for var, info in raw_var_to_pos.items():
            bbox_list = info.get("bbox")
            bbox = fitz.Rect(*bbox_list) if bbox_list else None
            self.var_to_pos[var] = {
                "pdf_path": info.get("pdf_path"),
                "page_index": info.get("page_index"),
                "match_text": info.get("match_text"),
                "bbox": bbox
            }

        # 恢复所有 PDF 缓存
        self.pdf_cache.clear()
        self.pdf_selector.clear()
        pdf_cache = state.get("pdf_cache", {})
        for pdf_path, info in pdf_cache.items():
            if not os.path.exists(pdf_path):
                continue
            try:
                doc = fitz.open(pdf_path)
                self.pdf_cache[pdf_path] = {
                    "doc": doc,
                    "pages_text": info["pages_text"],
                    "page_indices": info["page_indices"],
                }
                self.pdf_selector.addItem(pdf_path)
            except Exception:
                continue

        # 恢复当前选中的 PDF
        self.current_pdf_path = state.get("current_pdf_path")
        if self.current_pdf_path and self.current_pdf_path in self.pdf_cache:
            self.pdf_selector.setCurrentText(self.current_pdf_path)
            self.switch_pdf_to(self.current_pdf_path)
        else:
            QMessageBox.warning(self, "提示", "PDF 无法恢复或路径不存在")

        self.update_var_list()
        self.build_table_tab()
        self.template_path = state.get("template_path")
        if self.template_path and os.path.exists(self.template_path):
            tmpl_name = os.path.basename(self.template_path)
            self.load_tmpl_btn.setText(f"已加载模板：{tmpl_name}")
            self.load_tmpl_btn.setToolTip(self.template_path)

        # 加载 PDF
        if self.current_pdf_path and os.path.exists(self.current_pdf_path):
            doc = fitz.open(self.current_pdf_path)
            pages_text = [doc[i].get_text() for i in self.selected_indices]
            self.pdf_cache[self.current_pdf_path] = {
                "doc": doc,
                "pages_text": pages_text,
                "page_indices": self.selected_indices
            }
            if self.pdf_selector.findText(self.current_pdf_path) == -1:
                self.pdf_selector.addItem(self.current_pdf_path)
            self.pdf_selector.setCurrentText(self.current_pdf_path)
            self.switch_pdf_to(self.current_pdf_path)
        else:
            QMessageBox.warning(self, "错误", "PDF 文件路径无效，无法恢复 PDF")
            
        self.alias_file_path = state.get("alias_file_path")
        if self.alias_file_path and os.path.exists(self.alias_file_path):
            try:
                with open(self.alias_file_path, encoding="utf-8") as f:
                    self.field_aliases = json.load(f)
                alias_name = os.path.basename(self.alias_file_path)
                self.load_alias_btn.setText(f"已加载别名：{alias_name}")
                self.load_alias_btn.setToolTip(self.alias_file_path)
            except Exception as e:
                QMessageBox.warning(self, "别名加载失败", f"字段别名文件加载失败：{e}")



if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = PDFFieldChecker()
    window.show()
    sys.exit(app.exec_())
