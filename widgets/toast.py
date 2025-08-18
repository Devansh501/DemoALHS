import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor


class ToastWidget(QWidget):
    COLORS = {
        "success": ("#E6F4EA", "#1E4620", "#34A853"),
        "danger": ("#FCE8E6", "#5F2120", "#EA4335"),
        "stop": ("#FDE7E9", "#611A1E", "#D93025"),
        "failed": ("#FCE8E6", "#5F2120", "#D93025"),
        "warning": ("#FEF7E0", "#4E342E", "#F9AB00"),
    }

    def __init__(self, parent, title, message, state="success", duration=3000):
        super().__init__(parent)
        # Use Qt.ToolTip for better Wayland positioning
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.duration = duration
        self.elapsed = 0

        # Colors
        bg_color, text_color, accent_color = self.COLORS.get(state, self.COLORS["success"])

        # Main container widget
        container = QWidget(self)
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 0px;
            }}
        """)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)

        # Title label
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Roboto", 10, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {text_color}; background: transparent;")

        # Message label
        msg_lbl = QLabel(message)
        msg_lbl.setFont(QFont("Roboto", 9))
        msg_lbl.setStyleSheet(f"color: {text_color}; background: transparent;")
        msg_lbl.setWordWrap(True)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setFocusPolicy(Qt.NoFocus)
        close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 14px;
                color: rgba(0,0,0,0.54);
            }
            QPushButton:hover {
                color: red;
            }
        """)
        close_btn.clicked.connect(self.close)

        # Progress bar inside card
        self.progress_bar = QWidget()
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet(
            f"background-color: {accent_color}; border-radius: 0px;"
        )

        # Layout for text and close button
        header_layout = QHBoxLayout()
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)

        text_layout = QVBoxLayout()
        text_layout.addLayout(header_layout)
        text_layout.addWidget(msg_lbl)

        # Main container layout
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 12, 16, 0)
        container_layout.setSpacing(8)
        container_layout.addLayout(text_layout)
        container_layout.addWidget(self.progress_bar)

        # Outer layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(container)

        # Timer for progress bar shrink
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)

        self.show()
        self.adjustSize()
        self.move_to_bottom_mid()

    def move_to_bottom_mid(self, margin_percent=0.15):
        """Place toast horizontally centered, margin_percent from bottom."""
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        x = geometry.x() + (geometry.width() - self.width()) // 2
        y = geometry.y() + geometry.height() - self.height() - int(geometry.height() * margin_percent)
        self.move(x, y)

    def update_progress(self):
        self.elapsed += 30
        remaining_ratio = max(0, 1 - self.elapsed / self.duration)
        new_width = int(self.width() * remaining_ratio)
        self.progress_bar.setFixedWidth(new_width)

        if self.elapsed >= self.duration:
            self.timer.stop()
            self.close()
