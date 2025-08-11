from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QPen
from utilities.fontManager import FontManager


class InfoCard(QWidget):
    """
    InfoCard widget:
      - heading: string
      - points: list of strings
      - width, height: dimensions
      - fixed: if True, widget stays at given size; if False, it can resize
    """

    DEFAULT_WIDTH = 336
    DEFAULT_HEIGHT = 336
    BORDER_RADIUS = 12

    def __init__(
        self,
        heading="Pipette Info:",
        points=None,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        fixed=True,
        parent=None
    ):
        super().__init__(parent)

        # Handle QSize or integers for size
        if isinstance(width, QSize):
            w = width.width()
            h = width.height()
        else:
            w = width or self.DEFAULT_WIDTH
            h = height or self.DEFAULT_HEIGHT

        self._width = int(w)
        self._height = int(h)
        self._fixed_mode = fixed

        if self._fixed_mode:
            # Lock to exact size
            self.setFixedSize(self._width, self._height)
        else:
            # Start with a preferred size but allow resizing
            self.setMinimumSize(self._width, self._height)
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.setAutoFillBackground(False)
        self._heading_text = heading or ""
        self._points = list(points) if points else []

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(14)
        shadow.setOffset(4, 4)
        shadow.setColor(QColor(0, 0, 0, 110))
        self.setGraphicsEffect(shadow)

        self._setup_layout()

    def sizeHint(self):
        """Preferred size reported to layouts."""
        return QSize(self._width, self._height)

    def _setup_layout(self):
        # Fonts
        font_name = FontManager.get_font("lexendPeta")
        heading_font = QFont(font_name, 20)
        heading_font.setBold(True)
        heading_font.setLetterSpacing(QFont.AbsoluteSpacing, 1.8)



        point_font_name = FontManager.get_font("lexend")
        point_font = QFont(point_font_name, 12)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 26, 18)  # extra right padding
        layout.setSpacing(10)

        # Heading label
        self.heading_label = QLabel(self._heading_text, self)
        self.heading_label.setFont(heading_font)
        self.heading_label.setAlignment(Qt.AlignCenter)
        self.heading_label.setStyleSheet("color: #1e5d91;")

        heading_shadow = QGraphicsDropShadowEffect(self.heading_label)
        heading_shadow.setBlurRadius(6)
        heading_shadow.setOffset(0, 2)
        heading_shadow.setColor(QColor(0, 0, 0, 60))
        self.heading_label.setGraphicsEffect(heading_shadow)

        layout.addWidget(self.heading_label)
        layout.addStretch(2)

        # Points
        self._point_labels = []
        for idx, pt in enumerate(self._points):
            lbl = QLabel(self._format_point(idx, pt), self)
            lbl.setFont(point_font)
            lbl.setStyleSheet("color: #0b2230;")
            lbl.setWordWrap(True)
            lbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            self._point_labels.append(lbl)
            layout.addWidget(lbl)
            layout.addStretch(1)

        layout.addStretch(2)

        self._heading_font = heading_font
        self._point_font = point_font

    def _format_point(self, index, text):
        letter = chr(65 + (index % 26))
        return f"{letter}.) {text}"

    def setPoints(self, points):
        for lbl in self._point_labels:
            lbl.setParent(None)
            lbl.deleteLater()
        self._point_labels.clear()

        self._points = list(points) if points else []

        layout = self.layout()
        insert_index = 1  # after heading
        for idx, pt in enumerate(self._points):
            lbl = QLabel(self._format_point(idx, pt), self)
            lbl.setFont(self._point_font)
            lbl.setStyleSheet("color: #0b2230;")
            lbl.setWordWrap(True)
            lbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.insertWidget(insert_index, lbl)
            self._point_labels.append(lbl)
            insert_index += 1

        self.update()

    def setHeading(self, heading):
        self._heading_text = str(heading)
        self.heading_label.setText(self._heading_text)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        try:
            rect = self.rect().adjusted(0, 0, -1, -1)

            # Vertical gradient
            top_color = QColor("#a6cfe9")
            bottom_color = QColor("#d7ecf6")
            grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            grad.setColorAt(0.0, top_color)
            grad.setColorAt(1.0, bottom_color)

            painter.setBrush(grad)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, self.BORDER_RADIUS, self.BORDER_RADIUS)

            # Border
            pen = QPen(QColor(0, 0, 0))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect, self.BORDER_RADIUS, self.BORDER_RADIUS)
        finally:
            painter.end()
