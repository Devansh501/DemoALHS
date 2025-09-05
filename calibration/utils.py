from PyQt5.QtWidgets import QMessageBox, QLabel, QPushButton
from PyQt5.QtCore import QTimer

class Utils:
    def warning(self,obj,text):
        msg = QMessageBox(obj)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #23272e;
                color: white;
                border-radius: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
            }
            QLabel, QMessageBox QLabel {
                background-color: #23272e;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 0px;
                padding: 8px 0 8px 0;
            }
            QPushButton {
                background-color: #3b4252;
                color: white;
                border: 1px solid #81a1c1;
                padding: 8px 24px;
                border-radius: 6px;
                font-size: 15px;
                margin: 8px 4px;
            }
            QPushButton:hover {
                background-color: #5e81ac;
                color: #fff;
            }
        """)
        
        label = msg.findChild(QLabel)
        if label:
            label.setStyleSheet("background-color: #23272e; color: white; font-size: 18px; font-weight: bold; border-radius: 0px; padding: 8px 0 8px 0;")
        msg.exec_()
        return
