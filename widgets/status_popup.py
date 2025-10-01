import sys
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPointF
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QPushButton, QHBoxLayout
)

# ----------- Smooth Icon Makers -----------
def make_success_icon(size=96):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, True)

    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor("#28a745"))
    painter.drawEllipse(0, 0, size, size)

    path = QPainterPath()
    path.moveTo(QPointF(size * 0.28, size * 0.55))
    path.lineTo(QPointF(size * 0.45, size * 0.72))
    path.lineTo(QPointF(size * 0.75, size * 0.38))

    pen = QPen(Qt.white, size * 0.1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    painter.setPen(pen)
    painter.drawPath(path)
    painter.end()
    return pixmap


def make_failure_icon(size=96):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, True)

    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor("#dc3545"))
    painter.drawEllipse(0, 0, size, size)

    pen = QPen(Qt.white, size * 0.1, Qt.SolidLine, Qt.RoundCap)
    painter.setPen(pen)
    painter.drawLine(QPointF(size * 0.3, size * 0.3), QPointF(size * 0.7, size * 0.7))
    painter.drawLine(QPointF(size * 0.7, size * 0.3), QPointF(size * 0.3, size * 0.7))
    painter.end()
    return pixmap


# ----------- Popup Dialog (Opaque, Centered) -----------
class StatusPopup(QWidget):
    def __init__(self, message, status="success", duration=2000, parent=None):
        super().__init__(parent)

        # Frameless floating dialog
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Tool
            | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Known final size
        # self.popup_width = 280
        # self.popup_height = 180
        # self.resize(self.popup_width, self.popup_height)
        screen_geom = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_geom)

        # Outer layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        # Container with rounded opaque background
        container = QWidget()
        container.setObjectName("popupContainer")
        container.setStyleSheet("""
            QWidget#popupContainer {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 16px;
            }
        """)

        inner_layout = QVBoxLayout(container)
        inner_layout.setContentsMargins(30, 30, 30, 30)
        inner_layout.setSpacing(12)
        inner_layout.setAlignment(Qt.AlignCenter)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        pixmap = make_success_icon(80) if status == "success" else make_failure_icon(80)
        self.icon_label.setPixmap(pixmap)

        # Message
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.message_label.setStyleSheet("color: white; background: transparent;")
        self.message_label.setAlignment(Qt.AlignCenter)

        # Add widgets
        inner_layout.addWidget(self.icon_label)
        inner_layout.addWidget(self.message_label)
        main_layout.addWidget(container)

        # Auto-close
        QTimer.singleShot(duration, self.close)

        # Fade-in animation
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

        # Show widget
        self.show()

    def showEvent(self, event):
        """Center popup on screen after layout is calculated"""
        super().showEvent(event)
        screen_geom = QApplication.primaryScreen().availableGeometry()
        w, h = self.width(), self.height()
        x = screen_geom.center().x() - w // 2
        y = screen_geom.center().y() - h // 2
        self.setGeometry(x, y, w, h)


# ----------- Test Window -----------
class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Status Popup Test")
        self.setGeometry(200, 200, 400, 200)

        layout = QHBoxLayout(self)
        success_btn = QPushButton("Show Success")
        fail_btn = QPushButton("Show Failure")

        success_btn.clicked.connect(
            lambda: StatusPopup("Operation Successful!", status="success", duration=2500)
        )
        fail_btn.clicked.connect(
            lambda: StatusPopup("Operation Failed!", status="failure", duration=2500)
        )

        layout.addWidget(success_btn)
        layout.addWidget(fail_btn)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())
