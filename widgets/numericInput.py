from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QDoubleValidator
from PyQt5.QtCore import Qt, QSize
from typing import Union
from widgets.virtual_keyboard import VirtualKeyboard


class ThemedInputField(QWidget):
    SIZE_MAP = {
        "large": {"size": QSize(220, 52), "font": 16},
        "medium": {"size": QSize(180, 40), "font": 14},
        "small": {"size": QSize(90, 30), "font": 12}
    }

    COLORS = {
        "background": "#1e5d91",
        "focus": "#257bbf",
        "border": "#2c77b8",
        "text": "#ffffff",
        "placeholder": "#c8d5e0",
        "shadow": QColor(0, 0, 0, 110)
    }

    def __init__(self, label_text: str = None, placeholder="0", size="medium", numeric_only=True, parent=None):
        super().__init__(parent)

        self.numeric_only = numeric_only

        # Get style parameters
        size_info = self.SIZE_MAP.get(size, self.SIZE_MAP["medium"])
        self.input_size: QSize = size_info["size"]
        font_size: int = size_info["font"]
        radius = self.input_size.height() // 2

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Label (optional)
        self.label = None
        if label_text:
            self.label = QLabel(label_text)
            self.label.setStyleSheet(f"""
                QLabel {{
                    color: {self.COLORS['text']};
                    font-size: {font_size - 2}px;
                    font-weight: 600;
                    background: transparent;
                }}
            """)
            layout.addWidget(self.label)

        # Line Edit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setAlignment(Qt.AlignLeft)
        self.line_edit.setText("")
        self.line_edit.setFixedSize(self.input_size)

        if self.numeric_only:
            validator = QDoubleValidator(0.0, float("inf"), 6)
            validator.setNotation(QDoubleValidator.StandardNotation)
            self.line_edit.setValidator(validator)

        self.line_edit.setStyleSheet(f"""
            QLineEdit {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.COLORS['background']},
                    stop:1 #164569
                );
                border: 1px solid {self.COLORS['border']};
                border-radius: {radius}px;
                padding: 6px 12px;
                color: {self.COLORS['text']};
                font-size: {font_size}px;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.COLORS['focus']};
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.COLORS['focus']},
                    stop:1 #1c5d8c
                );
            }}
        """)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 3)
        shadow.setColor(self.COLORS["shadow"])
        self.setGraphicsEffect(shadow)

        layout.addWidget(self.line_edit)
        self.setLayout(layout)

        # Optionally expose signals
        self.textChanged = self.line_edit.textChanged
        self.textEdited = self.line_edit.textEdited
        self.editingFinished = self.line_edit.editingFinished
        self.returnPressed = self.line_edit.returnPressed

        # Restrict auto-expansion
        self.setFixedSize(self.input_size.width() + 16, self.input_size.height() + 28)
        self.line_edit.mousePressEvent = self.get_virtual_keyboard_callback(self.line_edit)

    def focusOutEvent(self, event):
        """If numeric-only and empty on blur, reset to '0'."""
        if self.numeric_only and self.line_edit.text().strip() == "":
            self.line_edit.setText("0")
        super().focusOutEvent(event)

    def text(self) -> str:
        return self.line_edit.text()

    def value(self) -> Union[float, str]:
        """
        Returns:
            float if numeric_only is True,
            str otherwise
        """
        text = self.line_edit.text().strip()
        if self.numeric_only:
            try:
                return float(text)
            except ValueError:
                return 0.0
        else:
            return text

    def setValue(self, value: Union[float, str]):
        """
        Sets the input field value. Accepts float or string.
        """
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
