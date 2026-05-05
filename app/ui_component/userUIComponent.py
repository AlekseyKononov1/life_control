from controller.userController import IUserController

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QScrollArea, QLabel, QStyle
)
from PyQt6.QtGui import QColor, QPalette, QTextCursor, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QSize
import sys
import re


class NoScrollTextEdit(QTextEdit):
    def wheelEvent(self, event):
        bar = self.verticalScrollBar()
        delta = event.angleDelta().y()

        atTop = bar.value() == bar.minimum()
        atBottom = bar.value() == bar.maximum()

        if (delta > 0 and atTop) or (delta < 0 and atBottom):
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
        nextIdx = (idx + direction) % len(fields)
        fields[nextIdx].textbox.setFocus()


class TextItem(QWidget):
    def __init__(self, onDelete, txt: str=None):
        super().__init__()

        self.onDelete = onDelete

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.textbox = NoScrollTextEdit()
        self.textbox.setFixedHeight(120)
        if isinstance(txt, str): self.textbox.setText(txt)

        self.deleteBtn = QPushButton("X")
        self.deleteBtn.setStyleSheet("background-color: #8b0000; color: white;")
        self.deleteBtn.clicked.connect(self.deleteSelf)

        layout.addWidget(self.textbox)
        layout.addWidget(self.deleteBtn)

        layout.setStretch(0, 87)
        layout.setStretch(1, 13)

    def deleteSelf(self):
        self.onDelete(self)
        self.setParent(None)
        self.deleteLater()


class TextSection(QWidget):
    def __init__(self, title):
        super().__init__()

        mainLayout = QVBoxLayout(self)

        label = QLabel(title)
        label.setStyleSheet("font-size: 20px; color: white;")
        mainLayout.addWidget(label)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.container = QWidget()
        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.containerLayout.addStretch()

        self.scrollArea.setWidget(self.container)
        mainLayout.addWidget(self.scrollArea)

        addBtn = QPushButton("Add Field")
        addBtn.setStyleSheet("background-color: #3A4A8A; color: white;")
        addBtn.clicked.connect(self.addField)
        mainLayout.addWidget(addBtn)

        self.fields = []

    def addField(self, txt: str):
        field = TextItem(onDelete=self.removeField, txt=txt)
        self.containerLayout.insertWidget(self.containerLayout.count() - 1, field)
        self.fields.append(field)

    def removeField(self, field):
        if field in self.fields:
            self.fields.remove(field)
            field.setParent(None)
            field.deleteLater()

    def hasInvalidFields(self):
        for field in self.fields:
            if re.search(r"\d", field.textbox.toPlainText()):
                return True
        return False


class MainWindow(QWidget):
    def __init__(self, userController: IUserController):
        super().__init__()
        self.userController = userController
        self.deleteNewLineRE = re.compile(r"\n")

        self.setWindowTitle("Two Sections UI")
        self.resize(1920, 1080)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#0A0E23"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#1A1F3C"))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

        mainLayout = QVBoxLayout(self)

        topBar = QHBoxLayout()

        self.statusLabel = QLabel("")
        self.statusLabel.setStyleSheet("color: #FF5555; font-size: 16px;")
        topBar.addWidget(self.statusLabel)

        topBar.addStretch()

        style = self.style()
        saveBtn = QPushButton()
        saveBtn.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        saveBtn.setIconSize(QSize(17, 17))
        saveBtn.setFixedSize(30, 30)
        saveBtn.setStyleSheet("background: #2E8B57; border-radius: 6px;")
        saveBtn.clicked.connect(self.globalSave)
        topBar.addWidget(saveBtn)

        compareBtn = QPushButton("≍")
        compareBtn.setFixedSize(30, 30)
        compareBtn.setStyleSheet("""
            background: #4682B4;
            border-radius: 6px;
            color: white;
            font-size: 22px;
            font-weight: bold;
        """)
        compareBtn.clicked.connect(self.globalCompare)
        topBar.addWidget(compareBtn)

        mainLayout.addLayout(topBar)

        sectionsLayout = QHBoxLayout()

        self.left = TextSection("Etalon")
        self.right = TextSection("User week")

        for day in self.userController.readData("db/etalon.csv"):
            self.left.addField(day)
            
        self.right.addField("something new hereA")
        self.right.addField("something new hereB")
        self.right.addField("something new hereC")

        sectionsLayout.addWidget(self.left)
        sectionsLayout.addWidget(self.right)

        mainLayout.addLayout(sectionsLayout)

        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.globalSave)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, activated=self.globalCompare)

    def validate(self):
        if self.left.hasInvalidFields() or self.right.hasInvalidFields():
            self.statusLabel.setText("Validation failed: digits are not allowed")
            return False

        self.statusLabel.setText("")
        return True

    def globalSave(self):
        # if self.validate():
        etalon = []
        for field in self.left.fields:
            etalon.append(self.deleteNewLineRE.sub("", field.textbox.toPlainText()))
        self.userController.writeData("db/etalon.csv", etalon)
        
    def highlightRightSection(self):
        for i, field in enumerate(self.right.fields):
            if i % 2 == 0:
                field.textbox.setStyleSheet("border: 2px solid red;")
            else:
                field.textbox.setStyleSheet("border: 2px solid green;")

    def globalCompare(self):
        if not self.validate():
            return

        self.highlightRightSection()
        print(2)