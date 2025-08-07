from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize, QEvent, QPoint
from PyQt5.QtGui import QPainter, QPixmap, QColor, QLinearGradient, QBrush


class IconButton(QPushButton):
    SIZE_MAP = {
        "small": QSize(40, 40),
        "medium": QSize(60, 60),
        "large": QSize(80, 80),
    }

    def __init__(self,
                 icon_path: str,
                 size: str = "medium",
                 parent=None,
                 primary_color: str = "#1e5d91",
                 hover_color: str = "#257bbf",
                 pressed_color: str = "#164569",
                 icon_size: int = 40,
                 shadow_color: str = "#00000080"):
        super().__init__(parent)

        self.icon_path = icon_path
        self.icon_size = icon_size
        self.primary_color = primary_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.shadow_color = shadow_color

        # Button size
        self.size_label = size if size in self.SIZE_MAP else "medium"
        self.setFixedSize(self.SIZE_MAP[self.size_label])

        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background: transparent;")
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.hovered = False
        self.pressed_in = False

        # Better shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(12)
        self.shadow.setOffset(0, 4)
        self.shadow.setColor(QColor(self.shadow_color))
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed_in = True
            self.shadow.setOffset(0, 2)  # Shadow shifts closer
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed_in = False
        self.shadow.setOffset(0, 4)  # Reset shadow
        self.update()
        super().mouseReleaseEvent(event)

    def event(self, e):
        if e.type() == QEvent.TouchBegin:
            e.accept()
            self.pressed_in = True
            self.hovered = True
            self.shadow.setOffset(0, 2)
            self.update()
            return True
        elif e.type() == QEvent.TouchEnd:
            e.accept()
            self.pressed_in = False
            self.hovered = False
            self.shadow.setOffset(0, 4)
            self.update()
            self.clicked.emit()
            return True
        return super().event(e)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)

        # Simulate press-in by adjusting drawing rect
        if self.pressed_in:
            rect = rect.adjusted(1, 1, -1, -1)

        # Determine fill color
        color = QColor(
            self.pressed_color if self.pressed_in else
            self.hover_color if self.hovered else
            self.primary_color
        )

        # Gradient fill
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0, color.lighter(115))
        grad.setColorAt(1, color.darker(120))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)

        radius = self.height() / 2
        painter.drawRoundedRect(rect, radius, radius)

        # Draw icon (smooth scaling)
        if self.icon_path:
            pixmap = QPixmap(self.icon_path)
            if not pixmap.isNull():
                scale = self.icon_size - (2 if self.pressed_in else 0)
                scaled_pixmap = pixmap.scaled(scale, scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_x = (self.width() - scaled_pixmap.width()) // 2
                icon_y = (self.height() - scaled_pixmap.height()) // 2
                painter.drawPixmap(QPoint(icon_x, icon_y), scaled_pixmap)
