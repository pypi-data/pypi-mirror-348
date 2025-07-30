# %%
import os
import sys
import shutil

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox,
    QPlainTextEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QCheckBox
)
from PySide6.QtCore import Qt

class RenameApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量重命名工具")
        self.setMinimumSize(800, 600)
        self.folder_path = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 文件夹选择
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("未选择文件夹")
        browse_button = QPushButton("选择文件夹")
        browse_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(QLabel("📁 文件夹："))
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(browse_button)
        layout.addLayout(folder_layout)

        # 匹配模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("🔍 匹配模式："))
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["模糊匹配", "精确匹配"])
        mode_layout.addWidget(self.mode_selector)
        layout.addLayout(mode_layout)

        # 输入区域
        input_layout = QHBoxLayout()
        self.name_input = QPlainTextEdit()
        self.name_input.setPlaceholderText("输入关键词或文件名（每行一个）")
        self.prefix_input = QPlainTextEdit()
        self.prefix_input.setPlaceholderText("输入对应编号前缀（每行一个）")
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.prefix_input)
        layout.addLayout(input_layout)

        # 新文件名选项
        self.include_original_name_checkbox = QCheckBox("在新文件名中保留原文件名")
        self.include_original_name_checkbox.setChecked(True)
        layout.addWidget(self.include_original_name_checkbox)

        # 操作按钮
        btn_layout = QHBoxLayout()
        preview_button = QPushButton("👁️ 预览")
        rename_button = QPushButton("🚀 执行重命名")
        reset_button = QPushButton("🔄 重置")

        preview_button.clicked.connect(self.preview_rename)
        rename_button.clicked.connect(self.perform_rename)
        reset_button.clicked.connect(self.reset_all)

        btn_layout.addWidget(preview_button)
        btn_layout.addWidget(rename_button)
        btn_layout.addWidget(reset_button)
        layout.addLayout(btn_layout)

        # 预览表格
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["原文件名", "新文件名"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if path:
            self.folder_path = path
            self.folder_label.setText(path)

    def get_inputs(self):
        names = [line.strip() for line in self.name_input.toPlainText().splitlines() if line.strip()]
        prefixes = [line.strip() for line in self.prefix_input.toPlainText().splitlines() if line.strip()]
        return names, prefixes

    def preview_rename(self):
        self.table.setRowCount(0)

        if not self.folder_path:
            QMessageBox.warning(self, "错误", "请先选择文件夹。")
            return

        names, prefixes = self.get_inputs()
        if len(names) != len(prefixes):
            QMessageBox.warning(self, "错误", "关键词/文件名 与 前缀数量不一致。")
            return

        files = os.listdir(self.folder_path)
        preview = []
        used_files = set()
        include_original = self.include_original_name_checkbox.isChecked()
        mode = self.mode_selector.currentText()

        if mode == "模糊匹配":
            for keyword, prefix in zip(names, prefixes):
                matched_file = None
                for f in files:
                    if keyword in f and f not in used_files:
                        matched_file = f
                        used_files.add(f)
                        break
                if matched_file:
                    name_no_ext, ext = os.path.splitext(matched_file)
                    if include_original:
                        new_name = f"{prefix}_{name_no_ext}{ext}"
                    else:
                        new_name = f"{prefix}{ext}"
                    preview.append((matched_file, new_name))
        else:  # 精确匹配
            file_map = {os.path.splitext(f)[0]: f for f in files}
            for name, prefix in zip(names, prefixes):
                if name in file_map:
                    old_file = file_map[name]
                    _, ext = os.path.splitext(old_file)
                    if include_original:
                        new_name = f"{prefix}_{name}{ext}"
                    else:
                        new_name = f"{prefix}{ext}"
                    preview.append((old_file, new_name))

        for old, new in preview:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(old))
            self.table.setItem(row, 1, QTableWidgetItem(new))

    def perform_rename(self):
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "提示", "请先点击“预览”以生成重命名列表。")
            return

        count = 0
        for row in range(self.table.rowCount()):
            old_name = self.table.item(row, 0).text()
            new_name = self.table.item(row, 1).text()
            old_path = os.path.join(self.folder_path, old_name)
            new_path = os.path.join(self.folder_path, new_name)

            if os.path.exists(new_path):
                reply = QMessageBox.question(
                    self,
                    "文件已存在",
                    f"文件 {new_name} 已存在，是否覆盖？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    continue

            try:
                os.rename(old_path, new_path)
                count += 1
            except Exception as e:
                QMessageBox.warning(self, "错误", f"重命名失败：{old_name} -> {new_name}\n错误信息：{e}")
                return

        QMessageBox.information(self, "完成", f"成功重命名文件 {count} 个。")
        self.reset_all()

    def reset_all(self):
        self.name_input.clear()
        self.prefix_input.clear()
        self.table.setRowCount(0)
        self.folder_label.setText("未选择文件夹")
        self.folder_path = ""
        self.include_original_name_checkbox.setChecked(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RenameApp()
    window.show()
    app.exec()


# %%
