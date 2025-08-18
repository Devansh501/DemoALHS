from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtGui import QColor, QDoubleValidator
from PyQt5.QtCore import Qt, QSize
from typing import Union
from widgets.virtual_keyboard import VirtualKeyboard
from utilities.constants import CLICKABLE
from utilities.utils import Utils


class ThemedInputField(QWidget):
    SIZE_MAP = {
        "large": CLICKABLE["btnSizeLarge"],
        "medium": CLICKABLE["btnSizeMedium"],
        "small": CLICKABLE["btnSizeSmall"]
    }

    FONT_SIZE_MAP = {
        "large": CLICKABLE["fontSizeLarge"],
        "medium": CLICKABLE["fontSizeMedium"],
        "small": CLICKABLE["fontSizeSmall"]
    }

    COLORS = {
        "background": CLICKABLE["primary"],          # QColor
        "focus": CLICKABLE["hover"],                 # QColor
        "border": CLICKABLE["border"],               # QColor
        "text": CLICKABLE["text"],                   # QColor
        "placeholder": CLICKABLE["placeholderText"], # QColor
        "shadow": CLICKABLE["shadow"]                # QColor
    }

    def __init__(self, label_text: str = None, placeholder_text="0", size="medium", numeric_only=True, parent=None):
        super().__init__(parent)

        self.numeric_only = numeric_only

        # Size & font
        self.input_size: QSize = self.SIZE_MAP.get(size, self.SIZE_MAP["medium"])
        font_size: int = self.FONT_SIZE_MAP.get(size, self.FONT_SIZE_MAP["medium"])
        radius = self.input_size.height() // 5

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Label (optional)
        self.label = None
        if label_text:
            label_color = Utils.color_to_rgba_str(self.COLORS["text"])
            self.label = QLabel(label_text)
            self.label.setStyleSheet(f"""
                QLabel {{
                    color: {label_color};
                    font-size: {font_size - 2}px;
                    font-weight: 600;
                    background: transparent;
                }}
            """)
            layout.addWidget(self.label)

        # Line Edit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder_text)
        self.line_edit.setAlignment(Qt.AlignLeft)
        self.line_edit.setText("")
        self.line_edit.setFixedSize(self.input_size)

        if self.numeric_only:
            validator = QDoubleValidator(0.0, float("inf"), 6)
            validator.setNotation(QDoubleValidator.StandardNotation)
            self.line_edit.setValidator(validator)

        # Colors for QSS (convert QColor -> rgba(...))
        bg_start = self.COLORS["background"]
        bg_end = QColor(bg_start).darker(115)     # darker variant for gradient end
        focus_start = self.COLORS["focus"]
        focus_end = QColor(focus_start).darker(115)
        border = self.COLORS["border"]
        text = self.COLORS["text"]
        placeholder = self.COLORS["placeholder"]

        bg_start_s = Utils.color_to_rgba_str(bg_start)
        bg_end_s = Utils.color_to_rgba_str(bg_end)
        focus_start_s = Utils.color_to_rgba_str(focus_start)
        focus_end_s = Utils.color_to_rgba_str(focus_end)
        border_s = Utils.color_to_rgba_str(border)
        text_s = Utils.color_to_rgba_str(text)
        placeholder_s = Utils.color_to_rgba_str(placeholder)

        self.line_edit.setStyleSheet(f"""
            QLineEdit {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {bg_start_s},
                    stop:1 {bg_end_s}
                );
                border: 1px solid {border_s};
                border-radius: {radius}px;
                padding: 6px 12px;
                color: {text_s};
                font-size: {font_size}px;
                qproperty-alignment: AlignRight;
            }}
            QLineEdit:focus {{
                border: 1px solid {focus_start_s};
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {focus_start_s},
                    stop:1 {focus_end_s}
                );
            }}
            QLineEdit::placeholder {{
                color: {placeholder_s};
            }}
        """)

        # Shadow on the container
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        shadow.setColor(self.COLORS["shadow"])  # QColor is fine here
        self.setGraphicsEffect(shadow)

        layout.addWidget(self.line_edit)
        self.setLayout(layout)

        # Signal passthrough
        self.textChanged = self.line_edit.textChanged
        self.textEdited = self.line_edit.textEdited
        self.editingFinished = self.line_edit.editingFinished
        self.returnPressed = self.line_edit.returnPressed

        # Auto-size correctly (prevents clipping)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.adjustSize()

        # Virtual keyboard binding
        self.line_edit.mousePressEvent = self.get_virtual_keyboard_callback(self.line_edit)

    def focusOutEvent(self, event):
        if self.numeric_only and self.line_edit.text().strip() == "":
            self.line_edit.setText("0")
        super().focusOutEvent(event)

    def text(self) -> str:
        return self.line_edit.text()

    def value(self) -> Union[float, str]:
        t = self.line_edit.text().strip()
        if self.numeric_only:
            try:
                return float(t)
            except ValueError:
                return 0.0
        return t

    def setValue(self, value: Union[float, str]):
        if self.numeric_only:
            try:
                self.line_edit.setText(f"{float(value):.2f}")
            except (ValueError, TypeError):
                self.line_edit.setText("0")
        else:
            self.line_edit.setText(str(value))

    def setPlaceholder(self, text: str):
        self.line_edit.setPlaceholderText(text)

    def setLabel(self, text: str):
        if self.label:
            self.label.setText(text)

    def get_virtual_keyboard_callback(self, target_input):
        def callback(event):
            VirtualKeyboard.show_for(target_input)
            QLineEdit.mousePressEvent(target_input, event)
        return callback
