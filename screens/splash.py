from PyQt5.QtCore import (
    Qt, QTimer, pyqtProperty, QPropertyAnimation, QEasingCurve, QPointF, pyqtSignal
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect


def cubic_bezier(p0, p1, p2, p3, t: float) -> QPointF:
    """Evaluate cubic Bezier at t in [0,1]."""
    u = 1 - t
    x = (u ** 3) * p0.x() + 3 * (u ** 2) * t * p1.x() + 3 * u * (t ** 2) * p2.x() + (t ** 3) * p3.x()
    y = (u ** 3) * p0.y() + 3 * (u ** 2) * t * p1.y() + 3 * u * (t ** 2) * p2.y() + (t ** 3) * p3.y()
    return QPointF(x, y)


class LogoPainter(QWidget):
    """Draws and animates the logo with outer square and teardrop."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 220)
        self._progress = 0.0
        self._fill_opacity = 0.0

        # Outer square points
        gap = 44
        tl = QPointF(18, 18)
        tr = QPointF(202, 18)
        br = QPointF(202, 202)
        b_inner = QPointF(18 + gap, 202)
        bl_inner = QPointF(18, 202 - gap)
        self.outer_points = [tl, tr, br, b_inner, bl_inner]

        # Teardrop shape
        top      = QPointF(110, 40)
        right_c1 = QPointF(145, 70)
        right_c2 = QPointF(170, 140)
        bottom   = QPointF(110, 150)
        left_c1  = QPointF(50, 140)
        left_c2  = QPointF(75, 70)
        steps = 260
        right_pts = [cubic_bezier(top, right_c1, right_c2, bottom, i / steps) for i in range(steps + 1)]
        left_pts  = [cubic_bezier(bottom, left_c1, left_c2, top, i / steps) for i in range(steps + 1)]
        self.droplet_points = right_pts + left_pts
        self.droplet_polygon = QPolygonF(self.droplet_points)

        # Stroke segments
        self.lines = [
            (tl, tr),
            (tr, br),
            (br, b_inner),
            (bl_inner, tl)
        ]
        for i in range(len(self.droplet_points) - 1):
            self.lines.append((self.droplet_points[i], self.droplet_points[i + 1]))

        # Stroke animation
        self.anim = QPropertyAnimation(self, b"progress")
        self.anim.setDuration(2400)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.finished.connect(self.start_fill)

        # Fill animation
        self._fill_started = False
        self.fill_anim = QPropertyAnimation(self, b"fillOpacity")
        self.fill_anim.setDuration(500)
        self.fill_anim.setStartValue(0.0)
        self.fill_anim.setEndValue(1.0)
        self.fill_anim.setEasingCurve(QEasingCurve.OutCubic)

    def start_animation(self):
        self.anim.start()

    def start_fill(self):
        if not self._fill_started:
            self._fill_started = True
            self.fill_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("white"))  # background always white

        # Stroke
        pen = QPen(QColor("#0A66CC"), 6)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        total_lines = len(self.lines)
        prog_lines = total_lines * self._progress
        full_count = int(prog_lines)
        rem = prog_lines - full_count

        for i in range(full_count):
            p1, p2 = self.lines[i]
            painter.drawLine(p1, p2)

        if full_count < total_lines and rem > 0:
            p1, p2 = self.lines[full_count]
            ix = p1.x() + (p2.x() - p1.x()) * rem
            iy = p1.y() + (p2.y() - p1.y()) * rem
            painter.drawLine(p1, QPointF(ix, iy))

        # Fill droplet
        if self._fill_opacity > 0:
            painter.save()
            fill_color = QColor(186, 235, 255)
            fill_color.setAlphaF(self._fill_opacity)
            painter.setBrush(QBrush(fill_color))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(self.droplet_polygon)
            painter.restore()

            # Highlight
            painter.save()
            hi = QColor(255, 255, 255, int(220 * self._fill_opacity))
            painter.setBrush(QBrush(hi))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(125, 105), 12 * self._fill_opacity + 1, 26 * self._fill_opacity + 1)
            painter.restore()

        # Outline
        outline_pen = QPen(QColor("#0A66CC"), 2)
        outline_pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(outline_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPolyline(self.droplet_polygon)

    # Properties
    def getProgress(self): return self._progress
    def setProgress(self, value):
        self._progress = max(0.0, min(1.0, float(value)))
        self.update()
    progress = pyqtProperty(float, fget=getProgress, fset=setProgress)

    def getFillOpacity(self): return self._fill_opacity
    def setFillOpacity(self, value):
        self._fill_opacity = max(0.0, min(1.0, float(value)))
        self.update()
    fillOpacity = pyqtProperty(float, fget=getFillOpacity, fset=setFillOpacity)


class AnimatedSplash(QWidget):
    finished = pyqtSignal()  # emitted when splash animation finishes

    def __init__(self, parent=None):
        super().__init__(parent)

        # Force solid white background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)

        self.logo = LogoPainter(self)
        self.logo.start_animation()
        self.logo.fill_anim.finished.connect(self.start_text_animation)

        self.char_labels = []
        self.char_anims = []

    def resizeEvent(self, event):
        # Center logo dynamically
        self.logo.move(
            (self.width() - self.logo.width()) // 2,
            (self.height() - self.logo.height()) // 3
        )
        super().resizeEvent(event)

    def start_text_animation(self):
        text = "Automatic Pipetting Station"
        font = QFont("Arial", 24, QFont.Bold)
        fm = QFontMetrics(font)
        spacing = 6
        widths = [fm.horizontalAdvance(ch) for ch in text]
        total_width = sum(widths) + spacing * (len(text) - 1)
        start_x = (self.width() - total_width) // 2
        y = (self.logo.y() + self.logo.height() + 20)

        delay_per_char = 110
        for i, ch in enumerate(text):
            w = widths[i]
            h = fm.height()
            lbl = QLabel(ch, self)
            lbl.setFont(font)
            lbl.setStyleSheet("color: #0A66CC; background: transparent;")
            lbl.setAttribute(Qt.WA_TranslucentBackground)
            lbl.setGeometry(start_x, y, w + 4, h + 2)
            lbl.setAlignment(Qt.AlignCenter)

            effect = QGraphicsOpacityEffect(lbl)
            effect.setOpacity(0.0)
            lbl.setGraphicsEffect(effect)
            lbl.show()

            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(220)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            QTimer.singleShot(i * delay_per_char, anim.start)

            self.char_labels.append(lbl)
            self.char_anims.append(anim)
            start_x += w + spacing

        # Emit finished after last character
        if self.char_anims:
            self.char_anims[-1].finished.connect(lambda: QTimer.singleShot(900, self.finished.emit))
