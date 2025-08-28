import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QPushButton, QMainWindow
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPen


# --------------------- DynamicButton ---------------------
class DynamicButton(QWidget):
    def __init__(self, diameter=32, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # No clicks
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(diameter, diameter)

        self.checked = False
        self.border_color = QColor("#222")
        self.fill_color = QColor("#0078d7")

    def setChecked(self, state):
        self.checked = state
        self.update()

    def isChecked(self):
        return self.checked

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 2

        # Border circle
        pen = QPen(self.border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, radius, radius)

        # Inner filled circle if checked
        if self.checked:
            inner_radius = radius * 0.6
            painter.setBrush(self.fill_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, inner_radius, inner_radius)


# --------------------- ButtonGridWidget ---------------------
LABEL_SIZE = 32
BUTTON_SIZE = 32

class ButtonGridWidget(QWidget):
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.buttons = []

        # Container with shadow for the grid
        container = QWidget()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(4, 4)
        container.setGraphicsEffect(shadow)
        container.setStyleSheet("""
            QWidget {
                background: #fff;
                border-radius: 16px;
            }
        """)

        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(25, 25, 25, 25)

        # Empty top-left cell
        empty_label = QLabel("")
        empty_label.setFixedSize(LABEL_SIZE, LABEL_SIZE)
        grid_layout.addWidget(empty_label, 0, 0)

        # Column labels (clickable)
        for c in range(cols):
            col_label = QLabel(f"{c + 1}")
            col_label.setFont(QFont("Arial", 12))
            col_label.setAlignment(Qt.AlignCenter)
            col_label.setFixedHeight(LABEL_SIZE)
            col_label.setStyleSheet("""
                QLabel {
                    color: #0078d7;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #f9f9f9, stop:1 #e3e3e3);
                    border-radius: 16px;
                }
                QLabel:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #ffffff, stop:1 #d6d6d6);
                }
            """)
            col_label.mousePressEvent = lambda e, cc=c: self.toggleColumn(cc)
            grid_layout.addWidget(col_label, 0, c + 1)

        # Buttons with row labels
        for r in range(rows):
            row_label = QLabel(chr(65 + r))
            row_label.setFont(QFont("Arial", 12))
            row_label.setAlignment(Qt.AlignCenter)
            row_label.setFixedWidth(LABEL_SIZE)
            row_label.setStyleSheet("color: #444;")
            grid_layout.addWidget(row_label, r + 1, 0)

            row_buttons = []
            for c in range(cols):
                btn = DynamicButton(diameter=BUTTON_SIZE)
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                row_buttons.append(btn)
                grid_layout.addWidget(btn, r + 1, c + 1)
            self.buttons.append(row_buttons)

        # Layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(3)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

    def toggleColumn(self, col):
        all_checked = all(self.buttons[r][col].checked for r in range(self.rows))
        for r in range(self.rows):
            self.buttons[r][col].setChecked(not all_checked)

    def getSelectedCells(self):
        selected = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.buttons[r][c].isChecked():
                    selected.append(f"{chr(65 + r)}{c + 1}")
        return selected
