from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QLinearGradient, QPen, QFont
from utilities.fontManager import FontManager



class ThemedButton(QPushButton):
    SIZE_MAP = {
        "large": QSize(160, 48),
        "medium": QSize(120, 36),
        "small": QSize(90, 28)
    }

    FONT_SIZE_MAP = {
        "large":  19,
        "medium": 17,
        "small": 15
    }

    DEFAULT_COLORS = {
        "primary": "#1e5d91",
        "hover": "#257bbf",
        "pressed": "#164569",
        "disabled_bg": "#26425d",
        "disabled_text": "#a0aab5",
        "text": "#ffffff"
    }

    def __init__(self, text="", parent=None, size="medium", bold = False, **kwargs):
        super().__init__(text, parent)

        if isinstance(size, QSize):
            self.setFixedSize(size)
        elif size in self.SIZE_MAP:
            self.setFixedSize(self.SIZE_MAP[size])
        else:
            self.setFixedSize(self.SIZE_MAP["medium"])
        
        font_name = FontManager.get_font("lexendMega")
        self._font = QFont(font_name, self.FONT_SIZE_MAP.get(size, 18))
        if bold:
            self._font.setBold(True)
        
        self.setFont(self._font)

        self.colors = self.DEFAULT_COLORS.copy()
        for key in kwargs:
            if key in self.colors:
                self.colors[key] = kwargs[key]

        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background: transparent;")
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.hovered = False
        self.pressed_in = False

        # Drop shadow effect (Material style)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed_in = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed_in = False
        self.update()
        super().mouseReleaseEvent(event)

    def event(self, e):
        if e.type() == QEvent.TouchBegin:
            e.accept()
            self.pressed_in = True
            self.hovered = True
            self.update()
            return True
        elif e.type() == QEvent.TouchUpdate:
            e.accept()
            return True
        elif e.type() == QEvent.TouchEnd:
            e.accept()
            self.pressed_in = False
            self.hovered = False
            self.update()
            self.clicked.emit()
            return True
        return super().event(e)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Full rect, slightly inset to prevent overflow from pen width
        rect = self.rect().adjusted(1, 1, -1, -1)

        if self.pressed_in:
            rect = rect.adjusted(1, 1, -1, -1)

        # Colors
        if not self.isEnabled():
            bg_color = QColor(self.colors["disabled_bg"])
            text_color = QColor(self.colors["disabled_text"])
        elif self.pressed_in:
            bg_color = QColor(self.colors["pressed"])
            text_color = QColor(self.colors["text"])
        elif self.hovered:
            bg_color = QColor(self.colors["hover"])
            text_color = QColor(self.colors["text"])
        else:
            bg_color = QColor(self.colors["primary"])
            text_color = QColor(self.colors["text"])

        radius = min(self.width(), self.height()) * 0.15

        # Background gradient
        grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        grad.setColorAt(0, bg_color.lighter(120))
        grad.setColorAt(1, bg_color.darker(110))

        painter.setBrush(grad)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # ✅ Single clean black border
        border_pen = QPen(QColor(0, 0, 0))
        border_pen.setWidth(1)
        painter.setPen(border_pen)
        painter.drawRoundedRect(rect, radius, radius)

        # Draw text
        font = self.font()
        fm = QFontMetrics(font)
        text = self.text()
        text_width = fm.horizontalAdvance(text)
        max_text_width = rect.width() * 0.8

        while text_width > max_text_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            fm = QFontMetrics(font)
            text_width = fm.horizontalAdvance(text)

        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(rect, Qt.AlignCenter, text)

        painter.end()
