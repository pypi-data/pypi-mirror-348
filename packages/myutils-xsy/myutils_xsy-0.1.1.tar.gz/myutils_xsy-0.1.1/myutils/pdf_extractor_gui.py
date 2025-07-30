# %%
import sys
import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QListWidget, QMessageBox, QCheckBox, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt

class PDFExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 文本提取器")
        self.resize(600, 400)
        self.setAcceptDrops(True)  # 支持拖放

        # 布局
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("待处理的 PDF 文件（支持拖放）："))

        self.pdf_list = QListWidget()
        self.layout.addWidget(self.pdf_list)

        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("添加 PDF")
        self.add_button.clicked.connect(self.add_pdfs)
        btn_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("清空列表")
        self.clear_button.clicked.connect(self.pdf_list.clear)
        btn_layout.addWidget(self.clear_button)
        self.layout.addLayout(btn_layout)

        self.merge_checkbox = QCheckBox("合并输出为一个文本文件")
        self.layout.addWidget(self.merge_checkbox)

        self.extract_button = QPushButton("开始提取文本")
        self.extract_button.clicked.connect(self.extract_texts)
        self.layout.addWidget(self.extract_button)

        self.setLayout(self.layout)

    # 拖放功能
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self.pdf_list.addItem(path)

    # 添加文件
    def add_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        for f in files:
            self.pdf_list.addItem(f)

    # 提取逻辑
    def extract_texts(self):
        if self.pdf_list.count() == 0:
            QMessageBox.warning(self, "提示", "请先添加 PDF 文件。")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if not output_dir:
            return

        merge_output = self.merge_checkbox.isChecked()

        if merge_output:
            all_text = []
            for i in range(self.pdf_list.count()):
                path = self.pdf_list.item(i).text()
                text = self.extract_text_from_pdf(path)
                all_text.append(f"===== {os.path.basename(path)} =====\n{text}\n")
            output_path = os.path.join(output_dir, "merged_output.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(all_text))
        else:
            for i in range(self.pdf_list.count()):
                path = self.pdf_list.item(i).text()
                text = self.extract_text_from_pdf(path)
                filename = os.path.splitext(os.path.basename(path))[0]
                output_path = os.path.join(output_dir, f"{filename}.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(text)

        QMessageBox.information(self, "完成", "提取完成！")

    # 高质量提取 + 修复换行
    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        paragraphs = []

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            page_text = []
            for b in blocks:
                if b["type"] == 0:  # 纯文本块
                    lines = []
                    for line in b["lines"]:
                        span_text = " ".join(span["text"] for span in line["spans"]).strip()
                        lines.append(span_text)
                    block_text = " ".join(lines)
                    # 试图修复因换行导致的断句问题（启发式：句子末尾不完整，合并）
                    block_text = self.fix_line_breaks(block_text)
                    if block_text:
                        page_text.append(block_text)
            if page_text:
                paragraphs.append("\n".join(page_text))

        doc.close()
        return "\n\n".join(paragraphs)

    def fix_line_breaks(self, text):
        import re
        # 简单合并断句（避免“的\n下一句”）— 仅用于文本提取
        text = re.sub(r'(?<![\.\?\!。？！])\n(?![\n\-•\d])', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PDFExtractorApp()
    win.show()
    sys.exit(app.exec_())

# %%
import sys
import os
import fitz  # PyMuPDF
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget,
    QMessageBox, QCheckBox, QLabel, QHBoxLayout, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QDialog
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF
from PIL import Image


class RegionSelector(QDialog):
    def __init__(self, image_path, dpi=150):
        super().__init__()
        self.setWindowTitle("框选表格区域")
        self.dpi = dpi
        self.start = None
        self.end = None
        self.rect = QRectF()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.pixmap = QPixmap(image_path)
        self.item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.item)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == event.MouseButtonPress:
            self.start = event.pos()
        elif event.type() == event.MouseMove and self.start:
            self.end = event.pos()
            self.update_rect()
        elif event.type() == event.MouseButtonRelease:
            self.end = event.pos()
            self.update_rect()
            self.accept()
        return super().eventFilter(source, event)

    def update_rect(self):
        self.rect = QRectF(self.view.mapToScene(self.start), self.view.mapToScene(self.end))
        self.scene.removeItem(self.item)
        self.item = QGraphicsPixmapItem(self.pixmap.copy())
        painter = QPainter(self.pixmap)
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        painter.drawRect(self.rect)
        painter.end()
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

    def get_bbox_in_pdf_coords(self):
        x0 = self.rect.left() * 72 / self.dpi
        y0 = self.rect.top() * 72 / self.dpi
        x1 = self.rect.right() * 72 / self.dpi
        y1 = self.rect.bottom() * 72 / self.dpi
        return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


class PDFExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 提取工具")
        self.resize(600, 400)

        self.bbox = None  # 选中的表格区域

        self.layout = QVBoxLayout()
        self.pdf_list = QListWidget()
        self.layout.addWidget(QLabel("PDF 文件列表："))
        self.layout.addWidget(self.pdf_list)

        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("添加 PDF")
        self.add_button.clicked.connect(self.add_pdfs)
        btn_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("清空")
        self.clear_button.clicked.connect(self.pdf_list.clear)
        btn_layout.addWidget(self.clear_button)
        self.layout.addLayout(btn_layout)

        self.table_mode_checkbox = QCheckBox("启用结构化表格提取")
        self.table_mode_checkbox.stateChanged.connect(self.toggle_table_mode)
        self.layout.addWidget(self.table_mode_checkbox)

        self.select_area_button = QPushButton("选择表格区域")
        self.select_area_button.setEnabled(False)
        self.select_area_button.clicked.connect(self.select_table_area)
        self.layout.addWidget(self.select_area_button)

        self.merge_checkbox = QCheckBox("合并输出为一个文本文件")
        self.layout.addWidget(self.merge_checkbox)

        self.extract_button = QPushButton("开始提取")
        self.extract_button.clicked.connect(self.extract)
        self.layout.addWidget(self.extract_button)

        self.setLayout(self.layout)

    def toggle_table_mode(self):
        if self.table_mode_checkbox.isChecked():
            self.merge_checkbox.setEnabled(False)
            self.select_area_button.setEnabled(True)
        else:
            self.merge_checkbox.setEnabled(True)
            self.select_area_button.setEnabled(False)

    def add_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        if self.table_mode_checkbox.isChecked() and len(files) > 1:
            QMessageBox.warning(self, "限制", "表格提取模式下仅支持一个 PDF。")
            return
        for f in files:
            self.pdf_list.addItem(f)

    def select_table_area(self):
        if self.pdf_list.count() != 1:
            QMessageBox.warning(self, "提示", "请仅添加一个 PDF。")
            return
        path = self.pdf_list.item(0).text()
        doc = fitz.open(path)
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        image_path = "temp_preview.png"
        pix.save(image_path)

        dlg = RegionSelector(image_path)
        if dlg.exec_() == QDialog.Accepted:
            self.bbox = dlg.get_bbox_in_pdf_coords()

        os.remove(image_path)
        doc.close()

    def extract(self):
        if self.pdf_list.count() == 0:
            QMessageBox.warning(self, "提示", "请添加 PDF 文件")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if not output_dir:
            return

        if self.table_mode_checkbox.isChecked():
            self.extract_table_mode(output_dir)
        else:
            self.extract_text_mode(output_dir)

    def extract_table_mode(self, output_dir):
        if not self.bbox:
            QMessageBox.warning(self, "提示", "请先选择表格区域")
            return

        path = self.pdf_list.item(0).text()
        doc = fitz.open(path)
        page = doc.load_page(0)
        table_text = self.extract_table_text(page, self.bbox)
        output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(path))[0] + "_table.csv")

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in table_text:
                writer.writerow(row)

        QMessageBox.information(self, "完成", f"表格内容已导出：\n{output_path}")

    def extract_table_text(self, page, bbox):
        x0, y0, x1, y1 = bbox
        blocks = page.get_text("dict")["blocks"]
        rows = {}

        for b in blocks:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    sx0, sy0, sx1, sy1 = span["bbox"]
                    if x0 <= sx0 <= x1 and y0 <= sy0 <= y1:
                        cy = round((sy0 + sy1) / 2)
                        rows.setdefault(cy, []).append((sx0, span["text"]))

        structured = []
        for y in sorted(rows):
            row = [text for x, text in sorted(rows[y], key=lambda item: item[0])]
            structured.append(row)

        return structured

    def extract_text_mode(self, output_dir):
        merge = self.merge_checkbox.isChecked()
        if merge:
            all_text = []
            for i in range(self.pdf_list.count()):
                path = self.pdf_list.item(i).text()
                text = self.extract_text(path)
                all_text.append(f"===== {os.path.basename(path)} =====\n{text}")
            merged_path = os.path.join(output_dir, "merged_output.txt")
            with open(merged_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(all_text))
        else:
            for i in range(self.pdf_list.count()):
                path = self.pdf_list.item(i).text()
                text = self.extract_text(path)
                name = os.path.splitext(os.path.basename(path))[0]
                with open(os.path.join(output_dir, f"{name}.txt"), "w", encoding="utf-8") as f:
                    f.write(text)
        QMessageBox.information(self, "完成", "文本提取已完成。")

    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        paragraphs = []
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            page_text = []
            for b in blocks:
                if b["type"] == 0:
                    lines = [" ".join(span["text"] for span in line["spans"]).strip() for line in b["lines"]]
                    page_text.append(" ".join(lines))
            paragraphs.append("\n".join(page_text))
        doc.close()
        return "\n\n".join(paragraphs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PDFExtractorApp()
    win.show()
    sys.exit(app.exec_())

# %%
