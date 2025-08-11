from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utilities.fontManager import FontManager


class Heading(QLabel):
    def __init__(self, text: str, font_size: int = 24, parent=None):
        super().__init__(text, parent)

        # Full width and height alignment
        self.setAlignment(Qt.AlignCenter)

        # Make background transparent (optional)
        self.setStyleSheet(f"""
            QLabel {{
                color: #ffffff;
                font-size: {font_size}px;
                background: transparent;
            }}
        """)

        font_name = FontManager.get_font("michroma")
        font = QFont(font_name)
        self.setFont(font)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)

        # Allow expansion with layouts
        self.setMinimumHeight(font_size * 2)
        self.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Preferred)
