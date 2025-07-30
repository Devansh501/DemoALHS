from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HeadingWidget(QWidget):
    SIZE_MAP = {
        "large": 28,
        "medium": 24,
        "small": 18
    }

    def __init__(self, text, alignment='left', stretchable=False, size='large', parent=None):
        super().__init__(parent)

        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(text)
        font = QFont()
        font.setPointSize(self.SIZE_MAP.get(size, 24))  # Default to medium size (24)
        # font.setBold(True)
        self.label.setFont(font)
        self.setStyleSheet("color: white; background: transparent;")


        # Set alignment
        alignment = alignment.lower()
        if alignment == 'center':
            self.label.setAlignment(Qt.AlignCenter)
            layout.addStretch()
            layout.addWidget(self.label)
            layout.addStretch()
        elif alignment == 'right':
            self.label.setAlignment(Qt.AlignRight)
            layout.addStretch()
            layout.addWidget(self.label)
        else:  # default: left
            self.label.setAlignment(Qt.AlignLeft)
            layout.addWidget(self.label)
            layout.addStretch()

        # Size policy
        if stretchable:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
