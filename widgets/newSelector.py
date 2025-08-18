from PyQt5.QtWidgets import (
    QComboBox, QGraphicsDropShadowEffect, QListView,
    QStyledItemDelegate, QStyleOptionComboBox, QStyle
)
from PyQt5.QtCore import QSize, Qt, QPoint, QRect
from PyQt5.QtGui import (
    QPainter, QColor, QFontMetrics,
    QPen, QFont
)
from utilities.utils import Utils
from utilities.constants import CLICKABLE
from utilities.fontManager import FontManager


class PerfectDelegate(QStyledItemDelegate):
    """Delegate that ensures perfect text display without truncation"""
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setWidth(size.width() + 20)  # Add padding
        return size


class ThemedSelector(QComboBox):
    def __init__(self, parent=None, size="medium", bold=False, **kwargs):
        super().__init__(parent)

        # Size configuration
        self._size_type = size
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        # Font configuration
        font_name = FontManager.get_font("lexend")
        self._font = QFont(font_name, 12 if size == "medium" else 14 if size == "large" else 10)
        if bold:
            self._font.setBold(True)
        self.setFont(self._font)

        # Visual effects
        self.setCursor(Qt.PointingHandCursor)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 110))
        self.setGraphicsEffect(shadow)

        # Dropdown view setup
        list_view = QListView()
        list_view.setFont(self._font)
        list_view.setItemDelegate(PerfectDelegate())
        list_view.setSpacing(0)
        list_view.setContentsMargins(0, 0, 0, 0)
        list_view.setFrameShape(QListView.NoFrame)
        self.setView(list_view)

        # Base styling (combobox + dropdown)
        self.setStyleSheet(f"""
            QComboBox {{
                background: {Utils.color_to_rgba_str(CLICKABLE['primary'])};
                color: white;  /* force combobox text to white */
                border: 1px solid {Utils.color_to_rgba_str(CLICKABLE['border'])};
                border-radius: 6px;
                padding: 6px 30px 6px 12px;
                min-width: 100px;
                font-size: {CLICKABLE['fontSizeMedium']}px;
            }}
            QComboBox::drop-down {{
                width: 0;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background: {Utils.color_to_rgba_str(CLICKABLE['primary'])};
                border: none;
                margin: 0px;
                padding: 0px;
                outline: 0;  /* remove faint lines */
            }}
            QComboBox QAbstractItemView::item {{
                margin: 0px;
                padding: 4px 8px;
                height: {self._font.pointSize() + 8}px;
                color: white;  /* dropdown text white */
            }}
            QComboBox QAbstractItemView::item:selected {{
                background: #257bbf;
                color: white;  /* keep text white when selected */
            }}
        """)

    def showPopup(self):
        """Ensure dropdown matches content width exactly and no extra whitespace"""
        width = self._calculate_dropdown_width()
        self.view().setMinimumWidth(width)
        self.view().setFixedWidth(width)

        # Force the popup container background (fixes white top/bottom strips + faint frame)
        popup = self.view().window()
        popup.setStyleSheet(f"""
            background: {Utils.color_to_rgba_str(CLICKABLE['primary'])};
            border: none;  /* remove faint frame */
            border-radius: 6px;
            margin: 0px;
            padding: 0px;
        """)

        super().showPopup()

    def _calculate_dropdown_width(self):
        """Calculate exact width needed for the longest item"""
        fm = self.fontMetrics()
        max_width = max(fm.horizontalAdvance(self.itemText(i)) for i in range(self.count())) + 40
        return max(self.width(), max_width)

    def paintEvent(self, event):
        from utilities.constants import CLICKABLE
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        rect = self.rect()

        # Draw background
        painter.setBrush(QColor(CLICKABLE['primary']))
        painter.setPen(QPen(QColor(CLICKABLE['border']), 1))
        painter.drawRoundedRect(rect, 6, 6)

        # Draw text
        text = self.currentText()
        text_rect = QRect(rect)
        text_rect.adjust(12, 0, -30, 0)  # Proper padding

        painter.setFont(self._font)
        painter.setPen(QColor("white"))  # force text to white
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)

        # Draw arrow
        arrow_size = 6
        arrow_x = rect.right() - 18
        arrow_y = rect.center().y()

        painter.setBrush(QColor("white"))  # arrow white too
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(
            QPoint(arrow_x, arrow_y - arrow_size // 2),
            QPoint(arrow_x + arrow_size, arrow_y - arrow_size // 2),
            QPoint(arrow_x + arrow_size // 2, arrow_y + arrow_size // 2)
        )

        painter.end()

    def addItems(self, texts):
        """Override to adjust size when items are added"""
        super().addItems(texts)
        self.updateGeometry()  # Force size recalculation

    def sizeHint(self):
        """Calculate perfect size based on content"""
        fm = self.fontMetrics()
        text_width = max(
            fm.horizontalAdvance(text)
            for text in [self.itemText(i) for i in range(self.count())] + [self.currentText()]
        )
        return QSize(text_width + 50, 36)  # Width padding + standard height
