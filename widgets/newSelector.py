from PyQt5.QtWidgets import QComboBox, QGraphicsDropShadowEffect, QListView, QStyledItemDelegate
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QLinearGradient, QPen, QFont
from utilities.fontManager import FontManager


class AutoScaleDelegate(QStyledItemDelegate):
    """Delegate to auto-scale font size for long text in dropdown."""
    def paint(self, painter, option, index):
        text = index.data(Qt.DisplayRole) or ""
        font = QFont(option.font)  # copy font to avoid global changes
        fm = QFontMetrics(font)

        available_width = option.rect.width() - 12  # account for padding

        while fm.horizontalAdvance(text) > available_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            fm = QFontMetrics(font)

        painter.setFont(font)
        super().paint(painter, option, index)


class ThemedSelector(QComboBox):
    SIZE_MAP = {
        "large": QSize(200, 48),
        "medium": QSize(160, 36),
        "small": QSize(120, 28)
    }

    FONT_SIZE_MAP = {
        "large": 17,
        "medium": 15,
        "small": 13
    }

    DEFAULT_COLORS = {
        "primary": "#1e5d91",
        "hover": "#257bbf",
        "pressed": "#164569",
        "disabled_bg": "#26425d",
        "disabled_text": "#a0aab5",
        "text": "#ffffff"
    }

    def __init__(self, parent=None, size="medium", bold=False, **kwargs):
        super().__init__(parent)

        # Size
        if isinstance(size, QSize):
            self.setFixedSize(size)
        elif size in self.SIZE_MAP:
            self.setFixedSize(self.SIZE_MAP[size])
        else:
            self.setFixedSize(self.SIZE_MAP["medium"])

        # Font
        font_name = FontManager.get_font("lexendMega")
        self._font = QFont(font_name, self.FONT_SIZE_MAP.get(size, 18))
        if bold:
            self._font.setBold(True)
        self.setFont(self._font)

        # Colors
        self.colors = self.DEFAULT_COLORS.copy()
        for key in kwargs:
            if key in self.colors:
                self.colors[key] = kwargs[key]

        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

        # View (dropdown list)
        list_view = QListView()
        f_font = QFont(font_name, self.FONT_SIZE_MAP.get(size, 18) - 5)
        list_view.setFont(f_font)
        list_view.setTextElideMode(Qt.ElideNone)  # don't cut text
        list_view.setItemDelegate(AutoScaleDelegate())  # auto scale font
        list_view.setSpacing(0)
        list_view.setContentsMargins(0, 0, 0, 0)
        list_view.setStyleSheet(f"""
            QListView {{
                outline: none;
                border: none;
                background-color: {self.colors['primary']};
                color: {self.colors['text']};
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            QListView::item {{
                padding: 6px;
                background-color: transparent;
            }}
            QListView::item:selected {{
                background-color: {self.colors['hover']};
                border: none;
            }}
        """)
        self.setView(list_view)
        self.list_view = list_view

        # Remove default ComboBox border
        self.setStyleSheet("QComboBox { background: transparent; border: none; }")

    def showPopup(self):
        """Ensure dropdown width matches selector exactly and always opens below."""
        popup_width = self.width()
        self.view().setMinimumWidth(popup_width)

        super().showPopup()

        # Align popup exactly under combobox
        popup = self.view().window()
        if popup:
            global_pos = self.mapToGlobal(self.rect().bottomLeft())
            popup.move(global_pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)

        # Background color
        if not self.isEnabled():
            bg_color = QColor(self.colors["disabled_bg"])
            text_color = QColor(self.colors["disabled_text"])
        elif self.view().isVisible():  # Open state
            bg_color = QColor(self.colors["pressed"])
            text_color = QColor(self.colors["text"])
        else:
            bg_color = QColor(self.colors["primary"])
            text_color = QColor(self.colors["text"])

        radius = min(self.width(), self.height()) * 0.15

        # Gradient background
        grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        grad.setColorAt(0, bg_color.lighter(120))
        grad.setColorAt(1, bg_color.darker(110))

        painter.setBrush(grad)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Border
        border_pen = QPen(QColor(0, 0, 0))
        border_pen.setWidth(1)
        painter.setPen(border_pen)
        painter.drawRoundedRect(rect, radius, radius)

        # Text scaling for combo itself
        font = self.font()
        fm = QFontMetrics(font)
        text = self.currentText()
        text_width = fm.horizontalAdvance(text)
        max_text_width = rect.width() * 0.8

        while text_width > max_text_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            fm = QFontMetrics(font)
            text_width = fm.horizontalAdvance(text)

        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(rect.adjusted(8, 0, -20, 0), Qt.AlignVCenter | Qt.AlignLeft, text)

        # Arrow
        arrow_size = 8
        arrow_x = rect.right() - arrow_size - 8
        arrow_y = rect.center().y()
        painter.setBrush(QColor(text_color))
        painter.setPen(Qt.NoPen)
        points = [
            QPoint(arrow_x, arrow_y - arrow_size // 2),
            QPoint(arrow_x + arrow_size, arrow_y - arrow_size // 2),
            QPoint(arrow_x + arrow_size // 2, arrow_y + arrow_size // 2)
        ]
        painter.drawPolygon(*points)

        painter.end()
