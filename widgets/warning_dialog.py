import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QDialog, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QPixmap
from widgets.button import ThemedButton


class WarningDialog(QDialog):
    def __init__(self, message, icon_path=":icons/warning.png", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning")

        # Modal dialog so it blocks interaction, but we still catch global clicks
        self.setModal(True)
        self.setWindowFlags(
    Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self.setFixedSize(300, 150)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(
                pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        icon_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Title + description
        title = QLabel("Warning")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #D32F2F;")  # Material Red 700

        desc = QLabel(message)
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        desc.setStyleSheet("color: #555; font-size: 13px;")

        text_layout = QVBoxLayout()
        text_layout.addWidget(title)
        text_layout.addWidget(desc)

        content_layout = QHBoxLayout()
        content_layout.addWidget(icon_label)
        content_layout.addSpacing(10)
        content_layout.addLayout(text_layout)

        # Buttons
        ok_button = ThemedButton("OK")
        # cancel_button = ThemedButton("CANCEL")
        ok_button.clicked.connect(self.accept)
        # cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        # button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Style
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: transparent;
                color: #1976D2;
                font-weight: bold;
                border: none;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
                border-radius: 5px;
            }
        """)

        # store whether we installed the filter (to avoid double remove)
        self._filter_installed = False

    def showEvent(self, event):
        """Install app-level event filter when dialog is shown and center it over parent."""
        super().showEvent(event)

        app = QApplication.instance()
        if app and not self._filter_installed:
            app.installEventFilter(self)
            self._filter_installed = True

        # center on parent if provided, otherwise center on screen
        if self.parent():
            parent_geom = self.parent().geometry()
            x = parent_geom.center().x() - (self.width() // 2)
            y = parent_geom.center().y() - (self.height() // 2)
            self.move(x, y)
        else:
            screen = QApplication.primaryScreen().availableGeometry()
            x = screen.center().x() - (self.width() // 2)
            y = screen.center().y() - (self.height() // 2)
            self.move(x, y)

    def accept(self):
        """Remove event filter then accept."""
        self._remove_app_filter()
        super().accept()

    def reject(self):
        """Remove event filter then reject."""
        self._remove_app_filter()
        super().reject()

    def closeEvent(self, event):
        """Ensure filter removed on close."""
        self._remove_app_filter()
        super().closeEvent(event)

    def _remove_app_filter(self):
        app = QApplication.instance()
        if app and self._filter_installed:
            try:
                app.removeEventFilter(self)
            except Exception:
                pass
            self._filter_installed = False

    def keyPressEvent(self, event):
        """Treat ESC as Cancel."""
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        """
        Global event filter: if we see a mouse press outside the dialog while the dialog
        is visible, treat it as Cancel (reject).
        """
        if event.type() == QEvent.MouseButtonPress and self.isVisible():
            # map global click position into dialog coordinates
            try:
                global_pos = event.globalPos()
            except Exception:
                return super().eventFilter(obj, event)

            local_pos = self.mapFromGlobal(global_pos)
            if not self.rect().contains(local_pos):
                # clicked outside the dialog: treat as Cancel
                self.reject()
                # swallow the event so underlying widget doesn't also get the click
                return True

        return super().eventFilter(obj, event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material Warning Dialog Demo")
        # self.showFullScreen()

        btn = ThemedButton("Show Warning")
        
        btn.clicked.connect(self.show_warning)

        layout = QVBoxLayout()
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        layout.addWidget(ThemedButton("lollll"))
        self.setLayout(layout)

    def show_warning(self):
        dialog = WarningDialog(
            "Are you sure you want to continue? This action cannot be undone.",
            icon_path=":icons/warning.png",
            parent=self
        )
        result = dialog.exec_()

        if result == QDialog.Accepted:
            print("✅ User pressed OK")
        else:
            print("❌ User pressed Cancel (or clicked outside)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
