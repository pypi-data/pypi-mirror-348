import sys
import re
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLabel, QMessageBox
)


class TemplateToJsonConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("模板变量提取并导出JSON")
        self.setGeometry(100, 100, 800, 600)

        self.template_text = ""
        self.json_data = {}

        layout = QVBoxLayout()

        self.label = QLabel("请选择模板文件以提取变量并生成 JSON 数据")
        layout.addWidget(self.label)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview)

        self.load_btn = QPushButton("打开模板文件")
        self.load_btn.clicked.connect(self.load_template)
        layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("导出为 JSON 文件")
        self.save_btn.clicked.connect(self.export_json)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def load_template(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择模板文件", "", "文本文件 (*.txt *.j2)")
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            self.template_text = f.read()

        self.json_data = self.extract_variables(self.template_text)
        pretty_json = json.dumps(self.json_data, ensure_ascii=False, indent=2)
        self.preview.setPlainText(pretty_json)
        self.save_btn.setEnabled(True)

    def extract_variables(self, text):
        data = {}
        pattern = re.compile(
            r"{#\s*type:(?P<type>\w+)(?:\s+name:(?P<list_name>\w+)\s+fields:(?P<fields>[\w,]+))?\s*#}"
            r"|{{\s*(?P<var>\w+)(?:\s*\|\s*default\((?P<q>['\"])?(?P<default>.*?)?(?P=q)?\))?\s*}}"
        )
        lists = {}
        current_list = None

        for m in pattern.finditer(text):
            if m.group("type"):
                if m.group("type") == "list" and m.group("list_name"):
                    list_name = m.group("list_name")
                    fields = m.group("fields").split(",")
                    lists[list_name] = fields
                    data[list_name] = []  # 空列表
                elif m.group("type") == "multiline":
                    current_list = "multiline"
                    # current_list = None
                elif m.group("type") == "checkbox":
                    current_list = None
            elif m.group("var"):
                var = m.group("var")
                default = m.group("default") or ""
                if current_list:
                    # pass  # 忽略，避免混乱
                    data[var] = default
                else:
                    if default.lower() in ['true', 'false']:
                        data[var] = default.lower() == "true"
                    elif "\n" in default:
                        data[var] = default
                    else:
                        data[var] = default

        # 添加空 list 表结构
        for name, fields in lists.items():
            data[name] = [
                {field: "" for field in fields}
            ]

        return data

    def export_json(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存为 JSON", "", "JSON 文件 (*.json)")
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=2)
        QMessageBox.information(self, "完成", "JSON 数据已保存")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemplateToJsonConverter()
    window.show()
    sys.exit(app.exec_())
