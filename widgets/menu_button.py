import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QEasingCurve, QRectF, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QBrush, QPen

from utilities.fontManager import FontManager
from utilities.constants import MENU_BUTTON


class MenuButton(QWidget):
    clicked = pyqtSignal()  # ✅ Custom signal

    def __init__(self, text="", fontSize=22,btnHeight = MENU_BUTTON['height'],btnWidth = MENU_BUTTON['length'],parent=None):
        super().__init__(parent)
        self.setFixedSize(btnWidth, btnHeight)
        self._text = text

        font_name = FontManager.get_font(MENU_BUTTON['font_name'])
        self._font = QFont(font_name, fontSize)

        self._scale = 1.0
        self._shadowMode = "normal"  # "normal" or "pressed"
        self._press_inside = False  # ✅ Track if press started inside

        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(100)
        self._scale_anim.setEasingCurve(QEasingCurve.InOutQuad)

        self._click_locked = False
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        radius = 25
        scale = self._scale

        painter.save()
        painter.translate(w / 2, h / 2)
        painter.scale(scale, scale)
        painter.translate(-w / 2, -h / 2)

        button_rect = QRectF(10, 10, w - 20, h - 20)

        if self._shadowMode == "normal":
            self._draw_normal_shadow(painter, button_rect, radius)
        elif self._shadowMode == "pressed":
            self._draw_pressed_shadow(painter, button_rect, radius)

        # --- Button background ---
        painter.setBrush(QColor(MENU_BUTTON['bgColor']))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(button_rect, radius, radius)

        # --- Border ---
        painter.setPen(QPen(Qt.black, 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(button_rect, radius, radius)

        # --- Text ---
        painter.setFont(self._font)
        painter.setPen(QColor(MENU_BUTTON['color']))
        margin = 20
        text_rect = button_rect.adjusted(margin, margin, -margin, -margin)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self._text)

        painter.restore()

    def _draw_normal_shadow(self, painter, rect, radius):
        """Strong shadow on bottom and right edges (resting)."""
        layers = 14
        for i in range(layers):
            offset = i + 1
            alpha = int(80 * (1 - i / layers))  # softer shadow
            color = QColor(0, 0, 0, alpha)

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)

            path = QPainterPath()
            path.addRoundedRect(
                QRectF(
                    rect.left() + offset * 0.4,
                    rect.top() + offset * 0.4,
                    rect.width(),
                    rect.height()
                ),
                radius + offset * 0.3,
                radius + offset * 0.3
            )
            painter.drawPath(path)

    def _draw_pressed_shadow(self, painter, rect, radius):
        """Strong bottom-only shadow (pressed state)."""
        layers = 10
        for i in range(layers):
            offset = i + 1
            alpha = int(80 * (1 - i / layers))  # match with normal
            color = QColor(0, 0, 0, alpha)

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)

            path = QPainterPath()
            path.addRoundedRect(
                QRectF(
                    rect.left(),
                    rect.top() + offset * 0.6,
                    rect.width(),
                    rect.height()
                ),
                radius + offset * 0.3,
                radius + offset * 0.3
            )
            painter.drawPath(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._click_locked:
            self._click_locked = True
            self._press_inside = True
            self._animate_press()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._press_inside and self.rect().contains(event.pos()):
                self.clicked.emit()  # ✅ Emit custom clicked signal
            self._animate_release()
            QTimer.singleShot(200, self._unlock_click)
        super().mouseReleaseEvent(event)

    def _unlock_click(self):
        self._click_locked = False
        self._press_inside = False

    def _animate_press(self):
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(0.94)
        self._scale_anim.start()

        self._shadowMode = "pressed"
        self.update()

    def _animate_release(self):
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(1.0)
        self._scale_anim.start()

        self._shadowMode = "normal"
        self.update()

    # --- Scale property ---
    def getScale(self):
        return self._scale

    def setScale(self, value):
        self._scale = value
        self.update()

    scale = pyqtProperty(float, fget=getScale, fset=setScale)
