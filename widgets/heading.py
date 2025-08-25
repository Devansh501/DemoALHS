from PyQt5.QtWidgets import QLabel, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utilities.fontManager import FontManager
from utilities.constants import HEADING


class Heading(QLabel):
    """
    Responsive heading label (similar to HTML <h1>..<h6>).
    Scales font size relative to screen width (base: 1024x600).
    """

    BASE_SIZES = HEADING["base"]
    BASE_WIDTH = 1024  # Reference width for scaling

    def __init__(self, text: str, level: int = 1, parent=None):
        super().__init__(text, parent)

        # --- Clamp level ---
        level = max(1, min(6, level))
        settings = self.BASE_SIZES[level]

        # --- Screen scaling ---
        screen = QApplication.primaryScreen()
        screen_width = screen.size().width() if screen else self.BASE_WIDTH
        scale_factor = screen_width / self.BASE_WIDTH

        font_size = int(settings["size"] * scale_factor)
        spacing = settings["spacing"]

        # --- Alignment ---
        self.setAlignment(Qt.AlignCenter)

        # --- Font ---
        font_name = FontManager.get_font(HEADING["font_name"])
        font = QFont(font_name)
        font.setPointSize(font_size)
        font.setLetterSpacing(QFont.AbsoluteSpacing, spacing)
        self.setFont(font)

        # --- Style ---
        self.setStyleSheet(f"""
            QLabel {{
                color: {HEADING["font_color"]};
                background: transparent;
            }}
        """)

        # --- Layout behavior ---
        self.setMinimumHeight(int(font_size * 2))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
