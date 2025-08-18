from PyQt5.QtWidgets import QLabel, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utilities.fontManager import FontManager
from utilities.constants import HEADING


class Heading(QLabel):
    """
    A heading label similar to HTML <h1>..<h6>.
    Automatically scales font size relative to screen width (base: 1024x600).
    """

    # Base sizes for levels (designed for 1024x600 screen)
    BASE_SIZES = HEADING["base"]


    BASE_WIDTH = 1024

    def __init__(self, text: str, level: int = 1, parent=None):
        super().__init__(text, parent)

        # Clamp heading level (1–6)
        level = max(1, min(6, level))
        settings = self.BASE_SIZES[level]

        # --- Scaling ---
        screen = QApplication.primaryScreen()
        screen_width = screen.size().width() if screen else self.BASE_WIDTH
        scale_factor = screen_width / self.BASE_WIDTH

        font_size = int(settings["size"] * scale_factor)
        spacing = settings["spacing"] * scale_factor

        # --- Alignment ---
        self.setAlignment(Qt.AlignCenter)

        # --- Style ---
        self.setStyleSheet(f"""
            QLabel {{
                color: {HEADING["font_color"]};
                font-size: {font_size}px;
                background: transparent;
            }}
        """)

        # --- Font ---
        font_name = FontManager.get_font(HEADING["font_name"])
        font = QFont(font_name)
        font.setLetterSpacing(QFont.AbsoluteSpacing, spacing)
        self.setFont(font)

        # --- Layout behavior ---
        self.setMinimumHeight(font_size * 2)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
