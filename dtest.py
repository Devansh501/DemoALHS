import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication, 
                             QDialog, QPushButton, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie, QFont


from resources import resources



class LabLoadingWidget(QDialog):
    """Reusable lab-themed loading modal with GIF animation"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(450, 320)  # Reduced from 600x450


        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)  # Reduced from 40
        layout.setSpacing(15)  # Reduced from 25


        # Title label
        self.label = QLabel("Preparing Automatic Pipetting System...")
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 12, QFont.Medium)  # Reduced from 14
        self.label.setFont(font)
        self.label.setStyleSheet("color: #4A5568; background: transparent;")
        layout.addWidget(self.label)


        # GIF animation label
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_label.setStyleSheet("background: transparent;")
        
        # Load GIF from resources - smaller size to fit compact modal
        self.movie = QMovie(":/images/processLoader.gif")
        self.movie.setScaledSize(QSize(350, 180))  # Reduced from 500x280, preserves aspect ratio
        self.animation_label.setMovie(self.movie)
        
        layout.addWidget(self.animation_label)


        # Status label
        self.status_label = QLabel("Initializing components...")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Arial", 10, QFont.Normal)  # Reduced from 11
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #718096; background: transparent;")
        layout.addWidget(self.status_label)


    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw semi-transparent backdrop
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        # Draw white rounded card
        card_rect = self.rect().adjusted(15, 15, -15, -15)  # Reduced from 20
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(226, 232, 240), 2))
        painter.drawRoundedRect(card_rect, 16, 16)  # Reduced from 20
        painter.end()


    def startAnimation(self):
        """Start the GIF animation"""
        self.movie.start()


    def stopAnimation(self):
        """Stop the GIF animation"""
        self.movie.stop()


    def showEvent(self, event):
        """Auto-start animation when dialog is shown"""
        super().showEvent(event)
        self.startAnimation()


    def closeEvent(self, event):
        """Stop animation when dialog is closed"""
        self.stopAnimation()
        super().closeEvent(event)



class TestWindow(QMainWindow):
    """Test window with button to toggle loading modal"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Loading Widget Test - GIF Version")
        self.setGeometry(100, 100, 400, 300)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        title = QLabel("Automatic Pipetting System")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.toggle_btn = QPushButton("Show Loading Screen")
        self.toggle_btn.setFont(QFont("Arial", 12))
        self.toggle_btn.setFixedSize(200, 50)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #8BB140;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9DC154;
            }
            QPushButton:pressed {
                background-color: #7A9E38;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggleLoading)
        layout.addWidget(self.toggle_btn, alignment=Qt.AlignCenter)
        
        from PyQt5.QtCore import QTimer
        self.auto_hide_btn = QPushButton("Show for 3 seconds")
        self.auto_hide_btn.setFont(QFont("Arial", 11))
        self.auto_hide_btn.setFixedSize(200, 40)
        self.auto_hide_btn.setStyleSheet("""
            QPushButton {
                background-color: #38B2AC;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #319795;
            }
        """)
        self.auto_hide_btn.clicked.connect(self.showLoadingTimed)
        layout.addWidget(self.auto_hide_btn, alignment=Qt.AlignCenter)
        
        self.loading_widget = None


    def toggleLoading(self):
        if self.loading_widget and self.loading_widget.isVisible():
            self.loading_widget.stopAnimation()
            self.loading_widget.close()
            self.loading_widget = None
            self.toggle_btn.setText("Show Loading Screen")
        else:
            self.loading_widget = LabLoadingWidget(self)
            self.loading_widget.show()
            self.toggle_btn.setText("Hide Loading Screen")


    def showLoadingTimed(self):
        from PyQt5.QtCore import QTimer
        
        self.loading_widget = LabLoadingWidget(self)
        self.loading_widget.show()
        QTimer.singleShot(3000, lambda: self.hideLoading())


    def hideLoading(self):
        if self.loading_widget:
            self.loading_widget.stopAnimation()
            self.loading_widget.close()
            self.loading_widget = None
            self.toggle_btn.setText("Show Loading Screen")



def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
