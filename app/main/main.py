from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository
from service.validation import GuestForm
from support_utils.duration import IDuration, Duration
from repository.userRepository import UserRepository


from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QScrollArea, QLabel
)
from PyQt6.QtGui import QColor, QPalette, QTextCursor
from PyQt6.QtCore import Qt
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
        # Find parent TextItem
        item = self.parent()
        while item and item.__class__.__name__ != "TextItem":
            item = item.parent()

        if not item:
            return

        # Find parent TextSection
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
        self.textbox.textChanged.connect(self.validate_text)

        self.delete_btn = QPushButton("X")
        # self.delete_btn.setFixedWidth(40)
        self.delete_btn.setStyleSheet("background-color: #8b0000; color: white;")
        self.delete_btn.clicked.connect(self.delete_self)

        layout.addWidget(self.textbox)
        layout.addWidget(self.delete_btn)

        layout.setStretch(0, 87)
        layout.setStretch(1, 13)

    def validate_text(self):
        text = self.textbox.toPlainText()
        cleaned = re.sub(r"\d", "", text)

        if cleaned != text:
            self.textbox.blockSignals(True)
            self.textbox.setPlainText(cleaned)

            cursor = self.textbox.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.textbox.setTextCursor(cursor)

            self.textbox.blockSignals(False)

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


# -----------------------------
# Main Window
# -----------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Two Sections UI")
        self.resize(900, 600)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#0A0E23"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#1A1F3C"))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

        layout = QHBoxLayout(self)

        left = TextSection("Left Section")
        right = TextSection("Right Section")

        layout.addWidget(left)
        layout.addWidget(right)


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
