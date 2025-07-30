# %%
import os
import platform
import subprocess
import sys
import re
import json
from collections import OrderedDict
from datetime import datetime

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit,
    QTextEdit, QPushButton, QMessageBox, QApplication, QCheckBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QFileDialog, QSplitter
)
from jinja2 import Environment, Template, TemplateSyntaxError
from markupsafe import escape
from myutils.utils import render_html, extract_variables_with_defaults

def run_sign_report_app():
    app = QApplication(sys.argv)
    window = SignReportApp()
    window.show()
    sys.exit(app.exec_())

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# TEMPLATE_PATH = os.path.join(BASE_DIR, "myutils", "templates", "report_template.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "myutils", "output", "generated_report.txt")

class SignReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("格式文档生成器")
        self.resize(1000, 600)
        self.fields = {}
        self.template_vars = OrderedDict()
        self.template_content = ""
        self.user_editing_preview = False
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)  # 设置主 layout
        self.setLayout(self.main_layout)      # 关键！将 layout 设置到窗口

        # 左侧控件（字段输入区）
        self.left_widget = QWidget()
        self.left_vlayout = QVBoxLayout(self.left_widget)
        self.form_layout = QFormLayout()

        self.edit_toggle = QCheckBox("允许编辑模板")
        self.edit_toggle.stateChanged.connect(self.toggle_preview_editable)
        self.load_template_btn = QPushButton("导入模板")
        self.load_template_btn.clicked.connect(self.select_and_load_template)
        self.import_btn = QPushButton("导入数据")
        self.import_btn.clicked.connect(self.import_data)
        self.export_data_btn = QPushButton("导出数据")
        self.export_data_btn.clicked.connect(self.export_data)
        self.generate_btn = QPushButton("导出签报")
        self.generate_btn.clicked.connect(self.export_report)

        self.left_vlayout.addWidget(self.edit_toggle)
        self.left_vlayout.addWidget(self.load_template_btn) 
        self.left_vlayout.addWidget(self.import_btn)
        self.left_vlayout.addWidget(self.export_data_btn)
        self.left_vlayout.addLayout(self.form_layout)
        self.left_vlayout.addWidget(self.generate_btn)
        self.left_vlayout.addStretch()

        # 左侧滚动区域包装（方便容纳更多字段）
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.left_widget)

        # 右侧预览框
        self.preview_box = QTextEdit()
        self.preview_box.setReadOnly(True)
        self.preview_box.setLineWrapMode(QTextEdit.WidgetWidth)
        self.preview_box.textChanged.connect(self.on_preview_edited)

        # 使用 QSplitter 可调节左右宽度
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.scroll)
        splitter.addWidget(self.preview_box)
        splitter.setSizes([400, 600])  # 初始宽度设置

        self.main_layout.addWidget(splitter)  # 将 splitter 添加到主布局

        # # 加载模板与初始渲染
        # template_path, _ = QFileDialog.getOpenFileName(
        #     self, "请选择签报模板", "", "模板文件 (*.txt);;所有文件 (*)"
        # )
        # if not template_path:
        #     QMessageBox.warning(self, "未选择模板", "未选择模板，程序即将退出。")
        #     sys.exit()

        # self.load_template(template_path)
        # self.update_preview_from_fields()

    def select_and_load_template(self):
        template_path, _ = QFileDialog.getOpenFileName(
            self, "选择模板文件", "", "模板文件 (*.txt);;所有文件 (*)"
        )
        if template_path:
            self.load_template(template_path)
            self.update_preview_from_fields()
            
    def load_template(self, template_path):
        if not os.path.exists(template_path):
            QMessageBox.critical(self, "模板缺失", f"模板文件未找到：{template_path}")
            return
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
            self.template_vars = extract_variables_with_defaults(self.template_content)
            self.rebuild_form()
            # print("🧩 提取的模板变量：")
            # print(json.dumps(self.template_vars, indent=2, ensure_ascii=False))
            self.setWindowTitle(f"格式文档生成器 - {os.path.basename(template_path)}")
        except Exception as e:
            QMessageBox.critical(self, "模板读取失败", f"读取模板失败：{e}")

    def toggle_preview_editable(self, state):
        editable = bool(state)
        self.preview_box.setReadOnly(not editable)
        self.preview_box.blockSignals(True)
        if editable:
            self.preview_box.setPlainText(self.template_content)
        else:
            old_data = {k: self._get_widget_value(w) for k, w in self.fields.items()}
            self.template_vars = extract_variables_with_defaults(self.template_content)
            self.rebuild_form()
            for var, val in old_data.items():
                w = self.fields.get(var)
                if not w: continue
                if isinstance(w, QTableWidget):
                    w.setRowCount(0)
                    for row in val:
                        self._append_table_row(var, row)
                elif isinstance(w, QTextEdit):
                    w.setPlainText(val)
                elif isinstance(w, QCheckBox):
                    w.setChecked(bool(val))
                else:
                    w.setText(str(val))
            self.update_preview_from_fields()
        self.preview_box.blockSignals(False)

    def on_preview_edited(self):
        if not self.preview_box.isReadOnly():
            new_content = self.preview_box.toPlainText()
            try:
                Environment().from_string(new_content)  # Validate syntax
                self.template_content = new_content
            except TemplateSyntaxError as e:
                QMessageBox.warning(self, "模板错误", f"模板语法无效：{e}")

    def rebuild_form(self):
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.fields.clear()
        for var, info in self.template_vars.items():
            if info['type'] == 'list':
                tbl = QTableWidget(0, len(info['fields']))
                tbl.setHorizontalHeaderLabels(info['fields'])
                tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                tbl.cellChanged.connect(lambda r, c, name=var: self.update_preview_from_fields())

                btn_add = QPushButton("新增")
                btn_add.clicked.connect(lambda _, name=var: self.add_list_row(name))

                btn_del = QPushButton("删除")
                btn_del.clicked.connect(lambda _, name=var: self.del_list_row(name))

                # 创建一个垂直容器，先放表格再放按钮
                wrapper = QWidget()
                vbox = QVBoxLayout(wrapper)
                vbox.addWidget(tbl)

                # 新建一个水平布局用于按钮排布
                btn_row = QHBoxLayout()
                btn_row.addWidget(btn_add)
                btn_row.addWidget(btn_del)
                btn_row.addStretch()  # 防止按钮顶到最右边

                vbox.addLayout(btn_row)
                self.fields[var] = tbl
                self.form_layout.addRow(var, wrapper)
            else:
                if info['type'] == 'multiline':
                    widget = QTextEdit()
                    widget.setPlaceholderText(str(info.get('default', '')))
                    widget.textChanged.connect(self.update_preview_from_fields)
                elif info['type'] == 'checkbox':
                    widget = QCheckBox()
                    default_val = info.get('default', False)
                    widget.setChecked(bool(default_val))
                    widget.stateChanged.connect(self.update_preview_from_fields)
                else:
                    widget = QLineEdit()
                    widget.setPlaceholderText(str(info.get('default', '')))
                    widget.textChanged.connect(self.update_preview_from_fields)
                self.fields[var] = widget
                self.form_layout.addRow(var, widget)

    def add_list_row(self, name):
        tbl: QTableWidget = self.fields[name]
        tbl.insertRow(tbl.rowCount())

    def del_list_row(self, name):
        tbl: QTableWidget = self.fields[name]
        r = tbl.currentRow()
        if r >= 0:
            tbl.removeRow(r)

    def _append_table_row(self, name, row_data):
        tbl: QTableWidget = self.fields[name]
        r = tbl.rowCount()
        tbl.insertRow(r)
        for c, fld in enumerate(self.template_vars[name]['fields']):
            tbl.setItem(r, c, QTableWidgetItem(row_data.get(fld, '')))

    def _get_widget_value(self, widget):
        if isinstance(widget, QTableWidget):
            name = next(k for k, v in self.fields.items() if v is widget)
            fields = self.template_vars[name]['fields']
            data = []
            for r in range(widget.rowCount()):
                entry = {}
                for c, fld in enumerate(fields):
                    item = widget.item(r, c)
                    entry[fld] = item.text() if item else ''
                data.append(entry)
            return data
        elif isinstance(widget, QTextEdit):
            return widget.toPlainText()
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        else:
            return widget.text()

    def update_preview_from_fields(self):
        if self.user_editing_preview:
            return

        data = {k: self._get_widget_value(w) for k, w in self.fields.items()}
        try:
            self.user_editing_preview = True

            # 🔹 记录滚动条位置
            scroll_pos = self.preview_box.verticalScrollBar().value()

            html = render_html(self.template_content, data, self.template_vars, source='user')
            self.preview_box.blockSignals(True)
            self.preview_box.setHtml(html)

            # 🔹 恢复滚动条位置
            self.preview_box.verticalScrollBar().setValue(scroll_pos)

        except Exception as e:
            self.preview_box.setPlainText(f"模板渲染失败：{e}")
        finally:
            self.preview_box.blockSignals(False)
            self.user_editing_preview = False

    def export_report(self):
        data = {k: self._get_widget_value(w) for k, w in self.fields.items()}

        try:
            tmpl = Template(self.template_content)
            result = tmpl.render(**data)
        except Exception as e:
            QMessageBox.critical(self, '模板渲染失败', str(e))
            return

        # ✅ 提取文件名模板
        filename_template_match = re.search(r"{#\s*filename:\s*(.*?)\s*#}", self.template_content)
        if filename_template_match:
            filename_expr = filename_template_match.group(1).strip()
            try:
                now = datetime.now()
                jinja_context = {
                    **{k: v for k, v in data.items() if k not in {"当前日期", "当前时间", "当前时间戳"}},
                    "当前日期": now.strftime("%Y%m%d"),
                    "当前时间": now.strftime("%H%M%S"),
                    "当前时间戳": now.strftime("%Y%m%d_%H%M%S")
                }
                filename = Template(filename_expr).render(**jinja_context)
                # 用 Jinja2 渲染文件名模板
                # filename = Template(filename_expr).render(**data)
            except Exception:
                print("❌ 文件名模板渲染失败：", e)
                filename = "文本导出.txt"
        else:
            filename = f"{data.get('项目名称', '未命名项目')}_文本导出.txt"

        # ✅ 弹出保存框
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            filename,
            "文本文件 (*.txt);;所有文件 (*)"
        )

        if not save_path:
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(result)
            QMessageBox.information(self, '完成', f'已保存到：{save_path}')
            self.open_output_folder(os.path.dirname(save_path))
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"导出失败：{e}")

    def export_data(self):
        data = {k: self._get_widget_value(w) for k, w in self.fields.items()}
        save_path, _ = QFileDialog.getSaveFileName(self, "保存数据", "", "JSON 文件 (*.json)")
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "成功", "数据已导出")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败：{e}")

    def import_data(self):
        load_path, _ = QFileDialog.getOpenFileName(self, "导入数据", "", "JSON 文件 (*.json)")
        if load_path:
            try:
                with open(load_path, "r", encoding="utf-8") as f:
                    imported_data = json.load(f)

                for var, new_val in imported_data.items():
                    if var not in self.fields:
                        # 模板中没有此字段，新增为单行文本框
                        widget = QLineEdit()
                        widget.setText(str(new_val))
                        widget.textChanged.connect(self.update_preview_from_fields)
                        self.fields[var] = widget
                        self.template_vars[var] = {"type": "singleline", "default": ""}
                        self.form_layout.addRow(var, widget)
                        continue

                    widget = self.fields[var]
                    current_val = self._get_widget_value(widget)

                    # 判断是否为空
                    def is_empty(val):
                        if isinstance(val, list):
                            return len(val) == 0
                        if isinstance(val, bool):
                            return False  # 复选框不算空
                        return not str(val).strip()

                    if is_empty(current_val) and not is_empty(new_val):
                        # 当前为空，导入非空 → 直接导入
                        pass
                    elif not is_empty(current_val) and is_empty(new_val):
                        # 当前不空，导入为空 → 跳过，不提示
                        continue
                    elif current_val != new_val:
                        # 非空内容不一致 → 需要确认
                        reply = QMessageBox.question(
                            self, "冲突确认",
                            f"字段“{var}”已有值，是否使用导入数据替换？\n\n原值：{current_val}\n新值：{new_val}",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                        )
                        if reply == QMessageBox.No:
                            continue  # 保留原值

                    # 应用导入值
                    if isinstance(widget, QTableWidget):
                        widget.setRowCount(0)
                        for row in new_val:
                            self._append_table_row(var, row)
                    elif isinstance(widget, QTextEdit):
                        widget.setPlainText(new_val)
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(bool(new_val))
                    else:
                        widget.setText(str(new_val))

                self.update_preview_from_fields()
                QMessageBox.information(self, "成功", "数据已导入")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入失败：{e}")


    def open_output_folder(self, folder=None):
        folder = folder or os.path.dirname(OUTPUT_PATH)
        if platform.system() == 'Windows':
            os.startfile(folder)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', folder])
        else:
            subprocess.call(['xdg-open', folder])

if __name__ == '__main__':
    run_sign_report_app()
# %%
