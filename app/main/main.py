from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository
from service.validation import GuestForm
from support_utils.duration import IDuration, Duration
from repository.userRepository import UserRepository

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QScrollArea, QLabel, QStyle
)
from PyQt6.QtGui import QColor, QPalette, QTextCursor, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QSize
import sys
import re


# -----------------------------
# Custom QTextEdit with TAB navigation
# -----------------------------
class NoScrollTextEdit(QTextEdit):
    def wheelEvent(self, event):
        bar = self.verticalScrollBar()
        delta = event.angleDelta().y()

        at_top = bar.value() == bar.minimum()
        at_bottom = bar.value() == bar.maximum()

        if (delta > 0 and at_top) or (delta < 0 and at_bottom):
            event.accept()
            return

        super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.navigate(1)
            return
        elif event.key() == Qt.Key.Key_Backtab:
            self.navigate(-1)
            return

        super().keyPressEvent(event)

    def navigate(self, direction):
        item = self.parent()
        while item and item.__class__.__name__ != "TextItem":
            item = item.parent()

        if not item:
            return

        section = item.parent()
        while section and section.__class__.__name__ != "TextSection":
            section = section.parent()

        if not section:
            return

        fields = section.fields
        if not fields:
            return

        idx = fields.index(item)
        next_idx = (idx + direction) % len(fields)
        fields[next_idx].textbox.setFocus()


# -----------------------------
# Text Item (one field + delete button)
# -----------------------------
class TextItem(QWidget):
    def __init__(self, on_delete):
        super().__init__()

        self.on_delete = on_delete

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.textbox = NoScrollTextEdit()
        self.textbox.setFixedHeight(120)

        self.delete_btn = QPushButton("X")
        self.delete_btn.setStyleSheet("background-color: #8b0000; color: white;")
        self.delete_btn.clicked.connect(self.delete_self)

        layout.addWidget(self.textbox)
        layout.addWidget(self.delete_btn)

        layout.setStretch(0, 87)
        layout.setStretch(1, 13)

    def delete_self(self):
        self.on_delete(self)
        self.setParent(None)
        self.deleteLater()


# -----------------------------
# Section with scrollable list of TextItems
# -----------------------------
class TextSection(QWidget):
    def __init__(self, title):
        super().__init__()

        main_layout = QVBoxLayout(self)

        label = QLabel(title)
        label.setStyleSheet("font-size: 20px; color: white;")
        main_layout.addWidget(label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container_layout.addStretch()

        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

        add_btn = QPushButton("Add Field")
        add_btn.setStyleSheet("background-color: #3A4A8A; color: white;")
        add_btn.clicked.connect(self.add_field)
        main_layout.addWidget(add_btn)

        self.fields = []

    def add_field(self):
        field = TextItem(on_delete=self.remove_field)
        self.container_layout.insertWidget(self.container_layout.count() - 1, field)
        self.fields.append(field)

    def remove_field(self, field):
        if field in self.fields:
            self.fields.remove(field)
            field.setParent(None)
            field.deleteLater()

    def has_invalid_fields(self):
        for field in self.fields:
            if re.search(r"\d", field.textbox.toPlainText()):
                return True
        return False


# -----------------------------
# Main Window
# -----------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Two Sections UI")
        self.resize(1920, 1080)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#0A0E23"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#1A1F3C"))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)

        # ---------------- TOP BAR (GLOBAL) ----------------
        top_bar = QHBoxLayout()

        # LEFT: validation label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #FF5555; font-size: 16px;")
        top_bar.addWidget(self.status_label)

        top_bar.addStretch()

        # RIGHT: Save button
        style = self.style()
        save_btn = QPushButton()
        save_btn.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        save_btn.setIconSize(QSize(17, 17))
        save_btn.setFixedSize(30, 30)
        save_btn.setStyleSheet("background: #2E8B57; border-radius: 6px;")
        save_btn.clicked.connect(self.global_save)
        top_bar.addWidget(save_btn)

        # RIGHT: Compare button
        compare_btn = QPushButton("≍")
        compare_btn.setFixedSize(30, 30)
        compare_btn.setStyleSheet("""
            background: #4682B4;
            border-radius: 6px;
            color: white;
            font-size: 22px;
            font-weight: bold;
        """)
        compare_btn.clicked.connect(self.global_compare)
        top_bar.addWidget(compare_btn)

        main_layout.addLayout(top_bar)

        # ---------------- SECTIONS ----------------
        sections_layout = QHBoxLayout()

        self.left = TextSection("Left Section")
        self.right = TextSection("Right Section")

        sections_layout.addWidget(self.left)
        sections_layout.addWidget(self.right)

        main_layout.addLayout(sections_layout)

        # ---------------- SHORTCUTS ----------------
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.global_save)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, activated=self.global_compare)

    # ---------------- GLOBAL ACTIONS ----------------
    def validate(self):
        if self.left.has_invalid_fields() or self.right.has_invalid_fields():
            self.status_label.setText("Validation failed: digits are not allowed")
            return False

        self.status_label.setText("")
        return True

    def global_save(self):
        if self.validate():
            print(1)

    # ---------------- NEW: highlight right section ----------------
    def highlight_right_section(self):
        for i, field in enumerate(self.right.fields):
            if i % 2 == 0:
                field.textbox.setStyleSheet("border: 2px solid red;")
            else:
                field.textbox.setStyleSheet("border: 2px solid green;")

    def global_compare(self):
        if not self.validate():
            return

        self.highlight_right_section()
        print(2)


# -----------------------------
# Run App
# -----------------------------
def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()


